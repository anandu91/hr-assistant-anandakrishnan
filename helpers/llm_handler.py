import pandas as pd
from datetime import datetime, timedelta
from ollama import Client
from helpers.query_handler import handle_rule_based_query

def handle_query(query, df):
    # Try rule-based logic first
    rule_response = handle_rule_based_query(query, df)
    if rule_response is not None:
        return rule_response

    # Step 1: Pre-process the data — remove rows with missing Exit Dates for resignation-based accuracy
    df["Exit Date"] = pd.to_datetime(df["Exit Date"], errors="coerce")
    filtered_df = df[df["Exit Date"].notna()]  # Only include rows where Exit Date exists

    # Limit to 40 rows for LLM input
    csv_data = filtered_df.head(40).to_csv(index=False)

    # Step 2: Dynamically calculate today and last 12-month start
    today = datetime.today().date()
    last_12_months_start = today - timedelta(days=365)
    today_str = today.strftime("%d-%m-%Y")
    last_12_months_str = last_12_months_start.strftime("%d-%m-%Y")

    # Step 3: Updated and strict prompt
    prompt = f"""
You are an intelligent HR data assistant designed to analyze structured employee CSV files and answer questions strictly based on valid logic with 100% accuracy.

The uploaded CSV contains the following columns:
- Name
- Department
- Join Date
- Exit Date
- Salary

Your instructions:
1. Analyze the data row by row using proper date and value comparisons.
2. Only include employees in the result if they strictly match the logic required by the user's question.
3. Never guess or include incorrect entries.
4. If data is missing or the answer cannot be determined, respond clearly with: "This information is not available in the uploaded data."
5. Do not repeat incorrect results and apologize — instead, provide only correct and clean answers.
6. Do not summarize — list exact employee names, dates, departments, and salaries when required.

✅ Rules to follow:
1. Use today's date as {today_str}.
2. An employee is considered **active** if their Exit Date is blank or empty.
3. An employee is considered **resigned** only if Exit Date is a valid date.
4. For time-based questions like "last 12 months", include only those with Exit Dates between {last_12_months_str} and {today_str}.
5. For year-based questions like "resigned in 2023", include only if Exit Date is in 2023.
6. For questions like “last 365 days”, use exact 1-year logic from {today_str} backwards.
7. Never include employees with blank Exit Dates when asked about resignations or exits.
8. List names, departments, dates, and salaries clearly if the query asks for employee details.
9. If the query can’t be answered due to missing Exit Dates, say: "Some records do not have Exit Dates and are considered active."

📌 Example Clarification:
- If "Chloe Lee" has Exit Date = (empty), she should NOT be included in a "who resigned" question.
- If "John Smith" has Exit Date = "2024-12-01" and today is {today_str}, include him (because it's within the last 365 days).

Here is the full CSV dataset (maximum 40 rows):

{csv_data}

User's Question:
{query}

Now, give the final answer using only the data above. Ensure logical accuracy. Provide the result in clean plain text.
"""

    # Step 4: Send to LLM
    try:
        client = Client(host='http://localhost:11434')
        response = client.chat(
            model="mistral:7b-instruct",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()

    except Exception as e:
        return f"⚠️ Ollama Error: {e}"
