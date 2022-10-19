
# https://www.psycopg.org/docs/usage.html


import psycopg2



try:
    conn = psycopg2.connect("dbname=postgres user=postgres port=5432 password=AAAaaa123")
    
except psycopg2.Error as e:
    print("Unable to connect!", e.pgerror, e.diag.message_detail)
    
else:
    print("Connected!")
    
    cur = conn.cursor()
    
    
    cur.execute("SELECT * FROM klustr.available_datasets();")
    print(cur.description)

    value = cur.fetchone()
    print(f'one > {value}')


    for i, emp in enumerate(cur):
        print(f'{i:03} | {emp}')
        
    conn.close()

pass