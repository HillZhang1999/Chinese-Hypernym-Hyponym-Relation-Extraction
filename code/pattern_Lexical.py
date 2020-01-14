class LP(object):
    def achieve_split_lst(self,lst, cixing_lst):
        """
        句子分割函数，根据分割列表，将句子分割成一个一个部分，同时也将每个词的词性分成一个一个部分；
        :param lst:分词过后的词列表
        :param cixing_lst:分词过后的词性列表
        :return:分割完后的词列表和词性列表
        """
        fenge_lst = ["，", "！", "；", "。", ",", "!", ".", ";"]
        cot = 0
        ct = cot
        every_sentence_lst = []
        every_sentence_cixing_lst = []
        while (cot < len(lst)):
            for m in fenge_lst:
                if (m == lst[cot]):
                    every_sentence_lst.append(lst[ct:cot])
                    every_sentence_cixing_lst.append(cixing_lst[ct:cot])
                    ct = cot + 1
                else:
                    continue
            cot += 1
        every_sentence_lst.append(lst[ct:cot])
        every_sentence_cixing_lst.append(cixing_lst[ct:cot])
        return every_sentence_lst, every_sentence_cixing_lst

    def achieve_xiawei(self,qian_lst, qian_cixing_lst, guolv_dic, coo_lst):
        """
        根据分割完以后且在模式之前的词列表和词性列表来获得可能的下位词列表
        :param qian_lst:模式之前的词列表，前串
        :param qian_cixing_lst:模式之前的词性列表，前串词性列表
        :param guolv_dic:过滤词典
        :param coo_lst:并列词列表
        :return:下位词候选词
        """
        xiawei_houxuan = []
        for i in guolv_dic:
            if (i in qian_lst):
                return xiawei_houxuan
        tep_lst = qian_lst
        shuminghao_count = []
        for i in range(len(tep_lst) - 1):
            if (tep_lst[i] == "《"):
                for j in range(i + 1, len(tep_lst)):
                    if (tep_lst[j] == "》"):
                        shuminghao_count.append([i, j])
                        break
        if ("的" in qian_lst):
            qian_lst = qian_lst[::-1]
            qian_cixing_lst = qian_cixing_lst[::-1]
            cot = qian_lst.index("的")
            if (cot + 1 < len(qian_lst) and qian_cixing_lst[cot + 1] == "PN"):
                return xiawei_houxuan
            qian_lst = qian_lst[0:cot]
            qian_cixing_lst = qian_cixing_lst[0:cot]
            qian_lst = qian_lst[::-1]
            qian_cixing_lst = qian_cixing_lst[::-1]
        cott = 0
        ct = cott
        qian_lst_he = []
        qian_cixing_lst_he = []
        while (cott < len(qian_lst)):
            for m in coo_lst:
                if (m == qian_lst[cott]):
                    qian_lst_he.append(qian_lst[ct:cott])
                    qian_cixing_lst_he.append(qian_cixing_lst[ct:cott])
                    ct = cott + 1
                else:
                    continue
            cott += 1
        qian_lst_he.append(qian_lst[ct:cott])
        qian_cixing_lst_he.append(qian_cixing_lst[ct:cott])
        Replenish = ["有限", "之"]
        DT = ["本", "此", "该", "这"]
        for i in range(len(qian_lst_he)):
            ddt1 = qian_lst_he[i][::-1]
            ddt1_pos = qian_cixing_lst_he[i][::-1]
            if (len(ddt1) > 0):
                if ("LC" in ddt1_pos and "P" in ddt1_pos):
                    lc = ddt1_pos.index("LC")
                    p = ddt1_pos.index("P")
                    if (lc != -1 and p != -1):
                        if (p > lc):
                            temp = ddt1[p + 1:]
                            ddt1 = ddt1[0:lc]
                            for k in temp:
                                ddt1.append(k)
                            temp_lst = ddt1_pos[p + 1:]
                            ddt1_pos = ddt1_pos[0:lc]
                            for k in temp_lst:
                                ddt1_pos.append(k)
                xiawei = ""
                scount = -1
                for j in range(len(ddt1)):
                    if (ddt1_pos[j] == "NN" or ddt1_pos[j] == "NR"):
                        xiawei += ddt1[j]
                        scount = j
                        break
                if (scount != -1):
                    if (len(shuminghao_count) > 0):
                        flag = 1
                        tep_count = tep_lst.index(xiawei)
                        for m in shuminghao_count:
                            if (tep_count < m[1] and tep_count > m[0]):
                                xiawei_lst = tep_lst[m[0] + 1:m[1]]
                                xiawei = "".join(xiawei_lst)
                                flag = 0
                                break
                        if (flag == 1):
                            while (scount + 1 < len(ddt1)):
                                if (ddt1_pos[scount + 1] == "NN") or (ddt1_pos[scount + 1] == "NR") or (
                                            ddt1_pos[scount + 1] == "CD") or (ddt1[scount + 1] in Replenish):
                                    scount += 1
                                    xiawei = ddt1[scount] + xiawei
                                elif (scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "M" and ddt1[
                                        scount + 2] in DT) or (ddt1[scount + 1] in DT) or (
                                            ddt1_pos[scount + 1] == "PN") or (
                                                        scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "DEG" and
                                                ddt1_pos[
                                                        scount + 2] == "PN"):
                                    xiawei = ""
                                    break
                                else:
                                    break
                    else:
                        while (scount + 1 < len(ddt1)):
                            if (ddt1_pos[scount + 1] == "NN") or (ddt1_pos[scount + 1] == "NR") or (
                                        ddt1_pos[scount + 1] == "CD") or (ddt1[scount + 1] in Replenish):
                                scount += 1
                                xiawei = ddt1[scount] + xiawei
                            elif (scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "M" and ddt1[
                                    scount + 2] in DT) or (ddt1[scount + 1] in DT) or (
                                        ddt1_pos[scount + 1] == "PN") or (
                                                    scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "DEG" and
                                            ddt1_pos[
                                                    scount + 2] == "PN"):
                                xiawei = ""
                                break
                            else:
                                break
                if (len(xiawei) > 0):
                    xiawei_houxuan.append(xiawei)
        return xiawei_houxuan

    def achieve_shangwei(self,hou_lst, hou_cixing_lst, guolv_dic, coo_lst):
        """
        根据分割完以后的后串词列表和词性列表获得上位词候选词
        :param hou_lst:分割完以后的后串词列表
        :param hou_cixing_lst:分割完以后的后串词性列表
        :param guolv_dic:过滤词典
        :param coo_lst:并列词列表
        :return:上位词候选词
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
        if ("的" in hou_lst):
            hou_lst = hou_lst[::-1]
            hou_cixing_lst = hou_cixing_lst[::-1]
            cot = hou_lst.index("的")
            if (cot + 1 < len(hou_lst) and hou_cixing_lst[cot + 1] == "PN"):
                return shangwei_houxuan
            hou_lst = hou_lst[0:cot]
            hou_cixing_lst = hou_cixing_lst[0:cot]
            hou_lst = hou_lst[::-1]
            hou_cixing_lst = hou_cixing_lst[::-1]
        cott = 0
        ct = cott
        hou_lst_he = []
        hou_cixing_lst_he = []
        while (cott < len(hou_lst)):
            for m in coo_lst:
                if (m == hou_lst[cott]):
                    hou_lst_he.append(hou_lst[ct:cott])
                    hou_cixing_lst_he.append(hou_cixing_lst[ct:cott])
                    ct = cott + 1
                else:
                    continue
            cott += 1
        hou_lst_he.append(hou_lst[ct:cott])
        hou_cixing_lst_he.append(hou_cixing_lst[ct:cott])
        Replenish = ["有限", "之"]
        DT = ["本", "此", "该", "这"]
        for i in range(len(hou_lst_he)):
            ddt1 = hou_lst_he[i][::-1]
            ddt1_pos = hou_cixing_lst_he[i][::-1]
            if (len(ddt1) > 0):
                flag1 = 0
                if ("LC" in ddt1_pos and "P" in ddt1_pos):
                    lc = ddt1_pos.index("LC")
                    p = ddt1_pos.index("P")
                    if (lc != -1 and p != -1):
                        if (p > lc):
                            temp = ddt1[p + 1:]
                            ddt1 = ddt1[0:lc]
                            for k in temp:
                                ddt1.append(k)
                            temp_lst = ddt1_pos[p + 1:]
                            ddt1_pos = ddt1_pos[0:lc]
                            for k in temp_lst:
                                ddt1_pos.append(k)
                shangwei = ""
                zhongxinci = ""
                scount = -1
                for i in range(len(ddt1)):
                    if (ddt1_pos[i] == "NN" or ddt1_pos[i] == "NR"):
                        shangwei += ddt1[i]
                        zhongxinci = shangwei
                        scount = i
                        break
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
                            while (scount + 1 < len(ddt1)):
                                if (ddt1_pos[scount + 1] == "NN") or (ddt1_pos[scount + 1] == "NR") or (
                                            ddt1_pos[scount + 1] == "CD") or (ddt1[scount + 1] in Replenish):
                                    scount += 1
                                    shangwei = ddt1[scount] + shangwei
                                    print(shangwei)
                                    flag1 = 1
                                elif (scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "M" and ddt1[
                                        scount + 2] in DT) or (ddt1[scount + 1] in DT) or (
                                            ddt1_pos[scount + 1] == "PN") or (
                                                        scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "DEG" and
                                                ddt1_pos[
                                                        scount + 2] == "PN"):
                                    shangwei = ""
                                    break
                                else:
                                    break
                    else:
                        while (scount + 1 < len(ddt1)):
                            if (ddt1_pos[scount + 1] == "NN") or (ddt1_pos[scount + 1] == "NR") or (
                                        ddt1_pos[scount + 1] == "CD") or (ddt1[scount + 1] in Replenish):
                                scount += 1
                                shangwei = ddt1[scount] + shangwei
                                flag1 = 1
                            elif (scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "M" and ddt1[
                                    scount + 2] in DT) or (
                                        ddt1[scount + 1] in DT) or (ddt1_pos[scount + 1] == "PN") or (
                                                    scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "DEG" and
                                            ddt1_pos[
                                                    scount + 2] == "PN"):
                                shangwei = ""
                                break
                            else:
                                break
                if (len(shangwei) > 0):
                    shangwei_houxuan.append(shangwei)
                if (flag1 == 1 and len(zhongxinci) > 0):
                    shangwei_houxuan.append(zhongxinci)
        return shangwei_houxuan
    def achieve_cidui_in_cidian(self,cidui_houxuan, cidui_houxuan_in_dic_include, dic):
        """
        筛选出上位词和下位词同时在八万个词词典中的上下位候选词对，同时删去上位词和下位词一样的词对
        :param cidui_houxuan: 上下位词对候选集合
        :param cidui_houxuan_in_dic_include: 在词典中的上下位词对候选集合
        :param dic: 八万个词的词典集合
        :return:
        """
        infile1 = open(dic, 'r', encoding='utf-8')
        dic = []
        for i in infile1:
            dic.append(i[0:len(i) - 1])
        infile1.close()
        infile2 = open(cidui_houxuan, 'r', encoding='utf-8')
        count = 0
        scount = 0
        for i in infile2:
            count += 1
            i = i[0:len(i) - 1]
            st = i.split()
            xiawei = st[0]
            shangwei = st[1]
            if (shangwei in dic and xiawei in dic):
                scount += 1
                outfile = open(cidui_houxuan_in_dic_include, 'a+', encoding='utf-8')
                outfile.write(i + "\n")
                outfile.close()
                print("目前正在检测第" + str(count) + "个词对，该词对在词典中，目前共有" + str(
                    scount) + "个词对在词典中，该词对为" + shangwei + " " + xiawei)
            else:
                print("目前正在检测第" + str(count) + "个词对，该词对不在词典中，进入下一个词对！")
        infile2.close()

    def guolv_shangwei_and_xiawei(self,dictGL, HYpernym, shangxiawei_houxuan, shangxiawei_houxuan_after_shaixuan):
        """
        第二次筛选，我们重新定义了一个上位词集合，里面有一些常规的上位词，同时我们建立了过滤词典，对于在过滤词典中的上下位词，我们直接进行了删除！
        :param dictGL: 过滤词典
        :param HYpernym: 上位词词典
        :param shangxiawei_houxuan:上下位词对候选集合
        :param shangxiawei_houxuan_after_shaixuan: 经过筛选后的上下位词对候选集合
        :return:
        """
        infile1 = open(dictGL, "r", encoding="utf-8")
        dicGL = {}
        for i in infile1:
            if (i[0:len(i) - 1] in dicGL.keys()):
                dicGL[i[0:len(i) - 1]] += 1
            else:
                dicGL[i[0:len(i) - 1]] = 1
        infile1.close()
        HYpernym_dic = {}
        infile2 = open(HYpernym, "r", encoding="utf-8")
        for i in infile2:
            if (i[0:len(i) - 1] in HYpernym_dic.keys()):
                HYpernym_dic[i[0:len(i) - 1]] += 1
            else:
                HYpernym_dic[i[0:len(i) - 1]] = 1
        infile2.close()
        shangxiawei_houxuan_st = open(shangxiawei_houxuan, "r", encoding="utf-8")
        for i in shangxiawei_houxuan_st:
            st = i[0:len(i) - 1]
            lst = st.split()
            xiawei = lst[0]
            shangwei = lst[1]
            if (
                            shangwei in HYpernym_dic.keys() and shangwei not in dicGL and xiawei not in dicGL and xiawei not in shangwei):
                outfile = open(shangxiawei_houxuan_after_shaixuan, "a+", encoding="utf-8")
                outfile.write(i)
                outfile.close()
        shangxiawei_houxuan_st.close()