import os, psycopg2

def rs_query(table_name, gene_string):
    rs_conn = psycopg2.connect(dbname = os.getenv('RS_DB'), 
                                user = os.getenv('RS_USER'), 
                                password = os.getenv('RS_PASSWORD'), 
                                host = os.getenv('RS_HOST'),
                                port = '5439')
    cur = rs_conn.cursor()
    sql_query = """ SELECT cancer_type, count(*)
                    FROM {}
                    WHERE {}
                    GROUP BY cancer_type
                    ORDER BY 2 desc
                    """.format(table_name, gene_string)
    cur.execute(sql_query)
    a = cur.fetchall()
    rs_conn.close()
    return a

