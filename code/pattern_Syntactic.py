class SyntacticExtraction:
    def __init__(self):
        self.yi=self.readFile('ATTquantifier')
        self.Is = self.readFile('Vis')
        self.oneOf = self.readFile('NOUNoneof')
        self.ADVfilter = self.readFile('ADVfilter')
        self.Replenish = self.readFile('Replenish')
        self.XianDing = self.readFile('XianDing')
        self.contain=self.readFile('Vcontain')
        #初始化常用词典成员变量

    def readFile(self,filename):  # 读取文件,返回列表
        f = open(filename, 'r', encoding='utf-8')
        st = f.readline()
        result = []
        while (st):
            result.append(st.replace("\n", ""))
            st = f.readline()
        f.close()
        return result

    def isPattern(self,words, now, ycjf, limit):  # 判断当前的谓语是否满足pattern
        pass

    def getProfix(self,words, cx, now):  # 获取名词类的修饰词作为前缀，保证上下位词对的准确度和完全度
        n = int(now)
        st = ''
        for i in range(n + 1, len(words) + 1): #补全书名号算法
            if (words[i - 1] == ';' or words[i - 1] == ',' or words[i - 1] == '、' or words[i - 1] == '《'):
                break
            elif (words[i - 1] == '》'):
                for j in range(n - 1, 0, -1):
                    if (words[j - 1] == '《'):
                        for k in range(j + 1, i):
                            st += words[k - 1]
                        return st
        result = []
        for i in range(n - 1, 0, -1):
            if (cx[i - 1] == 'NN' or cx[i - 1] == 'NR' or cx[i - 1] == 'CD' or (words[i - 1] in self.Replenish)):#搜索补全
                result.append(words[i - 1])
            elif (cx[i-1]=='DT' and words[i - 1] in self.XianDing) or cx[i - 1] == 'PN' or (i > 1 and cx[i - 1] == 'DEG' and cx[i - 2] == 'PN'):#规则限定
                result.append('*')
            else:
                break
        for w in result[::-1]:
            st += w
        st += words[n - 1]
        return st

    def compose(self,hyponyms, hypernyms):#组合生成词对
        result = []
        if (hyponyms == -1) or (hypernyms == -1):  # 上下位中有一个未抽取到词
            return result
        for sw in hyponyms:
            if (sw[1] == 'NN' or sw[1] == 'NR'):  # 是否名词（时间名词除外）
                for xw in hypernyms:
                    if (xw[1] == 'NN' or xw[1] == 'NR'):  # 是否名词（时间名词除外）
                        result.append(sw[0] + ' ' +xw[0])
        return result

    def saveWordPairs(self,infile, outfile, limit):  # 保存词对
        pass

    def getSentence(self,words):#拼接成句子
        sen = ''
        for w in words:
            sen += w
        return sen

    def showYcjf(self,ycjf, words, cx):#返回依存句法列表
        result = []
        for tmp in ycjf:
            if (int(tmp[0]) > 0):
                result.append(
                    words[int(tmp[0]) - 1] + '/' + cx[int(tmp[0]) - 1] + ' ' + words[int(tmp[1]) - 1] + '/' + cx[
                        int(tmp[1]) - 1] + ' ' + tmp[2])
            elif (int(tmp[0]) == 0):
                result.append(
                    "Root" + '/' + "$" + ' ' + words[int(tmp[1]) - 1] + '/' + cx[int(tmp[1]) - 1] + ' ' + tmp[2])
        return result

    def isSentence(self,sen,words):  # 判断是否是满足pattern的句子
        pass

    def saveWordPairs(self,infile, outfile, limit):  # 保存词对
        f = open(outfile, 'w', encoding='utf-8')
        count = 0
        sum = 0
        f2 = open(infile, 'r', encoding='utf-8')
        sen = f2.readline()
        dic = self.readFile('words.txt')
        words = []  # 句子的词序列
        cx = []  # 句子的词性序列
        ycjf = []  # 句子的依存句法序列
        f3 = open('Sentence_' + outfile, 'w', encoding='utf-8')
        while sen:
            if (sen == '\n'):
                sen = self.getSentence(words)
                if self.isSentence(sen,words):
                    ycjf2 = ycjf.copy()
                    resultL = self.getWordPairs(words, cx, ycjf, limit)
                    #print(sen)
                    #print(resultL)
                    flag = 0
                    for result in resultL:
                        tmp = result.split()
                        if (tmp[0] in dic) and (tmp[1] in dic) and (tmp[0] != tmp[1]):  # 去除掉词语中在过滤词典中的、上下位相等的
                            sum += 1
                            if (flag == 0):#保存句子、依存句法树
                                jfLi = self.showYcjf(ycjf2, words, cx)
                                f3.write(sen + '###')
                                for i in jfLi:
                                    f3.write(i + '###')
                                f3.write('\n')
                                count += 1
                                flag = 1
                            f.write(result + ' ' + str(count) + '\n')
                            f.flush()
                words = []
                cx = []
                ycjf = []
            else:
                li = sen.split('\t')
                words.append(li[1])
                cx.append(li[3])
                ycjf.append([li[6], li[0], li[7], li[9].rstrip('\n')])
            sen = f2.readline()
        f3.close()
        f3 = open('result.out', 'a+')
        f3.write(outfile + ' ' + str(sum) + '\n')
        f.close()
        f2.close()
        f3.close()