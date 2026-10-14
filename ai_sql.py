#step14:give the ai the database schema

SCHEMA = """
Table: sales

Columns:
Date TEXT
Product TEXT
Category TEXT
Region TEXT
Quantity INTEGER
Price INTEGER
Sales INTEGER
"""

#step15:load the AI model
from transformers import AutoTokenizer, AutoModelForCausalLM
MODEL_NAME = "yuashi/qwen2.5-1.5b-text2sql-merged"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)


#step16:create the prompt for the sql model
def generate_sql(question):
    prompt = f"""
You are a SQLite SQL generator.

Database schema:
{SCHEMA}

Your task is to convert the user's question into ONE correct SQL query.

STRICT RULES:
1. Use only the table: sales
2. Use only the columns in the schema.
3. For "total sales", use exactly:
   SELECT SUM(Sales) FROM sales;
4. Do not add GROUP BY unless the user asks to group by something.
5. Do not add ORDER BY unless the user asks for sorting.
6. Do not add LIMIT unless the user asks for a limited number of results.
7. Do not calculate or answer the question yourself.
8. Return ONLY the SQL query.
9. Do not return explanations.
10. Use HAVING to filter aggregated results, such as SUM, AVG, or COUNT.
11. Use WHERE to filter individual rows before grouping.
12. Do not return markdown or ```.

Examples:

Question: What is the total sales?
SQL: SELECT SUM(Sales) FROM sales;

Question: What is the total quantity?
SQL: SELECT SUM(Quantity) FROM sales;

Question: Which product has the highest sales?
SQL: SELECT Product, SUM(Sales) AS TotalSales FROM sales GROUP BY Product ORDER BY TotalSales DESC LIMIT 1;

User question:
{question}

SQL:
"""

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=False
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    result = result.split("SQL:")[-1].strip()

    return result


#step17:test the SQL generator
"""question = "What is the total sales?"
sql = generate_sql(question)
print(sql)"""

#step21:add SQL safety validation,#step32,38:strengthen SQL validation
def validate_sql(sql):
    sql = sql.strip().upper()

    if not sql:
        return False
    #Allow only one SELECT statement
    if not sql.upper().startswith("SELECT"):
        return False
    #reject multile SQL statements
    if ";" in sql.rstrip(";"):
        return False
    #allo queries only on the sales table
    if "FROM SALES" not in sql.upper():
        return False
    #Block SQL Commments
    if "--" in sql or "/*" in sql or "*/" in sql:
        return False

    forbidden = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "ATTACH",
        "DETACH",
        "PRAGMA",
        "REPLACE",
        "TRUNCATE"
    ]

    upper_sql = sql.upper()
    for word in forbidden:
        if word in upper_sql:
            return False

        
    return True

#step18:execute the generated SQL,#step22:connect the validator to sql execution,#step31:add error handling to sql execution

import sqlite3

def execute_sql(sql):
    if not validate_sql(sql):
        return "Unsafe SQL query blocked."
    try:
        #Step 39: Enable read-only database access
        conn = sqlite3.connect("file:sales.db?mode=ro", uri=True)
        #ste37:improve the table columns names
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        conn.close()
        return {
            "columns": columns,
            "rows": rows
        }
        
    except sqlite3.Error as e:
        return f"SQL Error: {e}" 


#step19:connect the two parts

def ask_data(question):
    sql = generate_sql(question)

    result = execute_sql(sql)

    return sql, result

#step20:test the complete pipeline,#step25:test the complete ai+safety+database pipeline,step28:clean u ai_sql
"""if __name__ == "__main__":"""
question = "Which product has the highest total sales?"
sql, result = ask_data(question)
print("Question:", question)
print("SQL:", sql)
print("Result:", result)

print(execute_sql("SELECT UnknownColumn FROM sales"))

#step23:test the safety validator(temporary use)
sql = "SELECT SUM(Sales) FROM sales;"
result = execute_sql(sql)
print(result)
#step24:test that unsafe SQL is blocked
"""sql = "DELETE FROM sales;"
result = execute_sql(sql)
print(result)"""



