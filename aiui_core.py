import requests
import time
import hashlib
import base64
import json

URL = "http://openapi.xfyun.cn/v2/aiui"

APPID = ""
API_KEY = ""

#HEADER参数
auth_id = "" # 你的AUTH ID

data_type = "text"          # 明确处理类型 text文本/audio音频

scene = "main_box"          # 情景值

sample_rate = '16000'       #音频采样率

aue = 'raw'                 #音频编码

speex_size = '60'           #speex音频帧大小

lat = '31.83'               #纬度
lng = '117.14'              #经度

pers_param = ''             #个性化参数

result_level = 'plain'      #结果级别，可选择plain（精简），complete（完整）

interact_mode = 'oneshot'   #是否开启云端VAD

# FILE_PATH = './text.txt'


def buildHeader():
    curTime = str(int(time.time()))
    param = "{\"auth_id\":\""+auth_id+"\",\"data_type\":\""+data_type+"\",\"scene\":\""+scene+"\",\"interact_mode\":\""+interact_mode+"\"\
    ,\"sample_rate\":\""+sample_rate+"\",\"aue\":\""+aue+"\"}"
    paramBase64 = base64.b64encode(param.encode('utf-8'))

    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + str(paramBase64, 'utf-8')).encode('utf-8'))
    checkSum = m2.hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
    }
    return header

def readFile(filePath):
    binfile = open(filePath, 'rb')
    data = binfile.read()
    # print('data in file:', data)
    return data
def aiui(word):
    r = requests.post(URL, headers=buildHeader(), data=word.encode('UTF-8'))
    content = r.content
    json_resp = json.loads(content.decode('utf-8'))
    code = json_resp['code']
    if code == '0':
        # print('success in response')
        result=json_resp['data']
        print(result[0]['intent']['answer']['text'])
        return json_resp['data']
    else:
        raise Exception(json_resp)

if __name__ == '__main__':
    aiui('你好')