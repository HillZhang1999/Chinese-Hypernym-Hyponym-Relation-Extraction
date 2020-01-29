import pattern_Syntactic_isA as father
import pattern_Syntactic_deng as Extraction_deng

class SyntacticExtraction_oneOf(father.SyntacticExtraction_isA):
    def isPattern(self,words, now, ycjf, limit):  # 判断当前的谓语是否满足pattern
        if (int(now) - 1 > 0 and ("（" == words[int(now) - 2] or "(" == words[int(now) - 2])):
            return False
        if (int(now) < len(words)):
            for w in self.Is:
                if (w == words[int(now) - 1]):
                    for k in ycjf:
                        if (k[0] == now) and (k[2] == 'adv') and (eval(k[3]) > limit):
                            n = int(k[1])
                            if (words[n - 1] in self.ADVfilter):
                                return False
                    for k in ycjf:
                        if (k[0] == now) and (k[2] == 'obj') and (eval(k[3]) > limit):
                            n = int(k[1])
                            if (words[n - 2] + words[n - 1] in self.oneOf) or (words[n - 1] in self.oneOf):
                                return True
        return False

    def getObj(self,words, ycjf, cx, now, limit):  # 获取当前谓语弧的宾语（考虑并列coo）
        result = []
        flag = 0
        tmp1 = []
        tmp2 = []
        for i in ycjf:
            if (i[0] == now) and (i[2] == 'obj') and (eval(i[3]) > limit):
                if words[int(i[1]) - 2] + words[int(i[1]) - 1] in self.oneOf or words[int(i[1]) - 1] in self.oneOf:
                    tmp1.append(i[1])
        for k in ycjf:
            if (k[0] in tmp1) and (k[2] == 'att') and (eval(k[3]) > limit):
                n = int(k[1])
                st = self.getProfix(words, cx, k[1])
                if (st != words[n - 1]) and ('*' not in st) and ('《' not in st):
                    result.append([st, cx[n - 1]])
                    result.append([words[n - 1], cx[n - 1]])
                else:
                    result.append([st, cx[n - 1]])
                tmp2.append(i[1])
                flag = 1
        for j in ycjf:  # 考虑coo
            if (j[0] in tmp2) and ((j[2] == 'coo') or (j[2] == 'sasubj') or (j[2] == 'dfsubj')) and (
                    eval(j[3]) > limit):
                n = int(j[1])
                st = self.getProfix(words, cx, j[1])
                if (st != words[n - 1]) and ('*' not in st) and ('《' not in st):
                    result.append([st, cx[n - 1]])
                    result.append([words[n - 1], cx[n - 1]])
                else:
                    result.append([st, cx[n - 1]])
                tmp2.append(j[1])
        if flag == 0:
            return -1
        return result

    def isSentence(self,sen,words):  # 判断是否是满足pattern的句子
        for w in self.Is:
            for ww in self.oneOf:
                if (w in sen) and (ww in sen) and (sen.index(w) < sen.index(ww)):
                    return True
        return False

def main():
    extraction = SyntacticExtraction_oneOf()
    #extraction.saveWordPairs('wiki_test_data', 'WordPairs_ycjf_oneOf_profix_inDic.txt', 0)
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/baike_data0.out', 'WordPairs_ycjf_oneOf_baike0_profix_inDic.txt', 0)
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/baike_data1.out', 'WordPairs_ycjf_oneOf_baike1_profix_inDic.txt', 0)
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/baike_data2.out', 'WordPairs_ycjf_oneOf_baike2_profix_inDic.txt', 0)
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/lter_wiki_data_ws_pos_standrad.out', 'WordPairs_ycjf_oneOf_wiki_profix_inDic.txt', 0)
    #chooseWordPairs('WordPairs-ycjf.txt', 'ycjf-result.txt', 'words.conll')
#主函数

if __name__ == '__main__':
  main()
#运行主函数