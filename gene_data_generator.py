# import packages
import os, boto3, re
from random import *

# environment variables
AWS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
s3 = boto3.resource('s3')
bucket_name = 'kiranpatel-insight-de'

# constants
num_lines = 738819  # produces 1GB of data
num_genes = 700     # number of genes correlated with cancers
num_files_start = 1
num_files_end = 500
cancer_type = ["adrenal gland",
                "bile duct",
                "bladder",
                "blood",
                "bone",
                "bone marrow",
                "brain",
                "breast",
                "cervix",
                "colorectal",
                "esophagus",
                "eye",
                "head and neck",
                "kidney",
                "liver",
                "lung",
                "lymph node",
                "nervous system",
                "ovary",
                "pancreas",
                "pleura",
                "prostate",
                "skin",
                "soft tissue",
                "stomach",
                "testis",
                "thymus",
                "thyroid",
                "uterus",
                "none"
                ]

# functions
def generate_gene_seq():
    gene_seq = ''
    for j in range(25):
        nc = bin(randint(0,268435455))[2:].zfill(28)
        if (j == 24):
            gene_seq = gene_seq + nc + "\n"
        else:
            gene_seq = gene_seq + nc
    gene_seq = re.sub(r'([0-1])(?!$)', r'\1,', gene_seq)
    return gene_seq

def generate_data_line(line_num, num_lines, file_num):
    id_write = str(line_num + (num_lines * file_num)).zfill(10)
    c = cancer_type[randint(0,29)]
    gene = generate_gene_seq()
    return (id_write + ',' + c + ',' + gene)

# main
# iterate number of files
for h in xrange(num_files_start, num_files_end):
    file_name = 'gene_data_' + str(h).zfill(4) + '.txt'
    file = open(file_name, 'w')
    # iterate number of lines in file
    for i in xrange(num_lines):
        file.write(generate_data_line(i, num_lines, h))
    file.close()
    s3.Object(bucket_name, file_name).upload_file(file_name)
    print(file_name + ' upload complete')
    os.remove(file_name)
    
print('Finished!')
