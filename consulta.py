"""Main script."""
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, String, DateTime
import pandas as pd
from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args

db_URI = engine = 'mysql+pymysql://usuariosfiec:Pll%V!o4J.L3@localhost/cienciadedados'
db_schema = environ.get('SQLALCHEMY_DB_SCHEMA')
engine = create_engine(db_URI)

df = pd.read_csv('data/teste.csv')
data = df.to_dict(orient = 'records')

app = Flask(__name__)
app.debug = True

def get_dataframe_from_sql(table_name):
    """Create DataFrame form SQL table."""
    sql_DF = pd.read_sql_table(table_name,
                               con=engine,
                               parse_dates=['posting_date', 'posting_updated'],
                               chunksize=100)
    return sql_DF

#
# df = pandas.read_csv('files/teste.csv')
# data = df.to_dict(orient = 'records')

def get_users(offset=0, per_page=20):

    return data[offset: offset + per_page]


for chunk in pd.read_sql_query(sql_str, engine, chunksize=10):
    do_something_with(chunk)
print(get_dataframe_from_sql('nyc_jobs'))



@app.route('/')
def index():

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    total = len(data)

    pagination_users = get_users(offset=offset, per_page=per_page)

    pagination = Pagination(page=page,
                            per_page=per_page,
                            total=total,
                            css_framework='bootstrap4')

    return render_template('index.html',
                           data=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)
# na execução de python app.py
if __name__ == "__main__":
    # execute o aplicativo Flask
    app.run(debug=True)