from flask import Flask, request, render_template, redirect, Response
import re
import csv
import io
from agent import get_response

from memory import (
    create_database,
    save_conversation,
    update_feedback,
    get_conversations,
    search_memory,
    save_knowledge,
    search_knowledge,
    get_feedback_stats,
    get_all_knowledge,
    delete_knowledge,
    update_knowledge,
    get_knowledge_count,
    get_learning_logs,
    get_learning_count,
    get_category_counts,
    get_conversation_by_id,
    save_learning_log,
    clear_learning_logs
)


app = Flask(__name__)

create_database()


# =========================================================
# AUTOMATIC CATEGORY DETECTION
# =========================================================

def detect_category(text):

    text = text.lower()

    electronics_words = [
        "arduino",
        "electronics",
        "circuit",
        "pcb",
        "vlsi",
        "antenna",
        "transistor",
        "diode",
        "resistor",
        "capacitor",
        "microcontroller",
        "communication",
        "wireless",
        "rf",
        "microwave"
    ]

    programming_words = [
        "python",
        "java",
        "programming",
        "code",
        "flask",
        "javascript",
        "html",
        "css",
        "sql",
        "database"
    ]

    ai_words = [
        "ai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "neural network",
        "yolo",
        "nlp",
        "chatbot",
        "computer vision"
    ]

    iot_words = [
        "iot",
        "internet of things",
        "smart device",
        "smart home",
        "sensor network",
        "wsn"
    ]

    hardware_words = [
        "esp32",
        "esp8266",
        "raspberry pi",
        "sensor",
        "breadboard",
        "processor",
        "hardware",
        "laptop",
        "computer"
    ]

    software_words = [
        "software",
        "windows",
        "application",
        "app",
        "website",
        "operating system",
        "linux"
    ]


    # Electronics
    for word in electronics_words:

        if word in text:
            return "Electronics"


    # Programming
    for word in programming_words:

        if word in text:
            return "Programming"


    # AI / ML
    for word in ai_words:

        if word in text:
            return "AI/ML"


    # IoT
    for word in iot_words:

        if word in text:
            return "IoT"


    # Hardware
    for word in hardware_words:

        if word in text:
            return "Hardware"


    # Software
    for word in software_words:

        if word in text:
            return "Software"


    return "General"


# =========================================================
# CLEAN AI RESPONSE BEFORE LEARNING
# =========================================================

def clean_response(ai_response):

    if not ai_response:
        return ""

    # Remove Confidence percentage
    clean_response = re.sub(
        r"\s*Confidence:\s*\d+%",
        "",
        ai_response,
        flags=re.IGNORECASE
    ).strip()

    return clean_response


# =========================================================
# HOME / ASK AI
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    response = ""

    if request.method == "POST":

        user_message = request.form.get(
            "message",
            ""
        ).strip()


        if user_message:

            # ---------------------------------------------
            # Search learned knowledge
            # ---------------------------------------------

            words = re.findall(
                r"\b[a-zA-Z0-9]+\b",
                user_message.lower()
            )

            knowledge = []


            for word in words:

                if len(word) >= 3:

                    results = search_knowledge(word)

                    if results:

                        knowledge.extend(results)


            # Remove duplicates
            knowledge = list(
                dict.fromkeys(knowledge)
            )


            # Maximum 5 knowledge items
            knowledge = knowledge[:5]


            # ---------------------------------------------
            # Search conversation memory
            # ---------------------------------------------

            memories = search_memory(
                user_message
            )


            # ---------------------------------------------
            # Prepare knowledge for agent
            # ---------------------------------------------

            agent_knowledge = []


            for item in knowledge:

                agent_knowledge.append(
                    (
                        item[0],
                        item[1]
                    )
                )


            # ---------------------------------------------
            # Get AI response
            # ---------------------------------------------

            response = get_response(
                user_message,
                memories,
                agent_knowledge
            )


            # ---------------------------------------------
            # Save conversation
            # ---------------------------------------------

            save_conversation(
                user_message,
                response
            )


    # ---------------------------------------------
    # Dashboard data
    # ---------------------------------------------

    conversations = get_conversations()

    knowledge_list = get_all_knowledge()

    knowledge_count = get_knowledge_count()

    learning_logs = get_learning_logs()

    learning_count = get_learning_count()

    category_counts = get_category_counts()

    total, helpful, not_helpful = (
        get_feedback_stats()
    )


    return render_template(
        "index.html",

        response=response,

        conversations=conversations,

        knowledge_list=knowledge_list,

        knowledge_count=knowledge_count,

        learning_logs=learning_logs,

        learning_count=learning_count,

        category_counts=category_counts,

        total=total,

        helpful=helpful,

        not_helpful=not_helpful
    )


