
""" 
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run  

"""

import os

from flask import Flask
from flask import Flask,render_template,request
import pandas as pd
import numpy as np
from pretty_html_table import build_table

##df = pd.read_csv("tailorbird/d_analytics/data/processed/Cost Comparison_Kings Colony.csv", header=0)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/form')
    def form():
        global df 
        df = pd.read_csv("tailorbird/d_analytics/data/processed/Cost Comparison_DATA Kings Colony v2.csv", header=0)

        return render_template('form.html')

    # a simple page that says hello
    @app.route('/viewreports', methods = ['POST', 'GET'])
    def viewreports():

        if request.method == 'GET':
            return f"The URL /data is accessed directly. Try going to '/form' to submit form"
        
        if request.method == 'POST':
            form_data = request.form

            for key,value in form_data.items():
                if key == 'Rows':
                    if value == '':
                        index_f = ['Category', 'SubCategory', 'WorkType']
                    else:
                        index_f = [x.strip() for x in value.split(',')]
            
                if key == 'Columns':
                    if value == '':
                        columns_f = ['GC', 'FloorPlan', 'UnitName']
                    else:
                        columns_f = [x.strip() for x in value.split(',')]

                if key == 'Function':
                    if value == '':
                        agg_func_f = 'sum'
                        m_name = 'Totals'
                    else:
                        agg_func_f = np.mean
                        m_name = 'Average'



            #return render_template('data.html',form_data = form_data)
            x = pd.pivot_table(df, index=index_f, 
                        columns=columns_f, values='Avg_Price_Per_Unit', aggfunc=agg_func_f,
                        margins=True, margins_name=m_name)
            ##return(x.to_html())
            ##return(build_table(x, 'blue_light'))
            s = x.style.format(precision=0, na_rep='MISS')

            #s = s.set_properties(**{'background-color': 'black',                                                   
            #                        'color': 'lawngreen'                   
            #                        })


            cell_hover = {  # for row hover use <tr> instead of <td>
                'selector': 'td:hover',
                'props': [('background-color', '#0000EE')]
            }
            index_names = {
                'selector': '.index_name',
                'props': [('background-color', '#B8FF33')]
            }
            headers = {
                'selector': 'th:not(.index_name)',
                'props': [('background-color', '#FFC300')]
            }
            s.set_table_styles([cell_hover, index_names, headers])

            s.set_table_styles([
                    {'selector': 'th.col_heading', 'props': 'text-align: center;'},
                    {'selector': 'th.col_heading.level0', 'props': 'font-size: 1.5em;'},
                    {'selector': 'td', 'props': 'text-align: center; font-weight: bold;'},
                    {'selector': '.index_name', 'props': 'text-align: right;'},
                    {'selector': 'th', 'props': 'border-left: None'},
                    {'selector': 'td', 'props': 'border-left: None'},
                    {'selector': 'td', 'props': 'border-collapse: collapse'},
                    {'selector': 'td', 'props': 'border-color: None'},
                    {'selector': 'td', 'props': 'background-color: black'},
                    {'selector': 'td', 'props': 'color: lawngreen'}
                ], overwrite=False)

            return(s.render())

    return app
