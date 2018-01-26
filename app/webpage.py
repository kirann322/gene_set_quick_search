from flask import request, render_template
from app import app
import redshift_query

@app.route('/')
@app.route('/index')
def index():
    return render_template('input_template.html')

@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['text']
	table_name = 'gene_data'
	a = redshift_query.rs_query(table_name, text)
	return render_template('output_template.html', sorted_data = a)

