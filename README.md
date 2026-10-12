Self-Learning AI Agent 🤖

📌 Project Overview

The Self-Learning AI Agent is a Python-based web application built using Flask. It allows users to interact with an AI-style chatbot, store knowledge, retrieve previous conversations, and learn from user feedback.

The project demonstrates rule-based responses, knowledge management, conversation memory, and basic analytics.

✨ Features

- AI Chat Interface: Ask questions and receive responses.
- Conversation Memory: Stores and retrieves previous conversations.
- Knowledge Base: Teach the agent new information.
- Knowledge Management: Search, update, and delete stored knowledge.
- Web Search: Retrieve information using Wikipedia search.
- User Feedback: Record feedback to improve stored knowledge.
- Calculator: Perform basic mathematical calculations.
- Date and Time: Retrieve current date and time.
- Learning Log: Track knowledge added through learning activities.
- Analytics Dashboard: View knowledge categories and statistics.
- CSV Export: Export knowledge-base data to a CSV file.

🛠️ Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Bootstrap
- Chart.js
- Wikipedia API

📂 Project Structure

self_learning_ai_agent/
├── templates/
│   └── index.html
├── app.py
├── agent.py
├── memory.py
├── tools.py
├── .gitignore
└── README.md

⚙️ Installation and Setup

1. Clone the repository

git clone https://github.com/DivyaBarate/self-learning-ai-agent.git
cd self-learning-ai-agent

2. Install dependencies

pip install flask requests

3. Run the application

python app.py

4. Open in your browser

Visit:

http://127.0.0.1:5000

🧠 How It Works

The application uses Python-based logic to process user questions, retrieve relevant stored knowledge, and generate responses. SQLite stores conversations and knowledge. User feedback and selected search results can update the knowledge base and learning log.

Note: This is a rule-based AI-style application. It does not train a large language model.

🚀 Future Improvements

- Integrate a language model for more natural responses.
- Improve semantic search and knowledge retrieval.
- Add automated tests and error handling.
- Improve the user interface and accessibility.

👩‍💻 Author

Divya Barate

GitHub: "DivyaBarate" (https://github.com/DivyaBarate)
