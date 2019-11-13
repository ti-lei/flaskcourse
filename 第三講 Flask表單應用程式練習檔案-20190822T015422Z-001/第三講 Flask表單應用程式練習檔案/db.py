
import firebase_admin
from firebase_admin import credentials, firestore

# 引用key.json
cred = credentials.Certificate("config/key.json")
firebase_admin.initialize_app(cred)

# todo 建立一個資料庫的實例
db = firestore.client()