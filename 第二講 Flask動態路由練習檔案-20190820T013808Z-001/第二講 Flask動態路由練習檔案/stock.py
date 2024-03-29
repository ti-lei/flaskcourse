from urllib.request import urlopen
from pyquery import PyQuery

class Stock:
    # 個股包含以下屬性 
    # 個股代號、名稱、成交價、買價、賣價
    def __init__(self, sid):
        self.id = sid
        self.name = None
        self.price = None
        self.bid = None
        self.offer = None

    # 定義爬取個股資訊的函式
    # 爬取目標:https://tw.stock.yahoo.com/q/q?s=2330
    def fetch_data(self):
        # 爬取整個目標網頁
        page = urlopen('https://tw.stock.yahoo.com/q/q?s=' + self.id)
        print('https://tw.stock.yahoo.com/q/q?s=' + self.id)
        # 使用big5解碼
        raw_html = page.read().decode('big5')
        # 定義整個網頁
        html = PyQuery(raw_html)
        # 篩選標籤是td且align="center"的元素
        # split 就是把空白去掉用list把東西連在一起
        data = html('td[align="center"]').text().split()
        print(data)
        # 把取得的資料配給物件的屬性
        self.name = data[0]
        self.price = data[3]
        self.bid = data[4]
        self.offer = data[5]
