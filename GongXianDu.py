import struct
from bs4 import BeautifulSoup
import requests
import re
import urllib
import time
global count
count=1

def readFile(filename):  # 读取文件,返回列表
    f = open(filename, 'r', encoding='utf-8')
    st = f.readline()
    result = []
    while (st):
        result.append(st.replace("\n", ""))
        st = f.readline()
    f.close()
    return result

def getSoup(url):#返回soup对象,解析网页源代码
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'  # 获取头文件
    web_data = s.get(url,timeout=2)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'html.parser')
    return soup

def getNums(word):#获取当前搜索词的结果数目
    url = 'http://www.baidu.com.cn/s?wd=' + urllib.parse.quote("intitle:"+word) + '&pn=0'#获取搜索页面的url
    soup=getSoup(url)
    for k in soup.find_all(name='span', class_="nums_text"):  # 抽取搜索结果条数的源代码
        nums=""
        for n in re.findall(r"\d+\.?\d*",str(k)):
            nums+=n
        result=eval(nums)#字符串转整数
    return result

def getValueW(word1,word2):#依据公式计算W值,W=hit(a,b)/min(hit(a),hit(b))，其中hit(a)为词在搜索引擎中出现的数目
    return(2*(getNums(word1+"+"+word2))/min((getNums(word1),getNums(word2))))

def getValueF(word1,word2):#计算筛选值F,F= F=together(a,b)/min(count(a),count(b))，其中together(a,b)为a词和b词在所有语料中在同一个句中出现的次数，count(a)为a词在所有语料中出现的次数
    with open("/Users/hillzhang/Desktop/zhangyue19/wiki/words/words.conll", "r", encoding="utf-8")as word_file:
        words = []
        for word in word_file.readlines():
            words.append(word.strip())
    wordNum = len(words)
    id2word_dict = {i: word for (i, word) in enumerate(words)}
    word2id_dict = {word: i for (i, word) in enumerate(words)}

    a = word2id_dict[word1]
    b = word2id_dict[word2]

    a_list = []
    flag_a = 0
    b_list = []
    flag_b = 0

    with open("/Users/hillzhang/Desktop/zhangyue19/wiki/wiki_dict/wiki_data.dict_b", "rb") as data_dict_b:
        while True:
            read_data = data_dict_b.read(4)
            if read_data:
                word_id = struct.unpack('i', read_data)[0]
                if word_id == a:
                    flag_a = 1
                    sentence_len = struct.unpack('i', data_dict_b.read(4))[0]
                    for i in range(sentence_len):
                        a_list.append(struct.unpack('i', data_dict_b.read(4))[0])
                    flag = struct.unpack('i', data_dict_b.read(4))[0]
                    if flag != -1:
                        print("数据出错a")
                        break
                    if flag_b == 1:
                        break
                elif word_id == b:
                    flag_b = 1
                    sentence_len = struct.unpack('i', data_dict_b.read(4))[0]
                    for i in range(sentence_len):
                        b_list.append(struct.unpack('i', data_dict_b.read(4))[0])
                    flag = struct.unpack('i', data_dict_b.read(4))[0]
                    if flag != -1:
                        print("数据出错b")
                        break
                    if flag_a == 1:
                        break
                else:
                    # print(word_id)
                    sentence_len = struct.unpack('i', data_dict_b.read(4))[0]
                    # print(sentence_len)
                    data_dict_b.seek(4 * sentence_len, 1)
                    flag = struct.unpack('i', data_dict_b.read(4))[0]
                    # print(flag)
                    if flag != -1:
                        print("数据出错")
                        break
            else:
                break
    c_list = sorted(list(set(a_list) & set(b_list)))
    if len(c_list) == 0:
        return 0
    else:
        return (len(c_list)/min(len(a_list),len(b_list)))

def getFile(filename1,filename2):#生成测试文件
    li=readFile(filename1)
    f=open(filename2,'w',encoding='utf-8')
    for i in range(0,10000,1000):
        for j in range (20000,30000,1000):
                f.write(li[i]+" "+li[j]+"\n")
    f.close()

def getValue (word1,word2):#获取综合值W+F
    return getValueF(word1, word2) + getValueW(word1, word2)


def train(infile,outfile,start):#计算W+F的值并保存
    global count
    li=readFile(infile)
    f=open(outfile,'a+',encoding='utf-8')
    for s in li[start:]:
        wordL=s.split()
        value = getValueF(wordL[0], wordL[1]) + getValueW(wordL[0], wordL[1])
        print("保存词对第"+str(count)+"个任务,共200个任务")
        print(wordL[0]+' '+wordL[1]+" "+str(value))
        if (value>0.01):
            f.write(s+"\n")
            f.flush()
        count+=1
    f.close()

def getResult(filename1,filename2):
    li1=readFile(filename1)
    li2=readFile(filename2)
    s=len(li1)
    right=0
    for word in li1:
        if (word in li2):
            right+=1
    p=right/s
    r=right/100
    f=2*p*r/(p+r)
    print('准确度:'+str(p))
    print("召回度:"+str(r))
    print("F1值:"+str(f))

def main():
     #getFile('words.txt','test.txt')
     global count
     while (count <= 200):
        try:
            train('test2','result3',count-1)
        except:  # 防止异常
            print('第' + str(count) + '个任务失败！')
            time.sleep(3)
            pass
    #getResult('result2','test')
#主函数

if __name__ == '__main__':
  main()
#运行主函数

