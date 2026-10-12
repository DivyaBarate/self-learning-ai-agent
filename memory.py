import sqlite3

DATABASE = "conversations.db"


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            ai_response TEXT,
            feedback TEXT
        )
    """)

    try:
        cursor.execute(
            "ALTER TABLE conversations ADD COLUMN feedback TEXT"
        )
    except sqlite3.OperationalError:
        pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            information TEXT,
            category TEXT DEFAULT 'General'
        )
    """)

    try:
        cursor.execute(
            "ALTER TABLE knowledge ADD COLUMN category TEXT DEFAULT 'General'"
        )
    except sqlite3.OperationalError:
        pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            source TEXT,
            learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_conversation(user_message, ai_response):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations
        (user_message, ai_response)
        VALUES (?, ?)
    """, (user_message, ai_response))

    conn.commit()
    conn.close()


def update_feedback(conversation_id, feedback):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE conversations
        SET feedback = ?
        WHERE id = ?
    """, (feedback, conversation_id))

    conn.commit()
    conn.close()


def get_conversation_by_id(conversation_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_message, ai_response
        FROM conversations
        WHERE id = ?
    """, (conversation_id,))

    result = cursor.fetchone()

    conn.close()

    return result


def get_conversations():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, user_message, ai_response, feedback
        FROM conversations
        ORDER BY id DESC
    """)

    conversations = cursor.fetchall()

    conn.close()

    return conversations


def search_memory(keyword):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_message, ai_response
        FROM conversations
        WHERE user_message LIKE ?
           OR ai_response LIKE ?
        ORDER BY
            CASE
                WHEN feedback = '1' THEN 0
                WHEN feedback = '-1' THEN 2
                ELSE 1
            END,
            id DESC
        LIMIT 5
    """, (f"%{keyword}%", f"%{keyword}%"))

    results = cursor.fetchall()

    conn.close()

    return results


def save_knowledge(topic, information, category="General"):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM knowledge
        WHERE LOWER(topic) = LOWER(?)
    """, (topic,))

    existing = cursor.fetchone()

    if existing:

        cursor.execute("""
            UPDATE knowledge
            SET information = ?, category = ?
            WHERE id = ?
        """, (information, category, existing[0]))

    else:

        cursor.execute("""
            INSERT INTO knowledge
            (topic, information, category)
            VALUES (?, ?, ?)
        """, (topic, information, category))

    conn.commit()
    conn.close()


def search_knowledge(keyword):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic, information, category
        FROM knowledge
        WHERE topic LIKE ?
           OR information LIKE ?
           OR category LIKE ?
        ORDER BY id DESC
        LIMIT 5
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    results = cursor.fetchall()

    conn.close()

    return results


def get_all_knowledge():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, topic, information, category
        FROM knowledge
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    conn.close()

    return results


def delete_knowledge(knowledge_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM knowledge
        WHERE id = ?
    """, (knowledge_id,))

    conn.commit()
    conn.close()


def update_knowledge(
    knowledge_id,
    topic,
    information,
    category="General"
):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE knowledge
        SET topic = ?, information = ?, category = ?
        WHERE id = ?
    """, (
        topic,
        information,
        category,
        knowledge_id
    ))

    conn.commit()
    conn.close()


def get_feedback_stats():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM conversations
        WHERE feedback = '1'
    """)
    helpful = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM conversations
        WHERE feedback = '-1'
    """)
    not_helpful = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM conversations
    """)
    total = cursor.fetchone()[0]

    conn.close()

    return total, helpful, not_helpful


def get_knowledge_count():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM knowledge
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


def save_learning_log(topic, source):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO learning_log
        (topic, source)
        VALUES (?, ?)
    """, (topic, source))

    conn.commit()
    conn.close()


def get_learning_logs():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, topic, source, learned_at
        FROM learning_log
        ORDER BY id DESC
        LIMIT 20
    """)

    results = cursor.fetchall()

    conn.close()

    return results


def get_learning_count():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM learning_log
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


def clear_learning_logs():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM learning_log
    """)

    conn.commit()
    conn.close()


def get_category_counts():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, COUNT(*)
        FROM knowledge
        GROUP BY category
        ORDER BY COUNT(*) DESC
    """)

    results = cursor.fetchall()

    conn.close()

    return results

def delete_arduino_knowledge():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM knowledge
        WHERE LOWER(topic) LIKE '%arduino%'
           OR LOWER(information) LIKE '%arduino%'
    """)

    conn.commit()
    conn.close()


create_database()