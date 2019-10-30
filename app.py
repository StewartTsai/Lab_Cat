import pymysql.cursors

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os

app = Flask(__name__)


access_token='Pj78g5mXSl5w/HfK3z4Qe4TRDTsi2wJZYZostAp2CHvAJsQZOjd4rI9vwIHYK2RovIjS3FJ8jMyY+Yn58MIdnRoiOTeKdfKGxEp7sYKoFcRhBIYZ7WPctF2NMWCJFyJbSbIIr1APEVLm1UIdcG3UqwdB04t89/1O/w1cDnyilFU='
chaneL_secret='748e776d2ecd781e5b472c3f6661490b'


# Channel Access Token
line_bot_api = LineBotApi(access_token)
# Channel Secret
handler = WebhookHandler(chaneL_secret)

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)
   
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
