#載入Linebot所需模組
from flask import Flask, request, abort

from linebot import(
    LineBotApi, WebhookHandler
)
from linebot.exceptions import(
    InvalidSignatureError
)
from linebot.models import *
 
app = Flask(__name__)
line_bot_api = LineBotApi("7A3PibTZDmxuvjKLP10FdEyYvlthWHABiy/4crzalC6oZ61IpV+BgF+b7WLABv/3NCv1EQZXrq17uC5lc7P5rn3KTtvNcuAO3CpkRU1I8GwxHmIoXBSvfNRDeYuGLmgcqMOtw93QBWKabOhVoM3UGwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("85233d8e7e4176e352f29b9ff2713870")
line_bot_api.push_message("Ueb610375209b3338cba1a20b94cd8d11"
,TextSensMessage(text= 'YOU can start')
)

#監聽所有來自 /callback的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    #get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    #get request body as text
    body = request.get_data(as_text= True)
    app.logger.info('Request body: '+ body)

    #handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

#訊息傳遞
@handler.add(MessageEvent, message= TextMessage)
def handle_message(event):
    message = TextSendMessage(text= event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

#主程式
import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host= '0.0.0.0', port=port)