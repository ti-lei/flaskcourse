from flask import Flask, render_template, request, session, redirect, url_for, flash
from firebase_admin import firestore
import time

# TODO: 引用建立商品表單類別
# 引用太多要用小括號包住
from forms import (CreateProductForm, EditProductForm, DeleteProductForm,
                   CreateCommentForm, EditCommentForm)

app = Flask(__name__)
# 引用資料庫 注意這裡回去看db.py 我們是引用db.py裡產生的一個instance
from db import db
# TODO: 設定應用程式的SECRET_KEY 創造金鑰以免別人製造假網頁對server送出請求 (必要)
app.config['SECRET_KEY'] = 'NTU'
print(app.config)


@app.route('/')
def index_page():
    # 從db取得products集合內的所有文件 由小到大排列
    # direction = firestore.Query.DESCENDING 由大到小排 如果想要由小到大直接刪掉這個attr就好(因為是預設)
    # 建立時間由近到遠排
    # 從 frirebase 拉下來的資料是一個無法print出來的object集合
    docs = db.collection('products').order_by(
        'created_at', direction=firestore.Query.DESCENDING).get()

    # dir(物件) 會將所有的屬性印出來
    print('[docs]', dir(docs))
    # 產品列表
    products = []
    for doc in docs:
        # 每一個產品都在不同文件的ID裡
        print('[文件ID]', doc.id)
        print('[文件資料]', doc.to_dict())

        # 建立一個產品的資料 doc.to_dict()拿到產品的欄位
        product = doc.to_dict()
        # 拿到文件ID
        product['id'] = doc.id
        # 把產品放到產品清單內
        products.append(product)

    # 首頁路由
    return render_template('index.html', products=products)


# GET 前端 呈現(GET) 後端 的資料
# POST 前端 將資料 傳送(POST) 給後端
@app.route('/create_product', methods=['GET', 'POST'])
def create_product_page():
    # 建立商品頁的路由
    # TODO: 建立商品表單的實例
    form = CreateProductForm()
    # TODO: 設定表單送出後的處理
    print('[判別使用路由的方法]', request.method)
    print('[表單是否被送出]', form.submit.data)
    print('[表單內的欄位是否通過驗證]', form.validate_on_submit())
    print(['表單出了什麼問題'], form.errors)

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

        # 將使用者轉跳到指定的路由函數
        # 使用 redirect 的原因? 這樣在傳 參數 時就不需要重新寫程式碼
        print('[新產品資料]', new_product)

        # 取得目前的PID, pid 會是 key, value 會是 目前新增的產品數量
        pid = db.document('web/config').get().to_dict()['pid']

        # 更新PID
        db.document('web/config').update({'pid': pid + 1})

        # 把新產品資料(dict)存到db的products集合並以pid命名, set的功用是把資料填進指定的文件裡
        # 與 [update] 不同的地方在於 update 只會把有動到的資料做更新 set 會把文件給丟掉
        db.document(f'products/{pid}').set(new_product)

        # 把新產品資料(dict)存到db的products集合, 使用 add會隨機產生文件的名字
        # db.collection('products').add(new_product)

        # 把新產品資料存到session
        session['new_product'] = new_product
        # 在下一個畫面閃現訊息
        # 字串前面 + f 可以串接字串
        # 'succes' 是我想傳入的 class 名稱 在bootstrap 裡 是叫做 alert-success
        flash(f'A product has been created - {new_product["title"]}.',
              'success')
        return redirect(url_for('form_feedback'))
    return render_template('create_product.html', form=form)


# 詳情頁,  <pid> 要帶入文件的ID
@app.route('/product/<pid>', methods=['GET', 'POST'])
def detail_product_page(pid):
    # 建立新增留言表單
    create_comment_form = CreateCommentForm(prefix='create-comment')
    # 如果新增表單送出 而且 資料無誤
    if create_comment_form.submit.data and create_comment_form.validate_on_submit(
    ):
        # 建立一則留言
        new_comment = {
            'email': create_comment_form.email.data,
            'content': create_comment_form.content.data,
            'created_at': time.time()
        }
        print(new_comment)

        # 新增留言
        db.collection(f'products/{pid}/comments').add(new_comment)

        # 閃現訊息
        flash('Your comment has been posted.', 'success')

        # 轉跳到同一個頁面
        return redirect(url_for('detail_product_page', pid=pid))

    # 取得指定id的文件
    doc = db.collection('products').document(pid).get()

    # 把文件處理為字典格式
    product = doc.to_dict()

    # 從 fire base 取得所有留言, 按照時間建立先後排序
    docs = db.collection(f'products/{pid}/comments').order_by(
        'created_at').get()

    # 留言清單
    comments = []
    for doc in docs:
        # 一則留言
        comment = doc.to_dict()
        comment['id'] = doc.id

        # 把編輯表單的功能 放在 過去的留言上, prefix = doc.id 可以讓 html 區分送出的是不同的表單
        comment['form'] = EditCommentForm(prefix=doc.id)

        # 如果表單送出且合格
        if comment['form'].submit.data and comment['form'].validate_on_submit(
        ):
            # 更新文件
            db.document(f'products/{pid}/comments/{doc.id}').update(
                {'content': comment['form'].content.data})
            # 閃現訊息
            flash('Your comment has been updated.', 'warning')
            # 回傳同一個畫面
            return redirect(url_for('detail_product_page', pid=pid))

        # 設定留言內容預設值
        comment['form'].content.data = comment['content']
        # 把留言放到清單內
        comments.append(comment)

    # 回傳模板
    return render_template('detail_product.html',
                           product=product,
                           create_comment_form=create_comment_form,
                           comments=comments)


# 編輯頁
@app.route('/product/<pid>/edit', methods=['GET', 'POST'])
def edit_product_page(pid):

    # ** 畫面上有一個以上的表單，要下 prefix 讓瀏覽器可辨識元件差異 **
    # prefix 加入了以後 在 html 裡面的 ID 和 name 的屬性 的 前面 會增加 prefiix設定的字串
    # ex:prefix = 'GG', 原本ID:'abc' 變成 ID:'GG-abc'
    # 建立編輯表單
    form = EditProductForm(prefix='edit-product')

    # 建立刪除表單
    delete_form = DeleteProductForm(prefix='delete-product')

    # 判斷編輯表單是否被送出且合法
    if form.submit.data and form.validate_on_submit():
        #準備更新後的產品
        edited_product = {
            'title': form.title.data,
            'img_url': form.img_url.data,
            'price': form.price.data,
            'category': form.category.data,
            'on_sale': form.on_sale.data,
            'description': form.description.data,
        }
        print('[edited_product]', edited_product)
        # 更新資料 / 除了時間以外都進行更新
        db.document(f'products/{pid}').update(edited_product)
        # 閃現訊息
        flash(f'Product has been updated - {edited_product["title"]}',
              'warning')
        # 轉跳畫面
        return redirect(url_for('index_page'))

    # 判斷刪除表單是否被送出且合法
    if delete_form.submit.data and delete_form.validate_on_submit():
        #移除指定文件
        db.document(f'products/{pid}').delete()
        flash('A product has been deleted', 'danger')
        return redirect(url_for('index_page'))

    # 取得指定id文件
    # 跟詳情頁一樣的取法不過只使用一次方法
    doc = db.document(f'products/{pid}').get()

    # 取得產品資料
    product = doc.to_dict()

    print('[Product]', product)
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
    # 從session取出港才此人存的new_product
    product = session['new_product']
    print(session)
    # 商品建立成功的路由
    return render_template('form_feedback.html', product=product)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
