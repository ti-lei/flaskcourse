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

# 定義預設回應 default_reply(Template)
default_reply = TemplateSendMessage(
    alt_text='預設文字說明',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://picsum.phtos/id/1070/1200/700.jpg',
                title='this is menu1',
                text='description1',
                actions=[
                    MessageAction(
                        label='查看聯絡地址',
                        text='聯絡地址'
                    ),
                    MessageAction(
                        label='查看聯絡電話',
                        text='聯絡電話'
                    ),
                    MessageAction(
                        label='查看照片',
                        text='餐點照片'
                    )
                ]
            ),
            # 第二張卡片
             CarouselColumn(
                thumbnail_image_url='https://picsum.phtos/id/1070/1200/700.jpg',
                title='this is menu1',
                text='description1',
                actions=[
                    MessageAction(
                        label='查看聯絡地址',
                        text='聯絡地址'
                    ),
                    MessageAction(
                        label='查看聯絡電話',
                        text='聯絡電話'
                    ),
                    MessageAction(
                        label='查看照片',
                        text='餐點照片'
                    )
                ]
            )           

        ]
    )
)