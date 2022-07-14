# -*- coding: utf-8 -*-

from competition.models import ChoiceInfo, FillInBlankInfo


def check_correct_num(rlist):
    if isinstance(rlist, list):
        total = len(rlist)
        correct = 0
        state_list = []
        replay_list=[]
        choice_list= ['A','B','C','D']

        for i in rlist:
            if isinstance(i, str):
                i = i.split(',')
                t = i[0][0]  # qtype
                p = i[0][2:]  # pk
                v = i[1]  # answer
                # 转换类型
                try:
                    pk = int(p)
                except ValueError:
                    continue
                # 判断题目类型
                # c:选择
                # t:填空
                if t == 'c':
                    try:
                        c = ChoiceInfo.objects.get(pk=pk)
                    except ChoiceInfo.DoesNotExist:
                        continue

                    if v in choice_list:
                        item='c.item' + str(choice_list.index(v)+1)
                        answer=str(eval(item))
                        if answer == str(c.answer):
                            correct += 1
                            state_list.append(1)
                        else:
                            state_list.append(0)
                        replay_list.append(answer)
                    else:
                        state_list.append(0)
                        replay_list.append('无')

                elif t == 'f':
                    try:
                        f = FillInBlankInfo.objects.get(pk=pk)
                    except FillInBlankInfo.DoesNotExist:
                        continue

                    if v.strip() == f.answer:
                        correct += 1
                        state_list.append(1)
                        replay_list.append(v.strip())
                    else:
                        state_list.append(0)
                        if v.strip()!='':
                            replay_list.append(v.strip())
                        else:
                            replay_list.append('无')

        wrong = total - correct
        return total, correct, wrong, state_list,replay_list

    return 0, 0, 0, [], []
