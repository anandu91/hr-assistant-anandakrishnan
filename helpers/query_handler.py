import pandas as pd
import re
from datetime import datetime, timedelta
from dateutil.parser import parse

def handle_rule_based_query(query, df):
    query = query.lower()

    try:
        # --- Average Salary by Department or Overall ---
        avg_salary_match = re.search(r"average salary(?: in ([a-zA-Z ]+))?", query)
        if avg_salary_match:
            dept = avg_salary_match.group(1)
            if dept:
                dept = dept.capitalize()
                filtered = df[(df["Department"].str.lower() == dept.lower()) & (df["Salary"].notna())]
                if not filtered.empty:
                    avg_salary = round(filtered["Salary"].mean(), 2)
                    return f"The average salary in {dept} is ₹{avg_salary:,.2f}."
                else:
                    return f"No salary data found for {dept} department."
            else:
                avg_salary = round(df["Salary"].mean(), 2)
                return f"The overall average salary is ₹{avg_salary:,.2f}."

        # --- Employees Who Joined Before a Specific Date ---
        joined_before_match = re.search(r"joined before (.+)", query)
        if joined_before_match:
            date_str = joined_before_match.group(1).strip(" ?“”\"'")
            try:
                date = parse(date_str, fuzzy=True, dayfirst=True)
                filtered = df[df["Join Date"] < date]
                if filtered.empty:
                    return f"No employees joined before {date.date()}."
                else:
                    result = "\n".join([
                        f"- {row['Name']} (joined on {row['Join Date'].date()})"
                        for _, row in filtered.iterrows()
                    ])
                    return f"Based on the provided CSV data, the employees who joined before {date.strftime('%B %Y')} are:\n\n{result}"
            except Exception as e:
                return f"⚠️ Date parsing error: {str(e)}"

        # --- Employees Who Joined Between Two Dates ---
        between_match = re.search(r"joined between (.+?) and (.+)", query)
        if between_match:
            start_str = between_match.group(1).strip(" ?“”\"'")
            end_str = between_match.group(2).strip(" ?“”\"'")
            try:
                start_date = parse(start_str, fuzzy=True, dayfirst=True)
                end_date = parse(end_str, fuzzy=True, dayfirst=True)
                filtered = df[(df["Join Date"] >= start_date) & (df["Join Date"] <= end_date)]
                if filtered.empty:
                    return f"No employees joined between {start_date.date()} and {end_date.date()}."
                else:
                    result = "\n".join([
                        f"{i+1}. {row['Name']} ({row['Department']}), hired on: {row['Join Date'].date()}"
                        for i, row in filtered.iterrows()
                    ])
                    return f"Here are the employees who joined between {start_date.strftime('%B %Y')} and {end_date.strftime('%B %Y')}:\n\n{result}"
            except Exception as e:
                return f"⚠️ Date parsing error: {str(e)}"

        # --- Employees Who Joined After a Specific Date ---
        joined_after_match = re.search(r"joined after (.+)", query)
        if joined_after_match:
            date_str = joined_after_match.group(1).strip(" ?“”\"'")
            try:
                date = parse(date_str, fuzzy=True, dayfirst=True)
                filtered = df[df["Join Date"] > date]
                if filtered.empty:
                    return f"No employees joined after {date.date()}."
                else:
                    result = "\n".join([
                        f"- {row['Name']} (joined on {row['Join Date'].date()})"
                        for _, row in filtered.iterrows()
                    ])
                    return f"According to the CSV data, the following employees joined after {date.date()}:\n\n{result}"
            except Exception as e:
                return f"⚠️ Date parsing error: {str(e)}"

        # --- Employees Joined in a Specific Year ---
        joined_in_match = re.search(r"joined in (\d{4})", query)
        if joined_in_match:
            year = int(joined_in_match.group(1))
            filtered = df[df["Join Date"].dt.year == year]
            if filtered.empty:
                return f"No employees joined in {year}."
            else:
                result = "\n".join([
                    f"- {row['Name']} (joined on {row['Join Date'].date()})"
                    for _, row in filtered.iterrows()
                ])
                return f"According to the CSV data, the following employees joined in {year}:\n\n{result}"

        # --- Employees Who Exited in the Last 12 Months ---
        if any(phrase in query for phrase in [
            "employees exited in the last 12 months",
            "employees left in the last 12 months",
            "who exited in the past year",
            "who exited during the past year",
            "employees who exited in the last year",
            "who left in the last 12 months",
            "employees resigned in the last 365 days",
            "resigned in the last 365 days" 
        ]):
            today = datetime.today()
            one_year_ago = today - timedelta(days=365)
            filtered = df[(df["Exit Date"].notna()) & (df["Exit Date"] >= one_year_ago) & (df["Exit Date"] <= today)]

            if filtered.empty:
                return "No employees exited in the past 12 months."

            result = "\n".join([
                f"{i+1}. {row['Name']} - {row['Department']} - {row['Exit Date'].date()} - {int(row['Salary'])}"
                for i, row in filtered.iterrows()
            ])
            return f"Here are the employees who exited in the last 12 months (from {one_year_ago.date()} to {today.date()}):\n\n{result}"

        # --- Still Active Employees Count ---
        if "how many employees" in query and ("currently active" in query or "still active" in query):
            active = df[df["Exit Date"].isna()]
            return f"There are {len(active)} employees currently active."

        # --- List Active Employees by Name ---
        elif (
            "list all active employees" in query or
            "list of active employees" in query or
            "who are the active employees" in query or
            "show active employees" in query
        ):
            active = df[df["Exit Date"].isna()]
            if active.empty:
                return "There are no currently active employees."
            names = "\n".join([f"{i+1}. {row['Name']}" for i, row in active.iterrows()])
            return f"Here is the list of {len(active)} active employees:\n\n{names}"

        # --- Count by Department ---
        if "employee count by department" in query or "count by department" in query:
            result_df = df["Department"].value_counts().reset_index()
            result_df.columns = ["Department", "Employee Count"]
            return result_df

        # --- Employees Exited in a Specific Year ---
        if "how many employees left in" in query or "how many employees exited in" in query:
            match = re.search(r"(\d{4})", query)
            if match:
                year = int(match.group(1))
                exited = df[(df["Exit Date"].notna()) & (df["Exit Date"].dt.year == year)]
                return f"{len(exited)} employees exited in {year}."
            else:
                return "⚠️ Couldn't identify the year."

        # --- Departments with More Than N Employees ---
        match = re.search(r"departments with more than (\d+)", query)
        if match:
            threshold = int(match.group(1))
            counts = df["Department"].value_counts()
            filtered = counts[counts > threshold].reset_index()
            filtered.columns = ["Department", "Employee Count"]
            return filtered

        # --- Top N Departments by Count ---
        match = re.search(r"top (\d+) departments", query)
        if match:
            top_n = int(match.group(1))
            top_departments = df["Department"].value_counts().head(top_n).reset_index()
            top_departments.columns = ["Department", "Employee Count"]
            return top_departments

        return None  # Let LLM handle unknown queries

    except Exception as e:
        return f"⚠️ Rule-based error: {str(e)}"
