import os, psycopg2

aws_region = os.getenv('AWS_DEFAULT_REGION')
table_name = 'gene_data'
role_arn = os.getenv('RS_ARN')

s3_bucket_address = 's3://kiranpatel-insight-de/gene_data_'
num_file_start = 1
num_file_end = 500

rs_conn = psycopg2.connect(dbname = os.getenv('RS_DB'), 
                            user = os.getenv('RS_USER'), 
                            password = os.getenv('RS_PASSWORD'), 
                            host = os.getenv('RS_HOST'),
                            port = '5439')

rs_conn.set_session(autocommit=True)

cur = rs_conn.cursor()

for i in xrange(num_file_start,num_file_end):
    s3_file_address = s3_bucket_address + str(i).zfill(4) + '.txt'

    sql_loading = """COPY {} FROM '{}' \
                    credentials 'aws_iam_role={}' \
                    delimiter ',' region '{}' """ \
                    .format(table_name, s3_file_address, role_arn, aws_region)

    cur.execute(sql_loading)
    print(s3_file_address + ' uploaded!')

rs_conn.close()
