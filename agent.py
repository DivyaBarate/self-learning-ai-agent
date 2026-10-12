from tools import calculate, get_current_datetime, web_search
from memory import save_knowledge, save_learning_log
import re


# =========================================================
# WORD NORMALIZATION
# =========================================================

def normalize_word(word):

    word = word.lower().strip()

    if word.endswith("ing") and len(word) > 5:
        word = word[:-3]

    elif word.endswith("ed") and len(word) > 4:
        word = word[:-2]

    elif word.endswith("s") and len(word) > 3:
        word = word[:-1]

    return word


# =========================================================
# KEYWORD EXTRACTION
# =========================================================

def get_keywords(text):

    stop_words = {
        "what", "is", "are", "the", "a", "an",
        "how", "why", "when", "where", "can",
        "you", "please", "tell", "me", "about",
        "explain", "define", "does", "do",
        "and", "of", "to", "in", "for",
        "this", "that", "know", "give",
        "information", "details"
    }

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    keywords = []

    for word in words:

        if len(word) >= 3 and word not in stop_words:

            normalized = normalize_word(word)

            if normalized not in keywords:
                keywords.append(normalized)

    return keywords


# =========================================================
# CLEAN LEARNED RESPONSE
# =========================================================

def clean_learned_response(information):

    if not information:
        return ""

    # Remove old Confidence text
    information = re.sub(
        r"\s*Confidence:\s*\d+%",
        "",
        information,
        flags=re.IGNORECASE
    ).strip()

    # Remove repeated learned-knowledge introduction
    information = re.sub(
        r"^(According to my learned knowledge about .*?:\s*)+",
        "",
        information,
        flags=re.IGNORECASE
    ).strip()

    return information


# =========================================================
# AI RESPONSE
# =========================================================

def get_response(
    user_message,
    memories=None,
    learned_knowledge=None
):

    user_message_lower = (
        user_message.lower().strip()
    )

    question_keywords = get_keywords(
        user_message
    )


    # =====================================================
    # DATE / TIME
    # =====================================================

    if any(word in user_message_lower for word in [
        "date",
        "time",
        "today",
        "current date",
        "current time"
    ]):

        return (
            get_current_datetime()
            + "\n\nConfidence: 100%"
        )


    # =====================================================
    # WEB SEARCH
    # =====================================================

    if (
        user_message_lower.startswith("search")
        or "search for" in user_message_lower
        or "search the web" in user_message_lower
    ):

        query = user_message_lower

        query = query.replace(
            "search the web",
            ""
        )

        query = query.replace(
            "search for",
            ""
        )

        query = query.replace(
            "search",
            ""
        )

        query = query.strip()


        if query:

            search_result = web_search(
                query
            )

            save_knowledge(
                query,
                search_result,
                "General"
            )

            save_learning_log(
                query,
                "Web Search"
            )

            return (
                f"{search_result}\n\n"
                f"Confidence: 95%"
            )


        return (
            "Please enter something to search."
        )


    # =====================================================
    # CALCULATOR
    # =====================================================

    if (
        "calculate" in user_message_lower
        or user_message_lower.startswith("what is")
    ):

        try:

            expression = user_message_lower

            expression = expression.replace(
                "calculate",
                ""
            )

            expression = expression.replace(
                "what is",
                ""
            )

            expression = expression.strip()


            allowed = (
                "0123456789+-*/%(). "
            )


            if expression and all(
                character in allowed
                for character in expression
            ):

                result = calculate(
                    expression
                )

                return (
                    f"The result is {result}\n\n"
                    f"Confidence: 100%"
                )

        except Exception:

            pass


    # =====================================================
    # LEARNED KNOWLEDGE
    # =====================================================

    if (
        learned_knowledge
        and question_keywords
    ):

        best_match = None
        best_score = 0


        for topic, information in learned_knowledge:

            topic_keywords = set(
                get_keywords(topic)
            )

            information_keywords = set(
                get_keywords(information)
            )


            score = 0


            # Topic keyword matching
            for keyword in question_keywords:

                if keyword in topic_keywords:

                    score += 5

                elif keyword in information_keywords:

                    score += 1


            # Extra score for topic match
            common_topic_words = (
                set(question_keywords)
                & topic_keywords
            )


            if common_topic_words:

                score += 2


            if score > best_score:

                best_score = score

                best_match = (
                    topic,
                    information
                )


        # =================================================
        # STRONG LEARNED MATCH
        # =================================================

        if (
            best_match
            and best_score >= 5
        ):

            topic, information = (
                best_match
            )


            clean_information = (
                clean_learned_response(
                    information
                )
            )


            # ---------------------------------------------
            # EXACT TOPIC MATCH
            # ---------------------------------------------

            topic_keywords = set(
                get_keywords(topic)
            )

            question_keyword_set = set(
                question_keywords
            )


            if (
                topic_keywords
                and topic_keywords.issubset(
                    question_keyword_set
                )
            ):

                confidence = 100

            else:

                confidence = 90


            return (
                f"{clean_information}\n\n"
                f"Confidence: {confidence}%"
            )


    # =====================================================
    # PREVIOUS MEMORY
    # =====================================================

    if memories:

        message, answer = memories[0]

        clean_answer = re.sub(
            r"\s*Confidence:\s*\d+%",
            "",
            answer,
            flags=re.IGNORECASE
        ).strip()


        return (
            "I found a relevant previous "
            "conversation in my memory.\n\n"
            f"Previous question: {message}\n"
            f"Previous answer: {clean_answer}\n\n"
            f"Confidence: 70%"
        )


    # =====================================================
    # BASIC RESPONSES
    # =====================================================

    if (
        "hello" in user_message_lower
        or "hi" in user_message_lower
    ):

        return (
            "Hello! I am your "
            "Self-Learning AI Agent.\n\n"
            "Confidence: 100%"
        )


    elif "name" in user_message_lower:

        return (
            "I am a Self-Learning AI Agent.\n\n"
            "Confidence: 100%"
        )


    elif "iot" in user_message_lower:

        return (
            "IoT stands for Internet of Things. "
            "It connects physical devices to the "
            "internet so they can collect and "
            "exchange data.\n\n"
            "Confidence: 95%"
        )


    elif "python" in user_message_lower:

        return (
            "Python is a high-level programming "
            "language used for software development, "
            "web development, artificial intelligence, "
            "data analysis, and automation.\n\n"
            "Confidence: 95%"
        )


    elif "arduino" in user_message_lower:

        return (
            "Arduino is an open-source electronics "
            "platform used for building and programming "
            "electronic projects.\n\n"
            "Confidence: 95%"
        )


    # =====================================================
    # UNKNOWN QUESTION
    # =====================================================

    else:

        return (
            "I am not confident about this question yet. "
            "Please teach me using the Teach AI section.\n\n"
            "Confidence: 0%"
        )