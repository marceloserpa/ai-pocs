import psycopg


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
    process_query("SELECT * FROM products;")    