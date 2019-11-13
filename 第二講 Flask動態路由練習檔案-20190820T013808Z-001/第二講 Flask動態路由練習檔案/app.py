from flask import Flask, render_template, Response
from urllib.parse import quote
import csv
from stock import Stock

app = Flask(__name__)

# 站內要顯示的個股列表
stocks = []

# 打開stock_list.csv
with open('stock_list.csv', newline='', encoding='utf-8') as stock_csv:
    # 把csv檔案格式轉換為list
    temp = list(csv.reader(stock_csv))
    stocklist = []
    for stock in temp:
        stocklist.append({
        'id': stock[0],
        'name': stock[1]
        })
    print(stocklist)

# 首頁路由
@app.route('/')
def index_page():
    return render_template('index.html',stocklist=stocklist,web_title="首頁")

# 個股詳情頁路由 多重路由
@app.route('/stock/<sid>')
def stock_page(sid):
    stock = Stock(sid)
    stock.fetch_data()
    return render_template('stock.html',stock=stock,web_title=stock.name)

# 比較圖表路由
@app.route('/chart')
def chart_page():
    name_list = []
    price_list = []
    color_list = []

    #把所有個股清單取出

    for s in stocklist:
        # 產生一個個股的物件實例
        stock = Stock(s['id'])

        # 爬取這個個股的資料
        stock.fetch_data()
        # 整理出個股名稱與價格的清單
        name_list.append(stock.name)
        price_list.append(float(stock.price))

        #如果交易價格大於100 放藍色
        # 紅 'rgba(255, 99, 132, 0.2)',
        # 藍 'rgba(54, 162, 235, 0.2)',

        if float(stock.price) > 100:
            color_list.append('rgba(54, 462, 235 , 0.2)')
        else:
            color_list.append('rgba(255, 99, 132, 0.2)')
            
    return render_template('chart.html',name_list=name_list,price_list=price_list,color_list=color_list)
    # 如果要傳入字串的話要這樣做 color_list = str(color_list.replace("'"),"")
    # 在 傳入javascript 的時候 使用json.parse 的格式時要用雙引號傳入 因為在json的格式是只能用雙引號

if __name__ == '__main__':
    app.run(debug=True)
