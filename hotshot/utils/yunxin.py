import hashlib
import time

import requests
import xml.etree.ElementTree as ET


class Yunxin:
    nonce = 'ymzmxh'
    HEX_DIGITS = ['0', '1', '2', '3', '4', '5',
                  '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    url = 'https://api.netease.im/sms/sendcode.action'

    def get_sms(self, phone, del_account=False):
        if del_account:
            account = self.del_get_account()
        else:
            account = self.get_account()
        # appKey = 'aeef21ae0d54f985fb3422b61165d712'
        # appSecret = 'c8d5f9272b87'
        if account is None:
            return None
        appKey = account['appKey']
        appSecret = account['appSecret']
        curTime = str(int(time.time()))
        encodeStr = (appSecret + self.nonce + curTime).encode(encoding='utf-8')
        checkSum = hashlib.sha1(encodeStr).hexdigest()
        checkSumByte = bytearray(checkSum, encoding='utf-8')
        strB = ''
        for j in checkSumByte:
            strB += self.HEX_DIGITS[(j >> 4) & 0x0f]
            strB += self.HEX_DIGITS[j & 0x0f]
        headers = {'AppKey': appKey, 'CurTime': curTime, 'CheckSum': checkSum, 'Nonce': self.nonce,
                   'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', }
        data = {'mobile': str(phone)}
        response = requests.post(self.url, data=data, headers=headers)
        # retrurn b'{"code":200,"msg":"1","obj":"5712"}'
        if response.json()['code'] != 200:
            self.get_sms(phone=phone, del_account=True)
        else:
            return response.json()

    def get_account(self):
        yun_xin_account = ET.ElementTree(file='./hotshot/utils/yunxinaccount')
        account = yun_xin_account.find('item')
        if account is not None:
            return account.attrib
        return None

    def del_get_account(self):
        yun_xin_account = ET.ElementTree(file='./hotshot/utils/yunxinaccount')
        root = yun_xin_account.getroot()
        account = yun_xin_account.find('item')
        if account is not None:
            root.remove(account)
            yun_xin_account.write('yunxinaccount', encoding='utf-8')
        account = yun_xin_account.find('item')
        if account is not None:
            return account.attrib
        else:
            return None
