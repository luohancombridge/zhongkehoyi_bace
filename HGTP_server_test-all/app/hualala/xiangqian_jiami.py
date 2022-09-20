# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
__author__ = 'Administrator'
import base64
from Crypto.Cipher import AES
import json
import requests
class AESCipher:
    def __init__(self,key):
        # self.key = 'Jy_ApP_0!9i+90&#'[0:16] #只截取16位
        self.key = key[0:16] #只截取16位
        self.iv = "2015030120123456" # 16位字符，用来填充缺失内容，可固定值也可随机字符串，具体选择看需求。
    def __pad(self, text):
        """填充方式，加密内容必须为16字节的倍数，若不足则使用self.iv进行填充"""
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad
    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]
    def encrypt(self, raw):
        """加密"""
        raw = self.__pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))
    def decrypt(self, enc):
        """解密"""
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv )
        return self.__unpad(cipher.decrypt(enc).decode("utf-8"))
class hengfeng_w_sing(object):
    #参数是请求中的reqData，字典格式，
    def __init__(self,data):
        self.url_sing = 'http://xq-app-server.jc1.jieyue.com/xqAppServer/api/APPBizRest/sign/v1/'
        if type(data) not in [list,dict]:
            self.data=json.dumps(data)
        else:
            self.data=data
    #返回直接可以调用的json字符串
    def sign_return(self):
        self.header_data={"Content-Type": "application/json"}
        self.header_data['reqJSON'] = json.dumps(self.data)
        k = requests.post(self.url_sing, data=json.dumps(self.data), headers=self.header_data)
        return  json.loads(k.text)['responseBody']['sign']


if __name__ == '__main__':
    e = AESCipher('Jy_ApP_0!9i+90&#')
    s={'aesRequest': "3QMTcYkRYmi3dh/F3fNk73eWbCeqZ7cWwRWYdkaggKyQCzdoOT52SMJURaGMqhlWpY0x5a6vTO46gsVnEaJ3Ng=="}

    data={"aesResponse":"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"}

    # enc_str = e.encrypt('123456')
    dec_str = e.decrypt(s['aesRequest'])
    # print('dec str: ' + dec_str)
    print(dec_str)