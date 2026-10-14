# 📊 AI Data Analyst

An AI-powered data analysis web application built using Python, Streamlit, Pandas, and SQLite. It allows users to upload datasets, explore sales data through interactive charts, and ask questions in natural language to generate SQL queries.

## 🚀 Features

- **Dataset Upload:** Upload CSV and Excel files.
- **Interactive Dashboard:** View total sales, total quantity, and product counts.
- **Data Visualization:** Analyze sales by region, product, category, and date.
- **Filters:** Filter data by region and date range.
- **AI Text-to-SQL:** Convert natural-language questions into SQL queries using a Hugging Face language model.
- **SQL Query Execution:** Execute permitted read-only queries against the sales database.
- **Query History:** View previous questions and generated SQL.
- **Download Data:** Export filtered sales data and query history as CSV files.
- **Data Validation:** Detect missing values, invalid data types, negative values, and empty datasets.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib
- SQLite
- Transformers
- PyTorch
- Hugging Face

## 📁 Project Structure

```text
AI_Data_Analyst/
├── app.py
├── ai_sql.py
├── database.py
├── requirements.txt
├── sales.db
└── data/
    └── sales_data.csv
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/muneem12/AI_Data_Analyst.git
cd AI_Data_Analyst
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

## 🤖 AI Model

The application uses a Hugging Face text-to-SQL model to generate SQL queries from natural-language questions.

## 📌 Project Purpose

This project demonstrates practical applications of data analysis, SQL, machine learning-related tooling, interactive visualization, and AI-powered natural-language interfaces.

## 👨‍💻 Author

**Mohammed Abdul Muneem**