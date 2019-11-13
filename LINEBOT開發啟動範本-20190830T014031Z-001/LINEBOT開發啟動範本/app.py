import firebase_admin
from firebase_admin import credentials, firestore
import requests

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

# 資料庫
db = firestore.client()

#!/usr/bin/env python3
# 運行以下程式需安裝模組: line-bot-sdk, flask

# 引入flask模組
from flask import Flask, request, abort
# 引入linebot相關模組
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)



# MessageEvent: 收到訊息的處理器
# TextMessage: 接收使用者文字訊息的處理器
# StickerMessage: 接收使用者貼圖訊息的處理器
# TextSendMessage: 回傳文字訊息的處理器
# StickerSendMessage: 回傳貼圖訊息的處理器
# 如需增加其他處理器請參閱以下網址的 Message objects 章節
# https://github.com/line/line-bot-sdk-python
from linebot.models import (
    MessageEvent, 
    TextMessage, 
    StickerMessage, 
    TextSendMessage, 
    StickerSendMessage, 
    LocationSendMessage, 
    TemplateSendMessage, 
    ButtonsTemplate, 
    PostbackAction, 
    MessageAction, 
    URIAction, 
    CarouselTemplate, 
    CarouselColumn
)

from replies import default_reply

# 定義應用程式是一個Flask類別產生的實例
app = Flask(__name__)

# LINE的Webhook為了辨識開發者身份所需的資料
# 相關訊息進入網址(https://developers.line.me/console/)
CHANNEL_ACCESS_TOKEN = 'xHXoxirOWKicZrgEaKyEbcSVMlC21zH6sNDQNpQnhhyeqX6V7dPdN4XANS+l8cjP7fMeR0a0JA0lEghZ4UI2abhc1MfwHhUqRfkfi7KgReB+lR8jPYbGeF0bsWsNHXRfBpMACgTaRPtkfp9vPM4k1AdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '1352b08a4c88a10e7ebfe9ef3e8bb52b'

# ================== 以下為 X-LINE-SIGNATURE 驗證程序 ==================

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/", methods=['POST'])
def callback():
    # 當LINE發送訊息給機器人時，從header取得 X-Line-Signature
    # X-Line-Signature 用於驗證頻道是否合法
    signature = request.headers['X-Line-Signature']
    print('[REQUEST]')
    print(request)
    print('[SIGNATURE]')
    print(signature)

    # 將取得到的body內容轉換為文字處理
    body = request.get_data(as_text=True)
    print("[BODY]")
    print(body)

    # 一但驗證合法後，將body內容傳至handler
    try:
        print('[X-LINE-SIGNATURE驗證成功]')
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
# ================== 以上為 X-LINE-SIGNATURE 驗證程序 ==================


# ========== 文字訊息傳入時的處理器 ==========
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 當有文字訊息傳入時
    # event.message.text : 使用者輸入的訊息內容
    
    print('[使用者傳入文字訊息]')
    print(str(event))
    user_msg = event.message.text

    # 把使用者的留言用 - 切割
    user_input = user_msg.split('-')
    if user_input[0] == '常見問答' :
        # 取得指定文件並檢查文件是否存在
        doc = db.document(f'faq/{user_input[1]}').get()
        # 如果文件存在




    # # 準備要回傳的文字訊息
    # # reply = TextSendMessage(text=f'你剛才說的是{user_msg}')
    # reply = LocationSendMessage(
    # title='my location',
    # address='Tokyo',
    # latitude=35.65910807942215,
    # longitude=139.70372892916203
    # )
    # # 取得指定文件並檢查文件是否存在
    # doc = db.document(f'faq/{user_msg}').get()
    # # print(dir.doc)
    # print(doc.exists)



        if doc.exists:
            print(dir(doc))
            #把文件變成字典
            doc = doc.to_dict()
            #判讀回應的格式
            if doc['type'] == 'text':
                reply = TextSendMessage(text=doc['text'])
                
            elif doc['type'] == 'location':
                reply = LocationSendMessage(
                    title = doc['title'],
                    address = doc['address'],
                    latitude = doc['latitude'],
                    longitude = doc['longitude']
                )
            elif doc['type'] == 'image':
                #如果是圖片
                reply = ImageSendMessage(
                    original_content_url = doc['original_content_url']
                    # preview_image_url = doc.
                )
        elif user_input[0] =='UV':
            #政府資料來源
            # 網址要記得改成http 否則 ssl 驗證會掛
            uv_url = 'http://opendata.epa.gov.tw/api/v1/UV?%24skip=0&%24top=1000&%24format=json'
            data = requests.get(url=uv_url).json()
            for d in data:
                if user_input[1] == ['SiteName']:
                    reply = TextMessage
            print(data)
        # 如果沒有處理回應
        elif reply ==None:
            reply = default_reply
        # 回傳訊息
        line_bot_api.reply_message(
            event.reply_token,
            reply)


# ========== 貼圖訊息傳入時的處理器 ==========
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    # 當有貼圖訊息傳入時
    print('[使用者傳入貼圖訊息]')
    print(str(event))

    # 準備要回傳的貼圖訊息
    # HINT: 機器人可用的貼圖 https://devdocs.line.me/files/sticker_list.pdf
    reply = StickerSendMessage(package_id='2', sticker_id='149')

    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token,
        reply)


import os
if __name__ == "__main__":
    print('[伺服器開始運行]')
    # 取得遠端環境使用的連接端口，若是在本機端測試則預設開啟於port5500
    port = int(os.environ.get('PORT', 5500))
    # 使app開始在此連接端口上運行
    print('[Flask運行於連接端口:{}]'.format(port))
    # 本機測試使用127.0.0.1, debug=True
    # Heroku部署使用 0.0.0.0
    app.run(host='127.0.0.1', port=port, debug=True)
