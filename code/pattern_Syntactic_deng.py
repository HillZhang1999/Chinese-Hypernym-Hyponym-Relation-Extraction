import pattern_Syntactic as father

class SyntacticExtraction_deng(father.SyntacticExtraction):
    def isPattern(self,words, now, ycjf, limit):  # 判断当前的名词是否满足pattern
        tmp = []
        for k in ycjf:
            if (k[0] == now) and (k[2] == 'att') and (eval(k[3]) > limit):
                tmp.append(k[1])
                for j in ycjf:
                    if (j[0] == k[1]) and (j[2] == 'adjct') and (eval(j[3]) > limit):
                        n = int(j[1])
                        if (n < len(words)) and (words[n - 1] == '等' or words[n - 1] == '等等') and (words[n] != '的'):
                            # print(words[n-1])
                            # print(n)
                            return n  # 返回位置
        for k in ycjf:  # 考虑并列词
            if (k[0] in tmp) and ((k[2] == 'coo') or (k[2] == 'sasubj') or (k[2] == 'dfsubj')) and (eval(k[3]) > limit):
                tmp.append(k[1])
                for j in ycjf:
                    if (j[0] == k[1]) and (j[2] == 'adjct') and (eval(j[3]) > limit):
                        n = int(j[1])
                        if (n < len(words)) and (words[n - 1] == '等' or words[n - 1] == '等等') and (words[n] != '的'):
                            # print(words[n-1])
                            # print(n)
                            return n  # 返回位置
        return -1

    def getHypernym(self,words, ycjf, cx, now, limit):  # 获取当前词的上位词（考虑并列coo/sasubj/dfsubj）
        n = int(now)
        st =self.getProfix(words, cx, now)
        result = []
        if (st != words[n - 1]) and ('*' not in st) and ('《' not in st):
            result.append([st, cx[n - 1]])
            result.append([words[n - 1], cx[n - 1]])
        else:
            result.append([st, cx[n - 1]])
        flag = 1
        if (flag == 0):
            return -1
        return result

    def getHyponym(self,words, ycjf, cx, now, limit, x):  # 由att获取下位词，考虑coo
        result = []
        flag = 0
        tmp2 = []
        for k in ycjf:  # 防止抽取到无关的att
            tmp1 = []
            if (k[0] == now) and (k[2] == 'att') and (eval(k[3]) > limit):
                tmp1.append(k[1])
                for j in ycjf:
                    if (j[0] == k[1]) and (j[2] == 'adjct') and (eval(j[3]) > limit):
                        n = int(j[1])
                        if (n < len(words)) and (words[n - 1] == '等' or words[n - 1] == '等等') and (
                                words[n] != '的') and (words[n] != '，'):
                            tmp2.append(k[1])
            for m in ycjf:  # 考虑并列词
                if (m[0] in tmp1) and ((m[2] == 'coo') or (m[2] == 'sasubj') or (m[2] == 'dfsubj')) and (
                        eval(k[3]) > limit):
                    tmp1.append(m[1])
                    for j in ycjf:
                        if (j[0] == m[1]) and (j[2] == 'adjct') and (eval(j[3]) > limit):
                            n = int(j[1])
                            if (n < len(words)) and (words[n - 1] == '等' or words[n - 1] == '等等') and (
                                    words[n] != '的') and (words[n] != '，'):
                                tmp2.append(k[1])
        for k in ycjf:
            if (k[0] == now) and (k[1] in tmp2):
                n = int(k[1])
                if n < x:#要在"等"之前
                    st = self.getProfix(words, cx, k[1])
                    result.append([st, cx[n - 1]])
                    flag = 1
                    tmp2.append(k[1])
        for j in ycjf:  # 考虑coo
            if (j[0] in tmp2) and ((j[2] == 'coo') or (j[2] == 'sasubj') or (j[2] == 'dfsubj')) and (
                    eval(j[3]) > limit):
                n = int(j[1])
                if (n < x):#要在"等"之前
                    st = self.getProfix(words, cx, j[1])
                    result.append([st, cx[n - 1]])
                    tmp2.append(j[1])
        if flag == 0:
            return -1
        return result

    def getWordPairs(self,words, cx, ycjf, limit):  # 由依存句法树和置信度限制范围，按照pattern抽取出上下位关系词汇
        result = []
        while True:
            flag = 0
            for i in range(len(ycjf)):
                if ycjf[i] != 'visited':
                    x = self.isPattern(words, str(i + 1), ycjf, limit)
                    if x != -1:  # 判断当前名词是否符合"等"pattern
                        hypernyms = self.getHypernym(words, ycjf, cx, str(i + 1), limit)  # 上位词为"等"后的名词
                        hyponyms = self.getHyponym(words, ycjf, cx, str(i + 1), limit, x)  # 下位词为修饰该名词的名词序列
                        for wp in self.compose(hyponyms, hypernyms):
                            flag = 1
                            result.append(wp)
                        ycjf[i] = 'visited'  # 防止重复访问结点
            if (flag == 0):  # 如果树中没有未访问的符合pattern弧，即可返回结果，否则继续迭代
                return result

    def isSentence(self,sen,words):  # 判断是否是满足pattern的句子
        if ('等' in words) or ('等等' in words):
            # print(sen)
            return True
        return False

def main():
    extraction=SyntacticExtraction_deng()
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/baike_data0.out', 'WordPairs_ycjf_etc_baike0_profix_inDic.txt', 0)
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/baike_data1.out', 'WordPairs_ycjf_etc_baike1_profix_inDic.txt', 0)
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/baike_data2.out', 'WordPairs_ycjf_etc_baike2_profix_inDic.txt', 0)
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/lter_wiki_data_ws_pos_standrad.out','WordPairs_ycjf_etc_wiki_profix_inDic.txt', 0)
#主函数

if __name__ == '__main__':
  main()
#运行主函数