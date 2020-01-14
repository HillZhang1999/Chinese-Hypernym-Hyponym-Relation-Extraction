import LP as father
class LP_deng(father.LP):
    def achieve_useful_sentence(self,baike, useful_sentence):
        """
        根据语料集合，筛选出符合deng模式的语句集合
        :param baike: 语料集合
        :param useful_sentence:符合deng模式的语句集合
        :return:
        """
        pattern_lst = ["等", "等等"]
        infile = open(baike, 'r', encoding='utf-8')
        outfile = open(useful_sentence, 'a+', encoding='utf-8')
        for i in infile:
            st = i[0:len(i) - 1].split()
            for j in pattern_lst:
                if (j in st):
                    outfile.write(i)
                    break
            continue
        infile.close()
        outfile.close()
    def achieve_shangwei(self,hou_lst, hou_cixing_lst, guolv_dic, coo_lst):
        """
        重写了父类中提取上位词的方法，根据分割完以后的后串词列表和词性列表获得上位词候选词
        :param hou_lst: 分割完以后的后串词列表
        :param hou_cixing_lst: 分割完以后的后串词性列表
        :param guolv_dic: 过滤词典
        :param coo_lst: 并列词列表
        :return:
        """
        shangwei_houxuan = []
        for i in guolv_dic:
            if (i in hou_lst):
                return shangwei_houxuan
        tep_lst = hou_lst
        shuminghao_count = []
        for i in range(len(tep_lst) - 1):
            if (tep_lst[i] == "《"):
                for j in range(i + 1, len(tep_lst)):
                    if (tep_lst[j] == "》"):
                        shuminghao_count.append([i, j])
                        break
        ct = -1
        for i in range(len(hou_lst)):
            if (hou_cixing_lst[i] == "VV" or hou_cixing_lst[i] == "VA" or hou_cixing_lst[i] == "VC" or hou_cixing_lst[
                i] == "VE"):
                ct = i
                break
        if (ct != -1):
            hou_lst = hou_lst[0:ct]
            hou_cixing_lst = hou_cixing_lst[0:ct]
        if (len(hou_lst) > 0):
            scount = -1
            shangwei = ""
            zhongxinci = ""
            Replenish = ["有限", "之"]
            DT = ["本", "此", "该", "这"]
            flag1 = 0
            for i in range(len(hou_lst) - 1):
                if (hou_cixing_lst[i] == "NN" or hou_cixing_lst[i] == "NR") and (
                        hou_cixing_lst[i + 1] != "NN" and hou_cixing_lst[i + 1] != "NR"):
                    scount = i
                    shangwei = hou_lst[scount]
                    zhongxinci = shangwei
                    break
            if (scount == -1):
                if (hou_cixing_lst[len(hou_lst) - 1] == "NN") or (hou_cixing_lst[len(hou_lst) - 1] == "NR"):
                    scount = len(hou_lst) - 1
                    shangwei = hou_lst[scount]
                    zhongxinci = shangwei
            if (scount != -1):
                if (len(shuminghao_count) > 0):
                    flag = 1
                    tep_count = tep_lst.index(shangwei)
                    for m in shuminghao_count:
                        if (tep_count < m[1] and tep_count > m[0]):
                            shangwei_lst = tep_lst[m[0] + 1:m[1]]
                            shangwei = "".join(shangwei_lst)
                            flag = 0
                            break
                    if (flag == 1):
                        while (scount - 1 >= 0):
                            if (hou_cixing_lst[scount - 1] == "NN") or (hou_cixing_lst[scount - 1] == "NR") or (
                                        hou_cixing_lst[scount - 1] == "CD") or (hou_lst[scount - 1] in Replenish):
                                scount -= 1
                                shangwei = hou_lst[scount] + shangwei
                                flag1 = 1
                            elif (scount - 2 >= 0 and hou_cixing_lst[scount - 1] == "M" and hou_lst[
                                    scount - 2] in DT) or (
                                        hou_lst[scount - 1] in DT) or (hou_cixing_lst[scount - 1] == "PN") or (
                                                    scount - 2 >= 0 and hou_cixing_lst[scount - 1] == "DEG" and
                                            hou_cixing_lst[
                                                    scount - 2] == "PN"):
                                shangwei = ""
                                break
                            else:
                                break
                else:
                    while (scount - 1 >= 0):
                        if (hou_cixing_lst[scount - 1] == "NN") or (hou_cixing_lst[scount - 1] == "NR") or (
                            hou_cixing_lst[scount - 1] == "CD") or (hou_lst[scount - 1] in Replenish):
                            scount -= 1
                            shangwei = hou_lst[scount] + shangwei
                            flag1 = 1
                        elif (scount - 2 >= 0 and hou_cixing_lst[scount - 1] == "M" and hou_lst[scount - 2] in DT) or (
                            hou_lst[scount - 1] in DT) or (hou_cixing_lst[scount - 1] == "PN") or (
                                        scount - 2 >= 0 and hou_cixing_lst[scount - 1] == "DEG" and hou_cixing_lst[
                                scount - 2] == "PN"):
                            shangwei = ""
                            break
                        else:
                            break
            if (len(shangwei) > 0):
                shangwei_houxuan.append(shangwei)
            if ((flag1 == 1) and (len(zhongxinci) > 0)):
                shangwei_houxuan.append(zhongxinci)
            return shangwei_houxuan
        if (len(hou_lst) == 0):
            return shangwei_houxuan

    def achieve_shangwei_and_xiawei(self,useful_sentence, guolv, shangxiawei_houxuan, tiqu_sentence):
        """
        根据符合deng模式的语句集合，来获得上下位关系候选词对
        :param useful_sentence:符合deng模式的语句结合
        :param guolv:过滤词典
        :param shangxiawei_houxuan:上下位候选词对集合
        :param tiqu_sentence:能够提取出上下位候选词对的语句集合
        :return:
        """

        bianhao = 0
        xushu = 0
        guolv_dic = []
        coo_lst = ["、", "或者", "或", "和", "以及", "与", "及"]
        infile_guolv = open(guolv, 'r', encoding='utf-8-sig')
        for i in infile_guolv:
            guolv_dic.append(i[0:len(i) - 1])
        infile_guolv.close()
        infile = open(useful_sentence, 'r', encoding='utf-8')
        pattern_lst = ["等", "等等"]
        for i in infile:
            xushu += 1
            st = i[0:len(i) - 1]
            ls = st.split()
            count1 = (len(ls) // 2)
            fen_ci_lst = ls[0:count1]
            ci_xing_lst = ls[count1:len(st)]
            every_sentence_lst, every_sentence_cixing_lst = achieve_split_lst(fen_ci_lst, ci_xing_lst)
            shangxiawei_houxuan_lst = []
            for k in range(len(every_sentence_lst)):
                sentence_lst = every_sentence_lst[k]
                sentence_cixing_lst = every_sentence_cixing_lst[k]
                for j in pattern_lst:
                    if (j in sentence_lst):
                        count = sentence_lst.index(j)
                        if (sentence_cixing_lst[count] == "ETC" and count != (len(sentence_lst) - 1) and sentence_lst[
                                count + 1] != "的"):
                            qian_lst = sentence_lst[0:count]
                            hou_lst = sentence_lst[count + 1:len(sentence_lst)]
                            qian_cixing_lst = sentence_cixing_lst[0:len(qian_lst)]
                            hou_cixing_lst = sentence_cixing_lst[count + 1:len(sentence_lst)]
                            shangwei_houxuan = achieve_shangwei(hou_lst, hou_cixing_lst, guolv_dic, coo_lst)
                            xiawei_houxuan = achieve_xiawei(qian_lst, qian_cixing_lst, guolv_dic, coo_lst)
                            if (len(shangwei_houxuan) > 0 and len(xiawei_houxuan) > 0):
                                for m in shangwei_houxuan:
                                    for n in xiawei_houxuan:
                                        if (m != n):
                                            shangxiawei_houxuan_lst.append(n + " " + m)
                            break
            if (len(shangxiawei_houxuan_lst) > 0):
                outfile_juzi = open(tiqu_sentence, 'a+', encoding='utf-8')
                outfile_juzi.write(i)
                bianhao += 1
                outfile_juzi.close()
                print("目前已经扫描了" + str(xushu) + "句，能够提取出上下位关系的句子有" + str(bianhao) + "句，其上下位候选词对如下：")
                outfile_shangxiawei = open(shangxiawei_houxuan, 'a+', encoding='utf-8')
                for m in shangxiawei_houxuan_lst:
                    outfile_shangxiawei.write(m + " " + str(bianhao) + "\n")
                    print(m + " " + str(bianhao))
                outfile_shangxiawei.close()
            else:
                print("目前已经扫描了" + str(xushu) + "句，该句不能提取出上下位关系")
        infile.close()