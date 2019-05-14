from bs4 import BeautifulSoup
import requests
import re
import urllib
import time
global count
count=82708

def check_contain_chinese(check_str):#判断字符串是否包含中文
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

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
    web_data = s.get(url,timeout=3)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'html.parser')
    return soup

def getFenLei(word):#获取分类页面的地址（可能无页面）
    result = []
    url="http://fenlei.baike.com/"+urllib.parse.quote(word)+"/list"
    soup=getSoup(url)
    title=soup.find(name='title')
    if ("操作错误" not in title):
        for s in soup.find_all(name='dl',class_='link_blue line-25 zoom'):
            for k in soup.find_all(name='dd'):
                for wd in re.findall(r">(.+?)<", str(k)):
                    w=wd.split('[')[0]
                    if check_contain_chinese(w)and(len(w)<=10):
                        result.append(w+" "+word)
    return result

def tiaoZheng(filename1,filename2):
    li=readFile(filename1)
    f=open(filename2,'w')
    now=0
    for s in li:
        wordL=s.split(' ')
        f.write(wordL[0].split('[')[0]+" "+wordL[1]+"\n")
        print("第"+str(now)+"个任务")
        now+=1
    f.close()



def saveWordPairs(filename1,filename2,start):#保存基于fenlei的上下位词对,从词典文件的第start个词开始
    global count
    li=readFile(filename1)[start:]
    f=open(filename2,'a+',encoding='utf-8')
    count=start+1
    s=str(len(li))
    wordPais=[]
    for st in li:
        print("保存词对第"+str(count)+"个任务,上位词："+st+",共84742个任务")
        p=getFenLei(st)
        print("保存了" + str(len(p)) + "个结果")
        for w in p:
            if(w not in wordPais):
                f.write(w+'\n')
                wordPais.append(w)
        count+=1
        f.flush()
    f.close()

def chooseWordPairs(filename1,filename2,dicname):#抽取均在词典中的词对
    f1 = open(filename2, 'w', encoding='utf-8')
    dic=readFile(dicname)
    for s in readFile(filename1):
        wordPairs=s.split()
        flag=0
        for word in wordPairs:
            if (word not in dic):
                flag=1
                break
        if (flag==0):
            print(s)
            f1.write(s+'\n')
            f1.flush()
    f1.close()

def main():
    #global count
    #while (count <= 84742):
    #    try:
    #        saveWordPairs('words.conll', 'WordPairs-fenlei-v1.txt', count - 1)
    #    except:  # 防止异常
    #        print('第' + str(count) + '个任务失败！')
    #        time.sleep(3)
    #        pass
    #chooseWordPairs('WordPairs-fenlei-v1.txt', 'WordPairs-fenlei-v2.txt', 'words.conll')
    #print(len(readFile('WordPairs-fenlei-v2.txt')))
    tiaoZheng('WordPairs-fenlei-v1.txt','WordPairs-fenlei-v3.txt')


#主函数

if __name__ == '__main__':
  main()

#运行主函数
