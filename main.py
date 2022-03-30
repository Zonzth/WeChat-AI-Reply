import time
import logging
from WechatPCAPI import WechatPCAPI
from queue import Queue
import threading
import aiui_core
fastlearning = 0
judge_AI=1


def on_message(message):
    queue_recved_message.put(message)

def thread_handle_message():
    global judge_AI
    while True:
        message = queue_recved_message.get()
        if message['data'].get('msg', 0) != 0:
            if message['data']['send_or_recv'] == '1+[Phone]':
                print(message['data']['msg']+"--->"+message['data']['from_nickname'])
                from_wxid = message['data']['from_wxid']
                msg = message['data']['msg']
                result=aiui_core.aiui(msg)
              
                reply(from_wxid,result[0]['intent']['answer']['text'])
            
def reply(from_wxid, replyStr):
    wx_inst.send_text(to_user=from_wxid, msg=replyStr)


logging.basicConfig(level=logging.INFO)
wx_inst = WechatPCAPI(on_message=on_message, log=logging)
queue_recved_message = Queue()


def logine():
    wx_inst.start_wechat(block=True)
    while not wx_inst.get_myself():
        time.sleep(1)
    print('登陆成功')
    threading.Thread(target=thread_handle_message).start()


logine()
