from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import func

from urllib.parse import parse_qsl

import requests

app = Flask(__name__)
CORS(app)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('zBJ/wUyLC74E5hXEobjc6s5hGiiH4Tm4dIdV4sbQrcX8azehI5MaZF9sG9sZgXUEQ+SFRzcaiu9TF7vOsinCn+0DFEhfbuWKEDArVssCnzmf208uG2Fcfn53vKqEPEGWMHUvyydFTO6eYYvQvdTxYQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('abe4bad7299820f486c4e91c38b596a4')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print('THE BODY: ' + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
# event.message 為 TextMessage 實例。所以此為處理 TextMessage 的 handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    #讓line develoes webhook驗證時，不會因罐頭訊息跳出錯誤
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        #回傳訊息的api
        line_bot_api.reply_message(event.reply_token,message)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
