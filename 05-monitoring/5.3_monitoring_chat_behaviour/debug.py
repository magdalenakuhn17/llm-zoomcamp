import psycopg2


def list_databases_and_tables():
    try:
        # Connect to the PostgreSQL server
        connection = psycopg2.connect(
            dbname="postgres",  # Use the default 'postgres' database to connect
            user="admin",
            password="admin",
            host="localhost",
            port="5432"
        )
        connection.autocommit = True

        # Create a cursor object
        cursor = connection.cursor()

        # Execute the SQL query to list all databases
        cursor.execute(
            "SELECT datname FROM pg_database WHERE datistemplate = false;")

        # Fetch all results from the executed query
        databases = cursor.fetchall()

        # Print all databases and their tables
        for db in databases:
            db_name = db[0]
            print(f"Database: {db_name}")

            # Connect to each database
            db_connection = psycopg2.connect(
                dbname=db_name,
                user="admin",
                password="admin",
                host="localhost",
                port="5432"
            )
            db_cursor = db_connection.cursor()

            # Execute the SQL query to list all tables
            db_cursor.execute("""
                SELECT table_schema, table_name 
                FROM information_schema.tables
                WHERE table_schema NOT IN ('information_schema', 'pg_catalog');
            """)

            # Fetch all results from the executed query
            tables = db_cursor.fetchall()

            # Print all tables
            if tables:
                for table in tables:
                    print(f"  Schema: {table[0]}, Table: {table[1]}")
            else:
                print("  No tables found.")

            # Close the cursor and connection for the current database
            db_cursor.close()
            db_connection.close()

        # Close the main cursor and connection
        cursor.close()
        connection.close()

    except Exception as error:
        print(f"Error occurred: {error}")


if __name__ == "__main__":
    list_databases_and_tables()
