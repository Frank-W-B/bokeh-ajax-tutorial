from flask import Flask, render_template, jsonify, request
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import AjaxDataSource, CustomJS


adapter = CustomJS(code="""
    const result = {x: [], y: []}
    const {points} = cb_data.response
    for (const [x, y] of points) {
        result.x.push(x)
        result.y.push(y)
    }
    return result
""")


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/dashboard/')
def show_dashboard():
    plots = []
    plots.append(make_ajax_plot())

    return render_template('dashboard.html', plots=plots)

#x = 0
x = [0]
y = [0]

@app.route('/data/', methods=['POST'])
def data():
    x.append(x[-1] + 1)
    y.append(2 ** x[-1])
    #print(f"x: {x}, y: {y}")
    return jsonify(points=list(zip(x,y)))

def make_ajax_plot(): 
    source = AjaxDataSource(data_url=request.url_root + 'data/',
                            polling_interval=1000, adapter=adapter)

    plot = figure(plot_height=150, sizing_mode='scale_width')
    plot.line('x', 'y', source=source, line_width=4)

    script, div = components(plot)
    return script, div
