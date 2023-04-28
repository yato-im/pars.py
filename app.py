from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        num_items = request.form['num_items']
        if url and num_items:
            url = url.strip()
            num_items = int(num_items)
            try:
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                products = soup.select('div.goods-tile__inner')
                results = []
                for i in range(num_items):
                    try:
                        name = products[i].select_one('span.goods-tile__title').text.strip()
                    except:
                        name = 'N/A'
                    try:
                        price = products[i].select_one('span.goods-tile__price-value').text.strip()
                    except:
                        price = 'N/A'
                    results.append({'name': name, 'price': price})
                return render_template('result.html', results=results)
            except:
                return render_template('error.html')
        else:
            return render_template('error.html')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
