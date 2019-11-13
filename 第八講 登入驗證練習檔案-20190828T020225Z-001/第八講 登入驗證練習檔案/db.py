import firebase_admin
from firebase_admin import credentials, firestore
# 引用key.json(資料庫金鑰)
cred = credentials.Certificate("config/key.json")
firebase_admin.initialize_app(cred)

# 建立一個資料庫的實例
db = firestore.client()
