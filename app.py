#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from flask import Flask, jsonify, render_template, request
import requests
import json
import numpy as np
import easyocr
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage
)
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)

app = Flask(__name__)

lineaccesstoken = 'SYXnsTdB0dFYCTH0zlYnUYF+pesgGsi1j9pTLsADqZXtSdYfTAnuxLBMwORGudClbJ6+VwXZOM1R3NA187Mhpr9wuATWVzRBpPSAfaIA5wFosxRBIUmsvZsneZZTwjCWE15JDL9+JdvviMwFRA4c/AdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)

####################### new ########################
@app.route('/')
def index():
    return "Hello World!"


@app.route('/webhook', methods=['POST'])
def callback():
    json_line = request.get_json(force=False,cache=False)
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        event_handle(event)
    return '',200


def event_handle(event):
    print(event)
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''

    try:
        rtoken = event['replyToken']
    except:
        print('error cannot get rtoken')
        return ''
    try:
        msgId = event["message"]["id"]
        msgType = event["message"]["type"]
    except:
        print('error cannot get msgID, and msgType')
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
        return ''
#####################################################################
    if msgType == "text":
        msg = str(event["message"]["text"])
        replyObj = TextSendMessage(text=msg)
        line_bot_api.reply_message(rtoken, replyObj)

    elif msgType == "image":
        
        img_id = event["message"]["id"]

        # message_content = line_bot_api.get_message_content(img_id)
        # with open('temp.png', 'wb') as fd:
        #     for chunk in message_content.iter_content():
        #         fd.write(chunk.content)

        url = f"https://api-data.line.me/v2/bot/message/{img_id}/content?LineBotApi={lineaccesstoken}"

        headers = {
        'Authorization': f'Bearer {lineaccesstoken}',
        'Accept': 'image/webp'
        }

        r = requests.request("GET", url, headers=headers)
        with open('temp.jpg','wb') as f:
            f.write(r.content)
        
        msg=''
        reader = easyocr.Reader(['en'], gpu = True)
        bounds = reader.readtext('temp.jpg')
        for i in bounds:
            if msg == '':
                msg = str(i[1])
            else:
                msg=msg+'\n'+str(i[1])

        replyObj = TextSendMessage(text=msg)
        line_bot_api.reply_message(rtoken, replyObj)

    else:
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
    return ''

if __name__ == '__main__':
    app.run(debug=True)
