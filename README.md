# 🤖 AI-Powered HR Assistant

*Built with Streamlit + Mistral via Ollama*

An intelligent HR dashboard that answers your **natural language questions** using a local [LLM](w) and your own employee data.

---

## 📺 Demo

🎥 **Watch it on YouTube**: [https://youtu.be/ZDJxEy8Dvwk](https://youtu.be/ZDJxEy8Dvwk)

---

## 🧠 What It Does

Ask questions like:

- “How many employees exited in 2023?”
- “Show me average salary by department.”
- “List departments with more than 5 employees.”
- “Who joined in 2023?”
- “How many employees joined in 2024?”
- “Show all employees who joined after January 2023.”

And get:

✅ Accurate answers\
📊 Auto-generated visual charts\
💡 All from a **local language model (LLM)** running fully offline

---

## ✨ Features

- 🔄 Upload any `.csv` employee dataset
- 🗣️ Ask natural language questions
- 📈 See instant charts (bar graphs, tables, etc.)
- ⚙️ Runs offline with [Mistral 7B](w) via [Ollama](https://ollama.com)
- 💻 Simple web UI powered by [Streamlit](w)

---

## 🖼 Interface Preview



---

## 🚀 Get Started Locally

Follow these quick steps to run it on your machine:

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/anandu91/hr-assistant-anandakrishnan.git
cd hr-assistant-anandakrishnan
```

---

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Start the Ollama Model (Mistral)

Ensure [Ollama](https://ollama.com) is installed and the **Mistral** model is available.

```bash
ollama run mistral
```

💡 *You can swap **`mistral`** with any other model supported by Ollama.*

---

### 5️⃣ Launch the Streamlit App

```bash
streamlit run app.py
```

🌐 The app will open at: [http://localhost:8501](http://localhost:8501)


---

## ⚙️ Assumptions and Simplifications Made

- The uploaded CSV must include the columns: `Name`, `Department`, `Join Date`, `Exit Date`, and `Salary`
- All dates are assumed to be in the format `YYYY-MM-DD`
- The assistant is optimized for HR-specific questions only (e.g., joiners, leavers, salary, department-wise analysis)
- Queries are handled using a combination of rule-based logic and a local LLM (Mistral via Ollama)
- Follow-up questions or multi-turn conversations are not supported
- Visual charts are generated for specific query types only
- The system is designed for use with mock/synthetic employee data — not real or sensitive information

---

---

## 📂 Sample Dataset

You can try it out using the provided sample CSV:

```
data/employee_data.csv
```