# =========================================================
# TEACH AI
# =========================================================

@app.route(
    "/teach",
    methods=["POST"]
)
def teach():

    topic = request.form.get(
        "topic",
        ""
    ).strip()


    information = request.form.get(
        "information",
        ""
    ).strip()


    category = request.form.get(
        "category",
        "General"
    )


    if topic and information:

        # Save knowledge
        save_knowledge(
            topic,
            information,
            category
        )


        # Save learning activity
        save_learning_log(
            topic,
            "Manual Teaching"
        )


    return redirect("/")


# =========================================================
# UPDATE KNOWLEDGE
# =========================================================

@app.route(
    "/update_knowledge/<int:knowledge_id>",
    methods=["POST"]
)
def update_knowledge_route(
    knowledge_id
):

    topic = request.form.get(
        "topic",
        ""
    ).strip()


    information = request.form.get(
        "information",
        ""
    ).strip()


    category = request.form.get(
        "category",
        "General"
    )


    if topic and information:

        update_knowledge(
            knowledge_id,
            topic,
            information,
            category
        )


    return redirect("/")


# =========================================================
# DELETE KNOWLEDGE
# =========================================================

@app.route(
    "/delete_knowledge/<int:knowledge_id>",
    methods=["POST"]
)
def delete_knowledge_route(
    knowledge_id
):

    delete_knowledge(
        knowledge_id
    )


    return redirect("/")

# =========================================================
# EXPORT KNOWLEDGE BASE
# =========================================================

@app.route("/export_knowledge")
def export_knowledge():

    knowledge_list = get_all_knowledge()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Topic",
        "Information",
        "Category"
    ])

    for item in knowledge_list:

        writer.writerow([
            item[0],
            item[1],
            item[2],
            item[3]
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=knowledge_base.csv"
    )

    return response


# =========================================================
# FEEDBACK
# =========================================================

@app.route(
    "/feedback",
    methods=["POST"]
)
def feedback():

    conversation_id = request.form.get(
        "conversation_id",
        ""
    )


    feedback_value = request.form.get(
        "feedback",
        ""
    )


    # ---------------------------------------------
    # Save feedback
    # ---------------------------------------------

    update_feedback(
        conversation_id,
        feedback_value
    )


    # =================================================
    # HELPFUL FEEDBACK = LEARN
    # =================================================

    if feedback_value == "1":

        conversation = get_conversation_by_id(
            conversation_id
        )


        if conversation:

            user_message, ai_response = conversation


            # -----------------------------------------
            # CLEAN RESPONSE
            # -----------------------------------------

            clean_ai_response = clean_response(
                ai_response
            )


            # -----------------------------------------
            # Detect category
            # -----------------------------------------

            category = detect_category(
                user_message
            )


            # -----------------------------------------
            # Save cleaned knowledge
            # -----------------------------------------

            save_knowledge(
                user_message,
                clean_ai_response,
                category
            )


            # -----------------------------------------
            # Learning log
            # -----------------------------------------

            save_learning_log(
                user_message,
                "Helpful Feedback - " + category
            )


    return redirect("/")


# =========================================================
# CLEAR LEARNING LOG
# =========================================================

@app.route(
    "/clear_learning",
    methods=["POST"]
)
def clear_learning():

    clear_learning_logs()

    return redirect("/")


# =========================================================
# CANCEL / BACK
# =========================================================

@app.route(
    "/cancel"
)
def cancel():

    return redirect("/")

# =========================================================
# ANALYTICS DATA
# =========================================================

@app.route("/analytics_data")
def analytics_data():

    total, helpful, not_helpful = get_feedback_stats()

    data = {
        "total": total,
        "helpful": helpful,
        "not_helpful": not_helpful,
        "knowledge": get_knowledge_count(),
        "learning": get_learning_count()
    }

    return data


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )