import psycopg2

conn = psycopg2.connect("dbname=funburger user=postgres password=thomas06 host=localhost")
cursor = conn.cursor()
sql_insert_query = "INSERT INTO orders (id, first_name, items, total_value, zipcode) VALUES (DEFAULT, %s, %s, %s, %s) RETURNING id;"


def add(first_name, items, total_value, zipcode):
    cursor.execute(sql_insert_query, (first_name, items, total_value, zipcode))
    conn.commit()
    cursor.close()        
    conn.close()
