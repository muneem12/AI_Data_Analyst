
#step1:add the dashboard

import streamlit as st
import pandas as pd

#step27:connect the ai to streamlit
from ai_sql import ask_data

st.title("📊 AI Data Analyst")

#ste39:add a query history feature
if "query_history" not in st.session_state:
    st.session_state.query_history = []

df = pd.read_csv("data/sales_data.csv")

#ste43:add the file uploader
uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")
        st.dataframe(df.head())

    except Exception as e:
        st.error(f"Error reading file: {e}")
        #step45:handle invalid uploaded files safely
        st.stop()

#step44:make the dashboard handle uloaded datasets safely

required_columns = [
    "Sales", "Quantity", "Product", "Region", "Date"
]

if all(col in df.columns for col in required_columns):

    #step47:handle empty datasets
    if df.empty:
        st.error("The uploaded dataset contains no data.")
        st.stop()

    #step48:check for missing values
    #step49:add a missing-values summary
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]

    #step52:handle missing values in required columns
    if df[required_columns].isnull().values.any():
        st.error(
            "Required sales columns contain missing values. "
            "Please fix the dataset and upload it again."
        )
        st.stop()

    if not missing_values.empty:
        st.warning("Dataset contains missing values.")
        st.write("Missing values in each column:")
        st.dataframe(missing_values)

        #step50:add a missing-value percentage
        missing_percentage = (
            df.isnull().sum() / len(df) * 100
        )

        missing_percentage = missing_percentage[
            missing_percentage > 0
        ]

        st.write("Missing value percentage:")
        st.dataframe(missing_percentage.round(2))

    else:
        st.success("No missing values found!")

    #step46:validate data types
    try:
        df["Date"] = pd.to_datetime(df["Date"], errors="raise")
        df["Sales"] = pd.to_numeric(df["Sales"], errors="raise")
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="raise")

    except (ValueError, TypeError) as e:
        st.error(f"Invalid data format: {e}")
        st.stop()

    #step53:check for invalid negative values
    if (df["Sales"] < 0).any() or (df["Quantity"] < 0).any():
        st.error("Sales and Quantity cannot contain negative values.")
        st.stop()

    st.success("Dataset contains all required sales columns.")

    #step4:add a region filter
    region = st.selectbox(
        "Select Region",
        ["ALL"] + sorted(df["Region"].unique().tolist())
    )

    #step6:add a date filter
    start_date = st.date_input(
        "Start Date",
        pd.to_datetime(df["Date"]).min()
    )

    end_date = st.date_input(
        "End Date",
        pd.to_datetime(df["Date"]).max()
    )

    #step7:make the date filter work
    df["Date"] = pd.to_datetime(df["Date"])

    df = df[
        (df["Date"].dt.date >= start_date) &
        (df["Date"].dt.date <= end_date)
    ]

    #step5:make the filter actually work
    if region != "ALL":
        df = df[df["Region"] == region]

    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    st.subheader("Sales Data")
    st.dataframe(df)

    #ste59:download filtered sales data
    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Sales Data",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )

    st.subheader("Basic Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"₹{df['Sales'].sum():,.0f}")
    col2.metric("Total Quantity", f"{df['Quantity'].sum():,}")
    col3.metric("Products", df["Product"].nunique())

    #step2:add sales by region
    #step3:add sales by product
    #step54:improve the dashboard with a sales trend chart
    #step57:improve the dashboard layout
    #(organize charts using tabs)

    tab1, tab2, tab3 = st.tabs([
        "Regional Analysis",
        "Product Analysis",
        "Sales Trends"
    ])

    with tab1:
        st.subheader("Sales by Region")
        region_sales = df.groupby("Region")["Sales"].sum()
        st.bar_chart(region_sales)

    with tab2:
        st.subheader("Sales by Product")
        product_sales = df.groupby("Product")["Sales"].sum()
        st.bar_chart(product_sales)

    with tab3:
        st.subheader("Sales Trend Over Time")
        daily_sales = df.groupby("Date")["Sales"].sum()
        st.line_chart(daily_sales)

    #step58:add a sales summary by category
    if "Category" in df.columns:
        st.subheader("Sales by Category")
        category_sales = df.groupby("Category")["Sales"].sum()
        st.bar_chart(category_sales)

    #step8:add an ai-style question box
    st.subheader("🤖 Ask Your Data")

    question = st.text_input(
        "Ask a question about the sales data:"
    )

    #sstep28:replace the old keyword-based ai
    if question:
        sql, result = ask_data(question)

        #step40:save each question and its generated SQL
        #step41:improve query history
        if not st.session_state.query_history or (
            st.session_state.query_history[-1]["Question"] != question
        ):
            st.session_state.query_history.append({
                "Question": question,
                "SQL": sql
            })

        st.write("Generated SQL:")
        st.code(sql, language="sql")

        st.write("Answer:")

        if isinstance(result, str):
            st.error(result)

            if result.startswith("SQL Error:"):
                st.info(
                    "Try rephrasing your question or asking about "
                    "the available sales columns."
                )

        else:
            result_df = pd.DataFrame(
                result["rows"],
                columns=result["columns"]
            )

            if result_df.shape == (1, 1):
                value = result_df.iloc[0, 0]

                #step61:improve answer display
                answer_label = result_df.columns[0]

                #step70:improve the result label
                friendly_labels = {
                    "SUM(Quantity)": "Total Quantity",
                    "SUM(Sales)": "Total Sales",
                    "AVG(Sales)": "Average Sales",
                    "MAX(Sales)": "Highest Sale",
                    "MIN(Sales)": "Lowest Sale"
                }

                answer_label = friendly_labels.get(
                    answer_label,
                    answer_label
                )

                st.metric(
                    answer_label,
                    f"{value:,.2f}"
                )

            elif result_df.shape == (1, 2):
                first = result_df.iloc[0, 0]
                second = result_df.iloc[0, 1]

                if isinstance(second, (int, float)) or hasattr(second, "item"):
                    second = second.item() if hasattr(second, "item") else second
                    st.success(f"{first} — ₹{second:,.2f}")
                else:
                    st.success(f"{first} — {second}")

            else:
                for col in result_df.columns:
                    if col.lower() in [
                        "sales", "totalsales", "averagesales"
                    ]:
                        result_df[col] = result_df[col].map(
                            lambda x: (
                                f"{x:,.2f}"
                                if isinstance(x, (int, float))
                                else x
                            )
                        )

                st.dataframe(result_df, use_container_width=True)

    #step42:improve the user experience
    st.subheader("🕘 Query History")

    if st.button("Clear History"):
        st.session_state.query_history = []
        st.rerun()

    if st.session_state.query_history:
        history_df = pd.DataFrame(
            st.session_state.query_history
        )

        csv = history_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Query History",
            data=csv,
            file_name="query_history.csv",
            mime="text/csv"
        )

        for item in reversed(st.session_state.query_history):
            with st.expander(item["Question"]):
                st.code(item["SQL"], language="sql")

    else:
        st.info("No questions asked yet.")

else:
    st.warning(
        "This dashboard requires Sales, Quantity, Product, Region, and Date columns."
    )
    st.dataframe(df.head())




# Old keyword-based AI code remains commented out.



#"""if question:
    #q = question.lower()

    #if "total sales" in q:
       # st.write(f"Total Sales: ₹{df['Sales'].sum():,.0f}")

    #elif "total quantity" in q:
        #st.write(f"Total Quantity: {df['Quantity'].sum():,}")

    #elif "most" in q and "product" in q:
     #   best_product = df.groupby("Product")["Sales"].sum().idxmax()
    #    st.write(f"Top Product: {best_product}")

    #elif "average" in q and "sales" in q:
    #    avg_sales = df["Sales"].mean()
    #    st.write(f"Average Sales: ₹{avg_sales:,.2f}")

    #elif "highest" in q or"maximum" in q:
     #   st.write(f"Highest Sale: ₹{df['Sales'].max():,.0f}")

    #elif "lowest" in q or "minimum" in q:
    #    st.write(f"Lowest Sale: ₹{df['Sales'].min():,.0f}")

    #else:
   #     st.write("Sorry, I don't understand that question yet.")"""