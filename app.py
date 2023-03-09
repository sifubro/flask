from flask import Flask, Response, redirect, url_for, render_template, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from scatterplots.scatterplot_blueprint import scatterplot

import io
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go


app = Flask(__name__)
app.register_blueprint(scatterplot, url_prefix="/scatterplot")

# flask run
# flask --app app.py  --debug run

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

df = pd.DataFrame()
df["x"] = x
df["y"] = y
#df = pd.read_csv("")

home_link = '''<p> </p> <p> </p> <a href="/"> Click to return to Homepage</a> '''

index = '''<p> Click the links below to view tables and scatterplots: </p>
<ul>
    <li><a href="/table">LoA MetafasV4 </a> </li>
    <li><a href="/scatterplot/scatter_matplotlib">Scatterplot matplotlib</a>  </li>
    <li><a href="/scatterplot/scatter_plotly">Scatterplot Plotly </a>  </li>
</ul>'''

@app.route('/')
def home():
    return render_template("index.html", content=df) + index


@app.route('/table')
def display_table():
    # Code to create and return a Pandas dataframe as an HTML table
    #return temp_df.to_html() + home_link
    
    data = {
            'name': ['Alice', 'Bob', 'Charlie', 'David'],
            'age': [25, 32, 18, 47],
            'city': ['New York', 'Paris', 'London', 'Tokyo']
        }

    df = pd.DataFrame(data)
    
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    canvas = FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    plt.close(fig)

    # Return the PNG image as binary data in the Flask response
    return Response(png_output.getvalue(), mimetype='image/png')




if __name__ == "__main__":
    app.run(debug=True)