from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets.html5 import NumberInput


class CreateProductForm(FlaskForm):
    # 建立商品的表單
    # 名稱(title)
    title = StringField('Title', validators=[DataRequired()])
    # 縮圖網址(img_url)
    img_url = StringField('Image', validators=[DataRequired()])
    # 價格(price)
    price = IntegerField('Price',
                         validators=[
                             DataRequired(),
                             NumberRange(min=0, max=9000000)
                         ],
                         widget=NumberInput()
                         )
    # 是否銷售中(on_sale)
    on_sale = BooleanField('On sale?')
    # 類別(category[Electronics, Handmade, Industrial, Sports, Toys, Others])
    category = SelectField('Category', choices=[
        # (資料, 使用者會看到的選項文字)
        ('electronics', 'Electronics'),
        ('handmade', 'Handmade'),
        ('industrial', 'Industrial')
    ])
    # 敘述(description)
    description = TextAreaField('Description')
    # 送出表單的按鈕(submit)
    submit = SubmitField('Create product')


class EditProductForm(FlaskForm):
    # 編輯商品的表單
    # 名稱(title)
    title = StringField('Title', validators=[DataRequired()])
    # 縮圖網址(img_url)
    img_url = StringField('Image', validators=[DataRequired()])
    # 價格(price)
    price = IntegerField('Price',
                         validators=[
                             DataRequired(),
                             NumberRange(min=0, max=9000000)
                         ],
                         widget=NumberInput()
                         )
    # 是否銷售中(on_sale)
    on_sale = BooleanField('On sale?')
    # 類別(category[Electronics, Handmade, Industrial, Sports, Toys, Others])
    category = SelectField('Category', choices=[
        # (資料, 使用者會看到的選項文字)
        ('electronics', 'Electronics'),
        ('handmade', 'Handmade'),
        ('industrial', 'Industrial')
    ])
    # 敘述(description)
    description = TextAreaField('Description')
    # 送出表單的按鈕(submit)
    submit = SubmitField('Update product')


class DeleteProductForm(FlaskForm):
    # 確認刪除
    confirm = BooleanField('Delete?', validators=[DataRequired()])
    # 送出表單按鈕
    submit = SubmitField('Delete product')


class CreateCommentForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create a comment')


class EditCommentForm(FlaskForm):
    content = TextAreaField('Edit content', validators=[DataRequired()])
    submit = SubmitField('Update comment')
