from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go

scatterplot = Blueprint("scatterplot_blueprint", __name__, static_folder="static", template_folder="template")


x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

df = pd.DataFrame()
df["x"] = x
df["y"] = y
#df = pd.read_csv("")

@scatterplot.route('/scatter_matplotlib')
def display_scatterplot():
    # Code to create and return a scatterplot using Matplotlib or Plotly

    fig, ax = plt.subplots()
    plt.scatter(df["x"], df["y"])
    
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Scatterplot")
    
    #ax.axis('off')
    #ax.axis('tight')
    #ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    # Method 1
    # canvas = FigureCanvas(fig)
    # png_output = io.BytesIO()
    # canvas.print_png(png_output)
    # plt.close(fig)
    # #Return the PNG image as binary data in the Flask response
    # return Response(png_output.getvalue(), mimetype='image/png')

    # Method 2
    # # Save plot to a PNG image in memory
    # img = io.BytesIO()
    # fig.savefig(img, format='png')
    # img.seek(0)
    # # Return image in HTTP response
    # response = make_response(img.getvalue())
    # response.headers['Content-Type'] = 'image/png'
    # return  response #render_template("index.html", image = img)

    # Method 3
    plt.savefig('./static/images/scatterplot.png')
    #'''<p><img src="./static/images/scatterplot.png" alt="Scatterplot"> </p>'''


    return  render_template("scatter.html") 



@scatterplot.route('/scatter_plotly')
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