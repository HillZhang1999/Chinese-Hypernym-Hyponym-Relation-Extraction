import jieba
import jieba.posseg
import re
dictGL=['这','本','此','该','那','我','你','他','她','似乎','好像','大概','貌似','它','之前','最近','今',"明",'例子','世纪','初','早','·','对于']
dictBL=['本质 上','指 的','说 的','表示 的']
jieba.load_userdict("words.conll")

def readFile(filename):  # 读取文件,返回列表
    f = open(filename, 'r', encoding='utf-8')
    st = f.readline()
    result = []
    while (st):
        result.append(st.replace("\n", ""))
        st = f.readline()
    f.close()
    return result

def getWord(sentence):#从短语或句子中抽取出实体名词
    word=jieba.posseg.lcut(sentence)#词性标注
    matchNList=['n','nr','nt','ns','nz','nrj']#名词词性列表
    if len(word)==1:#如果只有一个词，并且这个词是名词，直接返回这个词
        k=str(word[0])
        li=k.split('/')
        if (li[1] in matchNList):#如果词性是名词
            return (li[0])
    #matchVList=['v','vd','vn']
    #for i in range(len(word)):
    #    k=str(word[i])
    #    li=k.split('/')
    #    if (li[1] in matchVList):#匹配到动词之前
    #        word=word[:i]
    #        break
    for i in range(len(word)-1,-1,-1):#倒序遍历
        k=str(word[i])
        li=k.split('/')
        #print(k)
        if (li[1] in matchNList):#匹配第一个名词及之后的内容
            return (li[0])
    return -1

def hearst_pattern(senCut):#基于pattern的方法，先使用isA模板
    sleft=""
    sright="" 
    if (len(senCut)>1):
        for i in range(len(senCut)-1):#按照pattern，从是一[个（种，类...）]处将句子分为左右两部分，方便抽取上下位关系
            if ("是" in senCut[i])and("一" in senCut[i+1]):
                for w in senCut[:i]:
                    sleft+=w
                for w in senCut[i+2:]:
                    sright+=w
                break
            #print(w.word+" "+w.flag)
    pleft=sleft.split('的')[-1]
    pright=sright.split('的')[-1]
    #print(pleft)
    #print(pright)
    #按照人们的语言习惯，选取左边和右边部分最后一个的后面的短语进行分析
    wleft=getWord(pleft.split("（")[0])
    wright=getWord(pright.split("（")[0])
    #抽取实体名称作为下位和上位
    #print(wleft)
    #print(wright)
    if(wright!=-1)and(wleft!=-1):
        if (len(wright)<10)and(len(wleft)<10)and(wleft!=wright):#要求均有返回值，且上位词和下位词不能相同
            return(wleft+" "+wright)
    return -1

def train(infile,outfile):#训练模型
    li=open(infile)
    count=0
    f=open(outfile,'w',encoding='utf-8')
    for s in li:
        count+=1
        s = re.sub(r'（[^（）]*）', '', s)  # 去除解释性的内容
        l=s.split('，')#以逗号分隔句子，防止匹配混乱
        print("保存词对第"+str(count)+"个任务,共233302个任务")
        for sen in l:
            flag = 0
            for word in dictGL:  # 过滤词典过滤句子
                if word in sen:
                    flag = 1
            if flag == 1:
                continue
            for word in dictBL:#剥离词典剥离
                sen=sen.replace(word,'')
            result=hearst_pattern(sen.split())
            if (result!=-1):#有结果
                f.write(result+'\n')
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

def quChong(filename1,filename2):#去重
    li=readFile(filename1)
    count=0
    for word in li[:-1]:
        if li.count(word)>1:
            li.remove(word)
    f=open(filename2,'w',encoding='utf-8')
    for w in li:
        f.write(w+'\n')
        f.flush()
        print("去重任务："+str(count))
        count+=1
    f.close()

def main():
    train('sentenceWithIsA.txt','WordPairs-isA-v4.txt')
    #print(hearst_pattern('Linux   只是 一个 符合   POSIX   标准 的 内核'.split()))
    #quChong('WordPairs-isA-v4.txt','WordPairs-isA-v5.txt')
    #chooseWordPairs('WordPairs-isA-v5.txt', 'WordPairs-isA-v6.txt', 'words.conll')
#主函数

if __name__ == '__main__':
  main()
#运行主函数
