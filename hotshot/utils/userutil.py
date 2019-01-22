# 手机号码正则表达式
import re

REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"


def verify_phone(phone=''):
    if re.match(REGEX_MOBILE, phone) is not None:
        return True
    return False
