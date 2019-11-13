# 引用flask
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
# auth 是身分驗證模組
from firebase_admin import firestore, auth
from flask_wtf.csrf import CSRFProtect
# 引用時間模組
import time
import datetime
# 引用資料庫
from db import db
# 引用建立商品表單類別
from forms import (CreateProductForm,
                   EditProductForm,
                   DeleteProductForm,
                   CreateCommentForm,
                   EditCommentForm)

app = Flask(__name__)
csrf = CSRFProtect(app)
# 讓應用程式的所有模板可以直接取的CSRF
# 在這一步的時候 csrf 已經分配給所有的模板了
# 前端拿到token的方法 是使用 csrf_token() 取用已經分配好的 csrf
csrf.init_app(app)

# 設定應用程式的SECRET_KEY(secret key is required, CSRF)
app.config['SECRET_KEY'] = 'NTUCSIEFlask317'

# 定義應用程式要使用的session_cookie名稱
cookie_name = 'flask-cookie'



# 登入api
@app.route('/api/login', methods=['POST'])
def login_api():
    print('aa')
    # 取得 前端送來的 idToken
    id_token = request.json['idToken']
    # 過期日 das = N , N日後過期
    expires_in = datetime.timedelta(days=7)
    print('前端傳來的 id_token', id_token)
    print('過期時效', expires_in)
    # 換取 session_cookie(瀏覽器需要帶的簽證)
    session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
    print('session_cokkie', session_cookie)
    # 準備回應
    res = jsonify({'msg': '登入流程已完成'})
    # 把session_cookie寫到瀏覽器
    res.set_cookie(cookie_name, session_cookie)
    # 回應前端
    return res

@app.route('/hello', methods=['POST'])
def hello_api():
    # API不可以不回應, 如果後端收到前端的資料 但 沒有給前端回應 會出現 500 的錯誤
    data = request.json
    print('前端傳來的資料', data)
    # 準備給前端的回應
    res = jsonify({
        'msg': 'hello world',
        'msg2': f'你剛才傳的email是{data["email"]}'
    })
    return res
    

@app.route('/')
def index_page():
    # 從db取得products集合內的所有文件
    # direction=firestore.Query.DESCENDING 由大到小排
    # 建立時間由近到遠排
    docs = db.collection('products').order_by(
        'created_at', direction=firestore.Query.DESCENDING).get()
    # 產品列表
    products = []
    for doc in docs:
        # 建立一個產品的資料
        product = doc.to_dict()
        product['id'] = doc.id
        # 把產品放到產品清單內
        products.append(product)
    # 首頁路由
    return render_template('index.html', products=products)


@app.route('/create_product', methods=['GET', 'POST'])
def create_product_page():
    # 建立商品頁的路由
    # 建立商品表單的實例
    form = CreateProductForm()
    # 設定表單送出後的處理
    print('[前端使用路由的方法]', request.method)
    print('[表單是否被送出]', form.submit.data)
    print('[表單內的欄位是否通過驗證]', form.validate_on_submit())
    print('[表單驗證出了什麼問題]', form.errors)
    # 如果表單被送出 且 表單的欄位有通過驗證
    if form.submit.data and form.validate_on_submit():
        # 建構新產品的資料
        # form.欄位.data 使用者所設定的資料內容
        new_product = {
            'title': form.title.data,
            'img_url': form.img_url.data,
            'price': form.price.data,
            'category': form.category.data,
            'on_sale': form.on_sale.data,
            'description': form.description.data,
            'created_at': time.time()
        }
        print('[新產品資料]', new_product)
        # 取得目前的pid
        pid = db.document('web/config').get().to_dict()['pid']
        # 更新pid
        db.document('web/config').update({'pid': pid+1})
        # 把新產品資料(dict)存到db的products集合並以pid命名
        db.document(f'products/{pid}').set(new_product)
        # 把新產品資料存到session
        session['new_product'] = new_product
        # 在下一個畫面閃現訊息
        flash(
            f'A product has been created - {new_product["title"]}.', 'success')
        # 將使用者轉跳到指定的路由函數
        return redirect(url_for('form_feedback'))
    return render_template('create_product.html', form=form)


