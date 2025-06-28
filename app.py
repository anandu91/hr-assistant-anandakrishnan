import streamlit as st
import pandas as pd
from helpers.llm_handler import handle_query
import matplotlib.pyplot as plt

# ---- PAGE SETUP ----
st.set_page_config(page_title="HR Assistant", layout="wide")

# ---- CUSTOM CSS STYLING ----
st.markdown("""
    <style>
        body {
            background-color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .center-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: white;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: white;
        }
        .sidebar .css-1d391kg {
            background-color: #f3f4f6 !important;
        }
        .css-1aumxhk {
            background-color: white !important;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            border-radius: 5px;
            padding: 0.5em 1em;
        }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown('<div class="center-title">🤖 HR Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask Anything About Your Employees</div>', unsafe_allow_html=True)
st.write("---")

# ---- SIDEBAR ----
st.sidebar.header("📁 Upload Section")
uploaded_file = st.sidebar.file_uploader("Upload your HR CSV file", type="csv", help="Drag and drop or browse CSV file")

# ---- MAIN LOGIC ----
if uploaded_file:
    # Load dataset
    df = pd.read_csv(uploaded_file, parse_dates=["Join Date", "Exit Date"], dayfirst=True)
    
    # ---- CSV Validation ----
    REQUIRED_COLUMNS = {"Name", "Department", "Join Date", "Exit Date", "Salary"}
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
        st.stop()
    
    st.success("✅ File uploaded successfully!")
    st.markdown("### 📄 Data Preview")
    st.dataframe(df)

    # Query input
    st.markdown("💬 *Ask a question* (e.g., 'Who joined in 2024?', 'What's average salary in Sales?')")
    query = st.text_input("")

    if query:
        st.info("⏳ Processing your query using rule-based logic or Mistral via Ollama...")
        try:
            response = handle_query(query, df)
            st.subheader("📊 Result:")
            st.write(response)

            # Save as result_df if it's a DataFrame
            if isinstance(response, pd.DataFrame):
                result_df = response

            
            # ---- Optional Visualization: Department-wise Chart ----
            if "employee count by department" in query or "departments with more than" in query or "top" in query:
                # Drop NaN values just in case and sort index for consistency
                dept_count = df["Department"].dropna().value_counts().sort_index()

                # Chart title
                st.subheader("📊 Employee Distribution Chart")

                # Create a wider and taller chart
                fig, ax = plt.subplots(figsize=(8, 4.5))

                # Plot bar chart directly using Series plot
                dept_count.plot(kind="bar", color="skyblue", edgecolor="black", ax=ax)

                # Axis labels and title
                ax.set_xlabel("Department", fontsize=10)
                ax.set_ylabel("Count", fontsize=10)
                ax.set_title("Employee Count by Department", fontsize=16)

                # Smaller tick labels for readability
                ax.tick_params(axis='x', labelsize=8)
                ax.tick_params(axis='y', labelsize=8)

                # Auto-layout to prevent clipping
                plt.tight_layout()

                # Display the plot in Streamlit
                st.pyplot(fig)

                # Optional separator
                st.markdown("---")
                

            # ---- Optional Export CSV Button ----
            if 'result_df' in locals():
                st.markdown("### 📁 Export Filtered Results")
                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name='filtered_results.csv',
                    mime='text/csv'
                )

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
else:
    st.warning("📌 Please upload a CSV file from the sidebar to begin.")
