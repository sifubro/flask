from flask import Flask, Response, redirect, url_for, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import io
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go


app = Flask(__name__)

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
    <li><a href="/scatterplot">Scatterplot </a>  </li>
    <li><a href="/scatterplot_plotly">Scatterplot Plotly </a>  </li>
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


@app.route('/scatterplot')
def display_scatterplot():
    # Code to create and return a scatterplot using Matplotlib or Plotly

    fig, ax = plt.subplots()
    plt.scatter(df["x"], df["y"])
    
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    
    #ax.axis('off')
    #ax.axis('tight')
    #ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    canvas = FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    plt.close(fig)

    # Return the PNG image as binary data in the Flask response
    return Response(png_output.getvalue(), mimetype='image/png')
    
    
@app.route('/scatterplot_plotly')
def display_scatterplot_plotly():
    trace = go.Scatter(
        x=x,
        y=y,
        mode='markers'
    )

    layout = go.Layout(
        title='Scatterplot by Plotly',
        xaxis=dict(title='X-axis'),
        yaxis=dict(title='Y-axis')
    )

    fig = go.Figure(data=[trace], layout=layout)

    # Return the HTML code for the scatterplot with the home link
    return render_template("index.html") + fig.to_html(full_html=False)



if __name__ == "__main__":
    app.run(debug=True)