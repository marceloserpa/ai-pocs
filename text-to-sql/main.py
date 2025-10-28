import sys
import psycopg
from ollama import Client

def process_query(query):
    conn_info = {
        "dbname": "text2sql-poc",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": 5442
    }

    try:
        with psycopg.connect(**conn_info) as conn:

            with conn.cursor() as cur:
                cur.execute(query)

                items = cur.fetchall()

                # Print the results
                print("=== Product List ===")
                for item in items:
                    print(item)

    except psycopg.Error as e:
        print("Database error:", e)


if __name__ == "__main__":
    client = Client(host='http://localhost:11434')

    system_prompt = """
    Given an input question, create a syntactically correct PostgreSQL query to
    run to help find the answer. 

    Never query for all the columns from a specific table, only ask for a the
    few relevant columns given the question.

    Pay attention to use only the column names that you can see in the schema
    description. Be careful to not query for columns that do not exist. Also,
    pay attention to which column is in which table.

    Only Query are allowed. INSERT, DELETE or UPDATE instruction MUST return the error message 'operation NOT allowed'.

    You MUST return only the query, anything more will be wrong.

    Only use the following tables:

    -- Customers table
    CREATE TABLE customers (
        customer_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Products table
    CREATE TABLE products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        price NUMERIC(10,2) NOT NULL,
        stock INT NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Sales table
    CREATE TABLE sales (
        sale_id SERIAL PRIMARY KEY,
        customer_id INT NOT NULL REFERENCES customers(customer_id),
        product_id INT NOT NULL REFERENCES products(product_id),
        quantity INT NOT NULL CHECK (quantity > 0),
        total NUMERIC(10,2) NOT NULL,
        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    user_prompt = sys.argv[1]

    response = client.chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    query = response["message"]["content"]

    result = process_query(query)

    print(result)