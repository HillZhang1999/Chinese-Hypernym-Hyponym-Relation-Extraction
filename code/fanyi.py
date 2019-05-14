import urllib.request
import gzip
import urllib.parse
import json
import time
import random
import hashlib


def translate(content):
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    # 定义变量
    client = 'fanyideskweb'
    ctime = int(time.time() * 1000)
    salt = str(ctime + random.randint(1, 10))
    # key = 'rY0D^0\'nM0}g5Mm1z%1G4' 以前版本的秘钥
    key = 'aNPG!!u6sesA>hBAW1@(-'
    sign = hashlib.md5((client + content + salt + key).encode('utf-8')).hexdigest()
    # 表单数据
    data = {}
    data['i'] = content
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['salt'] = salt
    data['sign'] = sign
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CL1CKBUTTON'
    data['typoResult'] = 'false'
    data = urllib.parse.urlencode(data).encode('utf-8')
    # 请求头
    head = {}
    head['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    head['Accept-Encoding'] = 'gzip, deflate'
    head['Accept-Language'] = 'zh-CN,zh;q=0.9'
    head['Connection'] = 'keep-alive'
    head['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    head[
        'Cookie'] = 'OUTFOX_SEARCH_USER_ID=-1645744815@10.169.0.84; JSESSIONID=aaa9_E-sQ3CQWaPTofjew; OUTFOX_SEARCH_USER_ID_NCOO=2007801178.0378454; fanyi-ad-id=39535; fanyi-ad-closed=1; ___rl__test__cookies=' + str(
        ctime)
    head['Host'] = 'fanyi.youdao.com'
    head['Origin'] = 'http://fanyi.youdao.com'
    head['Referer'] = 'http://fanyi.youdao.com/'
    head[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    head['X-Requested-With'] = 'XMLHttpRequest'

    request = urllib.request.Request(url, data, head)
    response = urllib.request.urlopen(request)
    with gzip.open(response, 'rb') as f:
        response = f.read()
    # response=response.read().decode('utf-8')
    target = json.loads(response)
    result = target['translateResult'][0][0]['tgt']
    return result


def main():
    content = input('请输入需要翻译的内容：')
    print(translate(content))

#主函数

if __name__ == '__main__':
  main()

#运行主函数



