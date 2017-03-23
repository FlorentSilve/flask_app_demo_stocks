from flask import Flask, render_template, request, redirect
import datetime
import requests
import pandas as pd
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import os

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        stock = request.form['stock']
        feature = request.form['features']
        err = ''
        if not stock:
            err = 'Error: Please choose a stock'
        if err:
            return render_template('index.html', errormessage=err+'<br>')

        start_date = datetime.datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.datetime.now() - datetime.timedelta(days=31)).strftime('%Y-%m-%d')

        url = 'https://www.quandl.com/api/v3/datasets/WIKI/'+stock.upper()+'/data.csv?api_key=xwHMQV1h7w9Pimp2_9vR'+ \
            '&start_date='+end_date+'&end_date='+start_date+'&qopts.columns=1,2,3,4,date'

        r = requests.get(url)
        if r.status_code != 200:
            err = 'Could not find the stock "'+stock.upper()+'"'
            return render_template('index.html',errormessage=err+'<br>')

        df = pd.read_csv(StringIO(r.text))
        x = pd.to_datetime(df['Date'])
        y = df[feature]

        p = figure(x_axis_type='datetime', title=feature)
        p.line(x, y, color='navy')
        p.circle(x, y, size=4, color='navy', alpha=0.8)
        p.legend.location = 'top_left'

        p.grid.grid_line_alpha = 0
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Price'
        p.ygrid.band_fill_color = "olive"
        p.ygrid.band_fill_alpha = 0.1

    script, div = components(p, INLINE)
    title = 'Data for '+stock.upper() +' stock'
    html_page = render_template('page2.html', title=title, figurescript=script, figurediv=div)
    return encode_utf8(html_page)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port)