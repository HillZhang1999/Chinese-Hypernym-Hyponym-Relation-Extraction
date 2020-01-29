import pattern_Syntactic as father
import pattern_Syntactic_deng as Extraction_deng

class SyntacticExtraction_isA(father.SyntacticExtraction):
    deng = Extraction_deng.SyntacticExtraction_deng()
    def isPattern(self,words, now, ycjf, limit):  # 判断当前的谓语是否满足pattern
        if (int(now) - 1 > 0 and ("（" == words[int(now) - 2] or "(" == words[int(now) - 2])):
            return False
        liangci = self.readFile('ATTquantifier')
        if (int(now) < len(words) - 2):
            for w in self.Is:
                if (w == words[int(now) - 1]) and (
                        words[int(now)] + words[int(now) + 1] in liangci or words[int(now)] in liangci):
                    for k in ycjf:
                        if (k[0] == now) and (k[2] == 'adv') and (eval(k[3]) > limit):
                            n = int(k[1])
                            if (words[n - 1] in self.ADVfilter):
                                return False
                    return True
        return False

    def getSubj(self,words, ycjf, cx, now, limit):  # 获取当前谓语弧的主语（考虑并列coo）
        result = []
        flag = 0
        tmp = []
        for k in ycjf:
            if (k[0] == now) and (k[2] == 'subj') and (eval(k[3]) > limit):
                n = int(k[1])
                st = self.getProfix(words, cx, k[1])
                x = self.deng.isPattern(words, k[1], ycjf, limit)
                if x != -1:  # 判断当前名词是否符合"等"pattern
                    hyponyms = self.deng.getHyponym(words, ycjf, cx, k[1], limit, x)  # 下位词为修饰该名词的名词序列
                    if hyponyms == -1:
                        result.append([st, cx[n - 1]])
                    else:
                        for wp in hyponyms:
                            result.append(wp)
                else:
                    result.append([st, cx[n - 1]])
                flag = 1
                tmp.append(k[1])
        for j in ycjf:  # 考虑coo
            if (j[0] in tmp) and ((j[2] == 'coo') or (j[2] == 'sasubj') or (j[2] == 'dfsubj')) and (eval(j[3]) > limit):
                n = int(j[1])
                st = self.getProfix(words, cx, j[1])
                x = self.deng.isPattern(words, j[1], ycjf, limit)
                if x != -1:  # 判断当前名词是否符合"等"pattern
                    hyponyms = self.deng.getHyponym(words, ycjf, cx, j[1], limit, x)  # 下位词为修饰该名词的名词序列
                    if hyponyms == -1:
                        result.append([st, cx[n - 1]])
                    else:
                        for wp in hyponyms:
                            result.append(wp)
                else:
                    result.append([st, cx[n - 1]])
                tmp.append(j[1])
        if flag == 0:
            return -1
        return result



    def getObj(self,words, ycjf, cx, now, limit):  # 获取当前谓语弧的宾语（考虑并列coo）
        result = []
        flag = 0
        tmp = []
        for k in ycjf:
            if (k[0] == now) and (k[2] == 'obj') and (eval(k[3]) > limit):
                n = int(k[1])
                st = self.getProfix(words, cx, k[1])
                if (st != words[n - 1]) and ('*' not in st) and ('《' not in st):
                    result.append([st, cx[n - 1]])
                    result.append([words[n - 1], cx[n - 1]])
                else:
                    result.append([st, cx[n - 1]])
                flag = 1
                tmp.append(k[1])
        for j in ycjf:  # 考虑coo
            if (j[0] in tmp) and ((j[2] == 'coo') or (j[2] == 'sasubj') or (j[2] == 'dfsubj')) and (eval(j[3]) > limit):
                n = int(j[1])
                st = self.getProfix(words, cx, j[1])
                if (st != words[n - 1]) and ('*' not in st) and ('《' not in st):
                    result.append([st, cx[n - 1]])
                    result.append([words[n - 1], cx[n - 1]])
                else:
                    result.append([st, cx[n - 1]])
                tmp.append(j[1])
        if flag == 0:
            return -1
        return result

    def getWordPairs(self,words, cx, ycjf, limit):  # 由依存句法树和置信度限制范围，按照pattern抽取出上下位关系词汇
        subjs = -1  # 考虑到同主语的情况，先保存主语
        result = []
        while True:
            flag = 0
            for i in range(len(ycjf)):
                tmp = ycjf[i]
                if (tmp[2] == 'root') and (eval(tmp[3]) > limit):  # 谓语做root的情况（需要先找主语）
                    li = [tmp[1]]  # 同主语谓语弧池
                    subjs = self.getSubj(words, ycjf, cx, tmp[1], limit)
                    ycjf[i] = 'visited'  # 防止重复访问结点
                    if (self.isPattern(words, tmp[1], ycjf, 0)):
                        objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                        for wp in (self.compose(subjs, objs)):
                            flag = 1
                            result.append(wp)
                    for j in range(len(ycjf)):
                        tmp = ycjf[j]
                        if (tmp[0] in li) and (tmp[2] == 'sasubj') and (eval(tmp[3]) > limit):  # 谓语做sasubj的情况（主语不变）
                            li.append(tmp[1])
                            ycjf[j] = 'visited'  # 防止重复访问结点
                            if (self.isPattern(words, tmp[1], ycjf, 0)):
                                objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                                for wp in (self.compose(subjs, objs)):
                                    flag = 1
                                    result.append(wp)
                        elif (tmp[0] in li) and (tmp[2] == 'sasubj-obj') and (
                                eval(tmp[3]) > limit):  # 谓语做sasubj-obj的情况（主语不变）
                            li.append(tmp[1])
                            ycjf[j] = 'visited'  # 防止重复访问结点
                            if (self.isPattern(words, tmp[0], ycjf, 0)) or (self.isPattern(words, tmp[1], ycjf, 0)):
                                if self.getObj(words, ycjf, cx, tmp[0], limit) == -1:
                                    objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                                elif self.getObj(words, ycjf, cx, tmp[1], limit) == -1:
                                    objs = self.getObj(words, ycjf, cx, tmp[0], limit)
                                else:
                                    objs = self.getObj(words, ycjf, cx, tmp[0], limit) + self.getObj(words, ycjf, cx, tmp[1],
                                                                                           limit)
                                for wp in (self.compose(subjs, objs)):
                                    flag = 1
                                    result.append(wp)
                elif (tmp[2] == 'dfsubj') and (eval(tmp[3]) > limit):  # 谓语做dfsubj的情况（主语需要重新找）
                    li = [tmp[1]]  # 同主语谓语弧池
                    subjs = self.getSubj(words, ycjf, cx, tmp[1], limit)
                    ycjf[i] = 'visited'  # 防止重复访问结点
                    if (self.isPattern(words, tmp[1], ycjf, 0)):
                        objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                        for wp in (self.compose(subjs, objs)):
                            flag = 1
                            result.append(wp)
                    for j in range(len(ycjf)):
                        tmp = ycjf[j]
                        if (tmp[0] in li) and (tmp[2] == 'sasubj') and (eval(tmp[3]) > limit):  # 谓语做sasubj的情况（主语不变）
                            li.append(tmp[1])
                            ycjf[j] = 'visited'  # 防止重复访问结点
                            if (self.isPattern(words, tmp[1], ycjf, 0)):
                                objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                                for wp in (self.compose(subjs, objs)):
                                    flag = 1
                                    result.append(wp)
                        elif (tmp[0] in li) and (tmp[2] == 'sasubj-obj') and (
                                eval(tmp[3]) > limit):  # 谓语做sasubj-obj的情况（主语不变）
                            li.append(tmp[1])
                            ycjf[j] = 'visited'  # 防止重复访问结点
                            if (self.isPattern(words, tmp[0], ycjf, 0)) or (self.isPattern(words, tmp[1], ycjf, 0)):
                                if self.getObj(words, ycjf, cx, tmp[0], limit) == -1:
                                    objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                                elif self.getObj(words, ycjf, cx, tmp[1], limit) == -1:
                                    objs = self.getObj(words, ycjf, cx, tmp[0], limit)
                                else:
                                    objs = self.getObj(words, ycjf, cx, tmp[0], limit) + self.getObj(words, ycjf, cx, tmp[1],
                                                                                           limit)
                                for wp in (self.compose(subjs, objs)):
                                    flag = 1
                                    result.append(wp)
                elif (tmp[2] == 'obj' or tmp[2] == 'exp') and (eval(tmp[3]) > limit):  # 谓语也有可能是宾语
                    li = [tmp[1]]  # 同主语谓语弧池
                    if (self.getSubj(words, ycjf, cx, tmp[1], limit) != -1):
                        subjs = self.getSubj(words, ycjf, cx, tmp[1], limit)
                    if (self.isPattern(words, tmp[1], ycjf, 0)):
                        ycjf[i] = 'visited'  # 防止重复访问结点
                        objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                        for wp in (self.compose(subjs, objs)):
                            result.append(wp)
                            flag = 1
                    for j in range(len(ycjf)):
                        tmp = ycjf[j]
                        if (tmp[0] in li) and (tmp[2] == 'sasubj') and (eval(tmp[3]) > limit):  # 谓语做sasubj的情况（主语不变）
                            li.append(tmp[1])
                            ycjf[j] = 'visited'  # 防止重复访问结点
                            if (self.isPattern(words, tmp[1], ycjf, 0)):
                                objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                                for wp in (self.compose(subjs, objs)):
                                    flag = 1
                                    result.append(wp)
                        elif (tmp[0] in li) and (tmp[2] == 'sasubj-obj') and (
                                eval(tmp[3]) > limit):  # 谓语做sasubj-obj的情况（主语不变）
                            li.append(tmp[1])
                            ycjf[j] = 'visited'  # 防止重复访问结点
                            if (self.isPattern(words, tmp[0], ycjf, 0)) or (self.isPattern(words, tmp[1], ycjf, 0)):
                                if self.getObj(words, ycjf, cx, tmp[0], limit) == -1:
                                    objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                                elif self.getObj(words, ycjf, cx, tmp[1], limit) == -1:
                                    objs = self.getObj(words, ycjf, cx, tmp[0], limit)
                                else:
                                    objs = self.getObj(words, ycjf, cx, tmp[0], limit) + self.getObj(words, ycjf, cx, tmp[1],
                                                                                           limit)
                                for wp in (self.compose(subjs, objs)):
                                    flag = 1
                                    result.append(wp)
                elif (tmp[2] == 'pred') and (eval(tmp[3]) > limit):  # 谓语也有可能是宾语
                    li = [tmp[1]]  # 同主语谓语弧池
                    st = self.getProfix(words, cx, tmp[0])
                    subjs = []
                    if (st != words[int(tmp[0]) - 1]) and ('*' not in st) and ('《' not in st):
                        subjs.append([st, cx[int(tmp[0]) - 1]])
                    else:
                        subjs.append([st, cx[int(tmp[0]) - 1]])
                    if (self.isPattern(words, tmp[1], ycjf, 0)):
                        ycjf[i] = 'visited'  # 防止重复访问结点
                        objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                        for wp in (self.compose(subjs, objs)):
                            result.append(wp)
                            flag = 1
                    for j in range(len(ycjf)):
                        tmp = ycjf[j]
                        if (tmp[0] in li) and (tmp[2] == 'sasubj') and (eval(tmp[3]) > limit):  # 谓语做sasubj的情况（主语不变）
                            li.append(tmp[1])
                            ycjf[j] = 'visited'  # 防止重复访问结点
                            if (self.isPattern(words, tmp[1], ycjf, 0)):
                                objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                                for wp in (self.compose(subjs, objs)):
                                    flag = 1
                                    result.append(wp)
                        elif (tmp[0] in li) and (tmp[2] == 'sasubj-obj') and (
                                eval(tmp[3]) > limit):  # 谓语做sasubj-obj的情况（主语不变）
                            li.append(tmp[1])
                            ycjf[j] = 'visited'  # 防止重复访问结点
                            if (self.isPattern(words, tmp[0], ycjf, 0)) or (self.isPattern(words, tmp[1], ycjf, 0)):
                                if self.getObj(words, ycjf, cx, tmp[0], limit) == -1:
                                    objs = self.getObj(words, ycjf, cx, tmp[1], limit)
                                elif self.getObj(words, ycjf, cx, tmp[1], limit) == -1:
                                    objs = self.getObj(words, ycjf, cx, tmp[0], limit)
                                else:
                                    objs = self.getObj(words, ycjf, cx, tmp[0], limit) + self.getObj(words, ycjf, cx, tmp[1],
                                                                                           limit)
                                for wp in (self.compose(subjs, objs)):
                                    flag = 1
                                    result.append(wp)
            if (flag == 0):  # 如果树中没有未访问的符合pattern谓语弧，即可返回结果，否则继续迭代
                return result

    def isSentence(self,sen,words):  # 判断是否是满足pattern的句子
        for w in self.Is:
            for i in self.yi:
                if (w + i) in sen:
                    #print(sen)
                    return True
        return False

def main():
    extraction=SyntacticExtraction_isA()
    #extraction.saveWordPairs('wiki_test_data', 'WordPairs_ycjf_isA_profix_inDic1.txt', 0)
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/baike_data0.out', 'WordPairs_ycjf_isA_baike0_profix_inDic.txt', 0)
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/baike_data1.out', 'WordPairs_ycjf_isA_baike1_profix_inDic.txt', 0)
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/baike_data2.out', 'WordPairs_ycjf_isA_baike2_profix_inDic.txt', 0)
    extraction.saveWordPairs('/data/zhangyue19/tolukaihua/lter_wiki_data_ws_pos_standrad.out','WordPairs_ycjf_isA_wiki_profix_inDic.txt', 0)
#主函数

if __name__ == '__main__':
  main()
#运行主函数