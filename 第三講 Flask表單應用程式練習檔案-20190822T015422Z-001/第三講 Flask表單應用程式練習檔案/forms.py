from flask_wtf import FlaskForm
# 各種表單的引用
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField, TextAreaField
# 驗證器
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets.html5 import NumberInput


class CreateProductForm(FlaskForm):
    # TODO: 建立商品的表單

    # 名稱(title) 只能填單列 DataRequirred() 會提醒你要填這個資訊
    title = StringField('Title', validators=[DataRequired()])
    # 縮圖網址(img_url)
    img_url = StringField('Image', validators=[DataRequired()])
    # 價格(price) NumberRange 可以協助做數字大小的區間驗證
    price = IntegerField(
        'Price',
        validators=[DataRequired(),
                    NumberRange(min=0, max=900000)],
        # 幫html加上 type = number 的屬性
        # 在前端裡面 就會不允許輸入非數字的東西
        widget=NumberInput())
    # 是否銷售中(on_sale)
    on_sale = BooleanField('On sale?')
    # 類別(category[Electronics, Handmade, Industrial, Sports, Toys, Others])
    category = SelectField(
        'Category',
        choices=[
            # (資料, 使用者會看到的文字)
            ('electronics', 'Electronics'),
            ('handmade', 'Handmade'),
            ('industrial', 'Industrial')
        ])
    # 敘述(description)
    description = TextAreaField('Description')
    # 送出表單的按鈕(submit)
    submit = SubmitField('Creat Product')
    pass


class EditProductForm(FlaskForm):
    # 編輯商品的表單

    # 名稱(title) 只能填單列 DataRequirred() 會提醒你要填這個資訊
    title = StringField('Title', validators=[DataRequired()])
    # 縮圖網址(img_url)
    img_url = StringField('Image', validators=[DataRequired()])
    # 價格(price) NumberRange 可以協助做數字大小的區間驗證
    price = IntegerField(
        'Price',
        validators=[DataRequired(),
                    NumberRange(min=0, max=900000)],
        # 幫html加上 type = number 的屬性
        # 在前端裡面 就會不允許輸入非數字的東西
        widget=NumberInput())
    # 是否銷售中(on_sale)
    on_sale = BooleanField('On sale?')
    # 類別(category[Electronics, Handmade, Industrial, Sports, Toys, Others])
    category = SelectField(
        'Category',
        choices=[
            # (資料, 使用者會看到的文字)
            ('electronics', 'Electronics'),
            ('handmade', 'Handmade'),
            ('industrial', 'Industrial')
        ])
    # 敘述(description)
    description = TextAreaField('Description')
    # 送出表單的按鈕(submit)
    submit = SubmitField('Update Product')
    pass


class DeleteProductForm(FlaskForm):
    # 確認刪除 DataRequired: 要求一定要做回覆
    confirm = BooleanField('Delete?', validators=[DataRequired()])
    # 送出表單按鈕
    submit = SubmitField('Delete product')


class CreateCommentForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Creat comment')


class EditCommentForm(FlaskForm):
    # 編輯的時候不能編輯Email 所以把Email拿掉
    content = TextAreaField('Edit Content', validators=[DataRequired()])
    submit = SubmitField('Update comment')