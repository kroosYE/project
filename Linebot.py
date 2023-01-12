# 載入LineBot所需要的套件
import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(
    '7A3PibTZDmxuvjKLP10FdEyYvlthWzalC6oZ61IpV+BgF+b7WLABv/3NCv1EQZXrq17uC5lc7P5rn3KTtvNcuAO3CpkRU1I8GwxHmIoXBSvfNRDeYuGLmgcqMOtw93QBWKabOhVoM3UGwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('85233d8e52f29b9ff2713870')

line_bot_api.push_message(
    'Ueb61338cba1a20b94cd8d11', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text = event.message.text
    if re.match('告訴我秘密', message):
        # Flex Message Simulator網頁：https://developers.line.biz/console/fx/
        flex_message = FlexSendMessage(
            alt_text='鉅亨網',
            contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://cimg.cnyes.cool/prod/news/4413249/l/80014f698152aa983bc9e9984fe4510f.png",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "action": {
                        "type": "uri",
                        "uri": "https://linecorp.com"
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "action": {
                        "type": "uri",
                        "uri": "https://linecorp.com"
                    },
                    "contents": [
                        {
                            "type": "text",
                            "text": "anue鉅亨網",
                            "size": "xxl",
                            "weight": "bold"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "新聞",
                                            "weight": "bold",
                                            "margin": "xs",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": "NEWS",
                                            "size": "sm",
                                            "align": "end",
                                            "color": "#aaaaaa"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "台股",
                                            "weight": "bold",
                                            "margin": "xs",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": "TAIEX",
                                            "size": "sm",
                                            "align": "end",
                                            "color": "#aaaaaa"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "美股",
                                            "weight": "bold",
                                            "margin": "xs",
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": "S&P 500",
                                            "size": "sm",
                                            "align": "end",
                                            "color": "#aaaaaa"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "text",
                            "text": "Anue鉅亨即時財經新聞，帶您掌握全球經濟趨勢、股市即時訊息、國際政經、時事及匯率",
                            "wrap": True,
                            "color": "#aaaaaa",
                            "size": "xxs"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#905c44",
                            "margin": "xxl",
                            "action": {
                                "type": "uri",
                                "label": "進入網站",
                                "uri": "https://www.cnyes.com/"
                            }
                        }
                    ]
                }
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