# 詳細頁
@app.route('/product/<pid>', methods=['GET', 'POST'])
def detail_product_page(pid):
    # 建立新增留言表單
    create_comment_form = CreateCommentForm(prefix='create-comment')
    # 如果新增留言表單送出
    if create_comment_form.submit.data and create_comment_form.validate_on_submit():
        # 建立一則留言
        new_comment = {
            'email': create_comment_form.email.data,
            'content': create_comment_form.content.data,
            'created_at': time.time()
        }
        print('[new_comment]', new_comment)
        # 新增留言
        db.collection(f'products/{pid}/comments').add(new_comment)
        # 閃現訊息
        flash('Your comment has been posted.', 'success')
        # 轉跳同一個頁面
        return redirect(url_for('detail_product_page', pid=pid))
    # 取得指定id的文件
    # doc = db.collection('products').document(pid).get()
    doc = db.document(f'products/{pid}').get()
    print('[doc]', doc)
    # 把文件處理為字典格式
    product = doc.to_dict()
    print('[product]', product)
    # 取得所有留言
    docs = db.collection(
        f'products/{pid}/comments').order_by('created_at').get()
    # 留言清單
    comments = []
    for doc in docs:
        # 一則留言
        comment = doc.to_dict()
        comment['id'] = doc.id
        # 把編輯表單記錄在留言上
        comment['form'] = EditCommentForm(prefix=doc.id)
        # 如果表單送出且合格
        if comment['form'].submit.data and comment['form'].validate_on_submit():
            # 更新文件
            db.document(f'products/{pid}/comments/{doc.id}').update({
                'content': comment['form'].content.data
            })
            # 閃現訊息
            flash('Your comment has been updated.', 'warning')
            # 回傳同一個畫面
            return redirect(url_for('detail_product_page', pid=pid))
        # 設定留言內容預設值
        comment['form'].content.data = comment['content']
        # 把留言放到清單
        comments.append(comment)
    # 回傳模板
    return render_template('detail_product.html',
                           product=product,
                           create_comment_form=create_comment_form,
                           comments=comments)

# 編輯頁
@app.route('/product/<pid>/edit', methods=['GET', 'POST'])
def edit_product_page(pid):
    # * 畫面上有一個以上的表單，要下prefix讓瀏覽器可辨識元件差異
    # 建立編輯表單
    form = EditProductForm(prefix='edit-product')
    # 建立刪除表單
    delete_form = DeleteProductForm(prefix='delete-product')
    # 判定編輯表單是否被送出且合法
    if form.submit.data and form.validate_on_submit():
        # 準備更新後的產品
        edited_product = {
            'title': form.title.data,
            'img_url': form.img_url.data,
            'price': form.price.data,
            'category': form.category.data,
            'on_sale': form.on_sale.data,
            'description': form.description.data
        }
        print('[edited_product]', edited_product)
        # 更新資料
        db.document(f'products/{pid}').update(edited_product)
        # 閃現訊息
        flash(
            f'Product has been updated - {edited_product["title"]}', 'warning')
        # 轉跳畫面
        return redirect(url_for('index_page'))
    # 判定刪除表單是否被送出且合法
    if delete_form.submit.data and delete_form.validate_on_submit():
        # 移除指定文件
        db.document(f'products/{pid}').delete()
        # 閃現訊息
        flash('A product has been delete', 'danger')
        # 轉跳首頁
        return redirect(url_for('index_page'))
    # 取得指定id文件
    doc = db.document(f'products/{pid}').get()
    # 取得產品資料
    product = doc.to_dict()
    print('[product]', product)
    # 將產品資料預設到編輯表單內
    form.title.data = product['title']
    form.img_url.data = product['img_url']
    form.price.data = product['price']
    form.category.data = product['category']
    form.on_sale.data = product['on_sale']
    form.description.data = product['description']
    # 回傳模板
    return render_template('edit_product.html',
                           form=form,
                           delete_form=delete_form)


# 新增成功頁
@app.route('/form_feedback')
def form_feedback():
    # 從session取出剛才此人所存的new_product
    product = session['new_product']
    # 商品建立成功的路由
    return render_template('form_feedback.html', product=product)


if __name__ == '__main__':
    app.run(debug=True)
