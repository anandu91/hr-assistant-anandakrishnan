# 🤖 AI-Powered HR Assistant (Streamlit + Mistral via Ollama)

This project is an **AI-powered HR assistant** that lets you ask natural language questions about your employee dataset. It combines:
- 📊 **Pandas & Rule-based Parsing**
- 💡 **Local LLMs** using [Mistral 7B via Ollama](https://ollama.com/)
- ⚙️ **Streamlit** for a fast, interactive UI

You can upload your own CSV file and get instant answers — from headcount, join/exit filters, salary stats, to department-level breakdowns!

---

## 📺 Demo Video

🔗 **Watch on YouTube**: [https://youtu.be/ZDJxEy8Dvwk](https://youtu.be/ZDJxEy8Dvwk)

[![Watch the demo](Sample_demo/app_interface.png)](https://youtu.be/ZDJxEy8Dvwk)

---

## 📸 Screenshots

### ✅ Application Interface  
![App Interface](Sample_demo/app_interface.png)

---

## 🛠 Features

- 🔍 Upload any employee dataset (`.csv`)
- 💬 Ask natural language questions like:
  - “How many employees joined in 2024?”
  - “Show me average salary by department”
  - “Who exited in the last 6 months?”
- 📊 Get visual charts for trends like salary distribution, department counts, etc.
- ⚡ Works fully **offline** using **local LLMs** via [Ollama](https://ollama.com)

---

## 📁 Project Structure

├── app.py ← Main Streamlit app
├── data/
│ └── employee_data.csv ← Sample HR dataset
├── helpers/
│ ├── llm_handler.py ← LLM interface (Mistral via Ollama)
│ └── query_handler.py ← Rule-based query parser
├── Sample_demo/
│ ├── app_interface.png ← Screenshot of app
│ └── Sample_demo.mp4 ← Optional video demo (YouTube used instead)
├── requirements.txt
└── README.md


---

## 🚀 How to Run the Project Locally

### 1. Clone the Repo

```bash
git clone https://github.com/anandu91/hr-assistant-anandakrishnan.git
cd hr-assistant-anandakrishnan


2. Create and Activate Virtual Environment

python -m venv venv
.\venv\Scripts\activate    # For Windows
# Or:
# source venv/bin/activate  # For Mac/Linux

3. Install Dependencies

pip install -r requirements.txt

4. Start the Ollama Model

Make sure you have Ollama installed and pull the model:

ollama run mistral

💡 You can replace mistral with any compatible local LLM model.

5. Run the Streamlit App

streamlit run app.py

You will see a web interface open at http://localhost:8501 where you can upload a CSV and ask queries.

💼 Sample Dataset

Provided in data/employee_data.csv


