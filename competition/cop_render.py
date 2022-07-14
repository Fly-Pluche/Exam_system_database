# -*- coding: utf-8 -*-

import json
import random
import collections

from django.shortcuts import render
from TimeConvert import TimeConvert as tc
from account.models import Profile
from competition.models import BankInfo, CompetitionKindInfo, CompetitionQAInfo, ChoiceInfo, FillInBlankInfo
from utils.decorators import check_copstatus, check_login
from utils.errors import (BankInfoNotFound, CompetitionNotFound,
                          ProfileNotFound, QuestionLogNotFound,
                          QuestionNotSufficient, CompetitionError)
from utils.redis.rpageconfig import get_pageconfig, get_form_regex
from utils.redis.rprofile import get_enter_userinfo
from utils.redis.rrank import get_rank, get_rank_data
from utils.response import json_response

import datetime


def home(request):
    """
    比赛首页首页视图
    :param request: 请求对象
    :return: 渲染视图: user_info: 用户信息; kind_info: 比赛信息;is_show_userinfo: 是否展示用户信息表单;user_info_has_entered: 是否已经录入表单;
             userinfo_fields: 表单字段;option_fields: 表单字段中呈现为下拉框的字段;
    """
    uid = request.GET.get('uid', '')  # 获取uid
    kind_id = request.GET.get('kind_id', '')  # 获取kind_id
    created = request.GET.get('created', '0')  # 获取标志位，以后会用到
    try:  # 获取比赛数据
        kind_info = CompetitionKindInfo.objects.get(kind_id=kind_id)
    except CompetitionKindInfo.DoesNotExist:  # 不存在渲染错误视图
        return render(request, 'err.html', CompetitionNotFound)
    try:  # 获取题库数据
        bank_info = BankInfo.objects.get(bank_id=kind_info.bank_id)
    except BankInfo.DoesNotExist:  # 不存在渲染错误视图
        return render(request, 'err.html', BankInfoNotFound)
    try:  # 获取用户数据
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:  # 不存在渲染错误视图
        return render(request, 'err.html', ProfileNotFound)
    if kind_info.question_num > bank_info.total_question_num:  # 比赛出题数量是否小于题库总大小
        return render(request, 'err.html', QuestionNotSufficient)
    show_info = get_pageconfig(kind_info.app_id).get('show_info', {})  # 从redis获取页面配置信息
    is_show_userinfo = show_info.get('is_show_userinfo', False)  # 页面配置信息，用来控制答题前是否展示一张表单
    form_fields = collections.OrderedDict()  # 生成一个有序的用来保存表单字段的字典
    form_regexes = []  # 生成一个空的正则表达式列表
    if is_show_userinfo:
        userinfo_fields = show_info.get('userinfo_fields', '').split('#')  # 从页面配置中获取userinfo_fields
        for i in userinfo_fields:  # 将页面配置的每个正则表达式取出来放入正则表达式列表
            form_regexes.append(get_form_regex(i))
        userinfo_field_names = show_info.get('userinfo_field_names', '').split('#')
        for i in range(len(userinfo_fields)):  # 将每个表单字段信息保存到有序的表单字段字典中
            form_fields.update({userinfo_fields[i]: userinfo_field_names[i]})
    return render(request, 'competition/index.html', {  # 渲染页面
        'user_info': profile.data,
        'kind_info': kind_info.data,
        'bank_info': bank_info.data,
        'is_show_userinfo': 'true' if is_show_userinfo else 'false',
        'userinfo_has_enterd': 'true' if get_enter_userinfo(kind_id, uid) else 'false',
        'userinfo_fields': json.dumps(form_fields) if form_fields else '{}',
        'option_fields': json.dumps(show_info.get('option_fields', '')),
        'field_regexes': form_regexes,
        'created': created
    })


def games(request, s):
    """
    获取所有比赛接口
    :param request: 请求对象
    :param s: 请求关键字
    :return: 返回该请求关键字对应的所有比赛类别
    """

    if s == 'hot':
        # 筛选条件: 完成时间大于当前时间;根据参与人数降序排序;根据创建时间降序排序;筛选10个
        kinds = CompetitionKindInfo.objects.filter(
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc),
        ).order_by('-total_partin_num').order_by('-created_at')[:10]

    elif s == 'tech':
        kinds = CompetitionKindInfo.objects.filter(
            kind_type=CompetitionKindInfo.IT_ISSUE,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    elif s == 'edu':
        kinds = CompetitionKindInfo.objects.filter(
            kind_type=CompetitionKindInfo.EDUCATION,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    elif s == 'culture':
        kinds = CompetitionKindInfo.objects.filter(
            kind_type=CompetitionKindInfo.CULTURE,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    elif s == 'sport':
        kinds = CompetitionKindInfo.objects.filter(
            kind_type=CompetitionKindInfo.SPORT,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    elif s == 'general':
        kinds = CompetitionKindInfo.objects.filter(
            kind_type=CompetitionKindInfo.GENERAL,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    elif s == 'interview':
        kinds = CompetitionKindInfo.objects.filter(
            kind_type=CompetitionKindInfo.INTERVIEW,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    else:
        kinds = None
    return render(request, 'competition/games.html', {
        'kinds': kinds,
    })


@check_login
@check_copstatus
def game(request):
    """
    返回比赛题目信息的视图
    :param request: 请求对象
    :return: 渲染视图: user_info: 用户信息;kind_id: 比赛唯一标识;kind_name: 比赛名称;cop_finishat: 比赛结束时间;rule_text: 大赛规则;
    """
    uid = request.GET.get('uid', '')  # 获取uid
    kind_id = request.GET.get('kind_id', '')  # 获取kind_id
    try:  # 获取比赛信息
        kind_info = CompetitionKindInfo.objects.get(kind_id=kind_id)
    except CompetitionKindInfo.DoesNotExist:  # 未获取到渲染错误视图
        return render(request, 'err.html', CompetitionNotFound)
    try:  # 获取题库信息
        bank_info = BankInfo.objects.get(bank_id=kind_info.bank_id)
    except BankInfo.DoesNotExist:  # 未获取到，渲染错误视图
        return render(request, 'err.html', BankInfoNotFound)
    try:  # 获取用户信息
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:  # 未获取到，渲染错误视图
        return render(request, 'err.html', ProfileNotFound)
    if kind_info.question_num > bank_info.total_question_num:  # 检查题库大小
        return render(request, 'err.html', QuestionNotSufficient)
    pageconfig = get_pageconfig(kind_info.app_id)  # 获取页面配置信息
    return render(request, 'competition/game.html', {  # 渲染视图信息
        'user_info': profile.data,
        'kind_id': kind_info.kind_id,
        'kind_name': kind_info.kind_name,
        'cop_finishat': kind_info.cop_finishat,
        'period_time': kind_info.period_time,
        'rule_text': pageconfig.get('text_info', {}).get('rule_text', '')
    })

# def history_game(request):
#     """
#     返回比赛题目信息的视图
#     :param request: 请求对象
#     :return: 渲染视图: user_info: 用户信息;kind_id: 比赛唯一标识;kind_name: 比赛名称;cop_finishat: 比赛结束时间;rule_text: 大赛规则;
#     """
#     uid = request.GET.get('uid', '')  # 获取uid
#     kind_id = request.GET.get('kind_id', '')  # 获取kind_id
#     try:  # 获取比赛信息
#         kind_info = CompetitionKindInfo.objects.get(kind_id=kind_id)
#     except CompetitionKindInfo.DoesNotExist:  # 未获取到渲染错误视图
#         return render(request, 'err.html', CompetitionNotFound)
#     try:  # 获取题库信息
#         bank_info = BankInfo.objects.get(bank_id=kind_info.bank_id)
#     except BankInfo.DoesNotExist:  # 未获取到，渲染错误视图
#         return render(request, 'err.html', BankInfoNotFound)
#     try:  # 获取用户信息
#         profile = Profile.objects.get(uid=uid)
#     except Profile.DoesNotExist: # 未获取到，渲染错误视图
#         return render(request, 'err.html', ProfileNotFound)
#     if kind_info.question_num > bank_info.total_question_num: # 检查题库大小
#         return render(request, 'err.html', QuestionNotSufficient)
#     pageconfig = get_pageconfig(kind_info.app_id)  # 获取页面配置信息
#     return render(request, 'competition/history_game.html', {  # 渲染视图信息
#         'user_info': profile.data,
#         'kind_id': kind_info.kind_id,
#         'kind_name': kind_info.kind_name,
#         'period_time': kind_info.period_time,
#     })


@check_login
@check_copstatus
def history_game(request):
    """
    返回比赛题目信息的视图
    :param request: 请求对象
    :return: 渲染视图: user_info: 用户信息;kind_id: 比赛唯一标识;kind_name: 比赛名称;cop_finishat: 比赛结束时间;rule_text: 大赛规则;
    """
    uid = request.GET.get('uid', '')  # 获取uid
    kind_id = request.GET.get('kind_id', '')  # 获取kind_id
    try:  # 获取比赛信息
        kind_info = CompetitionKindInfo.objects.get(kind_id=kind_id)
    except CompetitionKindInfo.DoesNotExist:  # 未获取到渲染错误视图
        return render(request, 'err.html', CompetitionNotFound)
    try:  # 获取题库信息
        bank_info = BankInfo.objects.get(bank_id=kind_info.bank_id)
    except BankInfo.DoesNotExist:  # 未获取到，渲染错误视图
        return render(request, 'err.html', BankInfoNotFound)
    try:  # 获取用户信息
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:  # 未获取到，渲染错误视图
        return render(request, 'err.html', ProfileNotFound)
    if kind_info.question_num > bank_info.total_question_num:  # 检查题库大小
        return render(request, 'err.html', QuestionNotSufficient)

    return render(request, 'competition/history_game.html', {  # 渲染视图信息
        'user_info': profile.data,
        'kind_id': kind_info.kind_id,
        'kind_name': kind_info.kind_name,
        'period_time': kind_info.period_time,
    })


def str2list(str, sign=','):
    if str[0] == '[':
        str = str[1:-1]
    str = str.replace('\'', '')
    lt = str.split(sign)
    return lt


def str2dict(question_list):
    question_list = str2list(question_list.replace('\"', ''))
    print('question_list', question_list)
    print('--' * 81)
    qs_list = []

    for question in question_list:
        data = {}
        if '？' in question:
            data['qtype'] = 'choice'
            data['question'] = question[1:].split('？')[0] + '?'
            items = str2list(question[1:].split('？')[1])[0]
            data['items'] = str2list(items, ';')
        else:
            data['qtype'] = 'fillinblank'
            data['question'] = question
        qs_list.append(data)
    return qs_list


@check_login
@check_copstatus
def get_history(request):
    """
    获取题目信息接口
    :param request: 请求对象
    :return: 返回json数据: user_info: 用户信息;kind_info: 比赛信息;qa_id: 比赛答题记录;questions: 比赛随机后的题目;
    """
    kind_id = request.GET.get('kind_id', '')  # 获取kind_id
    uid = request.GET.get('uid', '')  # 获取uid
    try:
        qa_info_uid = CompetitionQAInfo.objects.filter(uid=uid)
    except CompetitionQAInfo.DoesNotExist:
        return json_response(*CompetitionError.CompetitionNotFound)

    try:
        qa_info_kind = CompetitionQAInfo.objects.filter(kind_id=kind_id)
    except CompetitionKindInfo.DoesNotExist:
        return json_response(*CompetitionError.CompetitionNotFound)

    qa_ls = (qa_info_uid & qa_info_kind)

    for qa in qa_ls: qa_info = qa

    answer = str2list(qa_info.asrecord)
    question_list = str2dict(qa_info.qsrecord)
    state_list = str2list(qa_info.wrong_list)
    # state_list=[int(i) for i in state_list]
    replay_list = str2list(qa_info.aslogrecord)
    replay_list = [i.strip() for i in replay_list]

    # print('answer',qa_info.asrecord)

    return json_response(200, 'OK', {  # 返回JSON数据，包括题目信息，答题log信息等
        # 'kind_info': kind_id,
        'question_num': qa_info.total_num,
        # 'qa_id': qa_info.qa_id,
        'questions': question_list,
        'answer': answer,
        'replay_list': replay_list,
        'state': state_list
    })


# @check_login
# def history(requrest):
#     uid = requrest.GET.get('uid', '')
#     kind_id = requrest.GET.get('kind_id', '')
#
#     try:
#         qa_info_uid = CompetitionQAInfo.objects.filter(uid=uid)
#
#     except CompetitionQAInfo.DoesNotExist:
#         return json_response(*CompetitionError.CompetitionNotFound)
#     try:
#         qa_info_kind = CompetitionQAInfo.objects.filter(kind_id=kind_id)
#     except CompetitionKindInfo.DoesNotExist:
#         return json_response(*CompetitionError.CompetitionNotFound)
#
#     qa_info = (qa_info_uid & qa_info_kind)[0]
#     rlist = qa_info.aslogrecord
#     question = qa_info.qsrecord
#     answer = qa_info.asrecord
#     wrong_list = qa_info.wrong_list
#     correct_list = qa_info.correct_list
#     choice_list = ['A', 'B', 'C', 'D']
#     print('question', question)
#     print('answer', answer)
#
#     # correct_aply=[]
#     # # correct_question=[]
#     # # correct_anw
#     #
#     # wrong_aply=[]
#     #
#     #
#     # for i in rlist:
#     #     if isinstance(i, str):
#     #         i = i.split(',')
#     #         t = i[0][0]  # qtype
#     #         p = i[0][2:]  # pk
#     #         v = i[1]  # answer
#     #         # 转换类型
#     #         try:
#     #             pk = int(p)
#     #         except ValueError:
#     #             continue
#     #         if t == 'c':
#     #             try:
#     #                 c = ChoiceInfo.objects.get(pk=pk)
#     #             except ChoiceInfo.DoesNotExist:
#     #                 continue
#     #             if v in choice_list:
#     #                 item = 'c.item' + str(choice_list.index(v) + 1)
#     #                 aply=str(eval(item))
#     #                 if aply == str(c.answer) : correct_aply.append(aply)
#     #                 else : wrong_list.append(aply)
#     #             else : wrong_list.append(aply)
#     #
#     #         elif t == 'f':
#     #             try:
#     #                 f = FillInBlankInfo.objects.get(pk=pk)
#     #             except FillInBlankInfo.DoesNotExist:
#     #                 continue
#     #             aply=v.strip()
#     #             if aply == f.answer:correct_aply.append(aply)
#     #             else:wrong_aply.append(aply)
#     # print('correct_aply',correct_aply)
#     # print('wrong_aply',wrong_aply)
#     return json_response(200, 'OK', {  # 返回JSON数据，包括题目信息，答题log信息等
#         'kind_id': qa_info.kind_id,
#         'uid': qa_info.uid,
#         'qa_id': qa_info.qa_id,
#         'wrong_list': qa_info.wrong_list,
#         'correct_list': qa_info.correct_list
#     })


@check_login
def history(requrest):
    # 用于得到uid和kind_id，用于打开页面
    uid = requrest.GET.get('uid', '')
    kind_id = requrest.GET.get('kind_id', '')

    try:
        qa_info_uid = CompetitionQAInfo.objects.filter(uid=uid)

    except CompetitionQAInfo.DoesNotExist:
        return json_response(*CompetitionError.CompetitionNotFound)
    try:
        qa_info_kind = CompetitionQAInfo.objects.filter(kind_id=kind_id)
    except CompetitionKindInfo.DoesNotExist:
        return json_response(*CompetitionError.CompetitionNotFound)

    qa_info = (qa_info_uid & qa_info_kind)[0]
    question = qa_info.qsrecord
    answer = qa_info.asrecord
    for i in question:  # 剔除答案信息
        i.pop('answer')
    print('history'*8)
    return json_response(200, 'OK', {  # 返回JSON数据，包括题目信息，答题log信息等
        'kind_info': qa_info.kind_id,
        'user_info': qa_info.uid,
        'qa_id': qa_info.qa_id,
        'questions': question,
        'answer': answer
    })


@check_login
def result(request):
    """
    比赛结果和排行榜的视图
    :param request: 请求对象
    :return: 渲染视图: qa_info: 答题记录数据;user_info: 用户信息数据;kind_info: 比赛信息数据;rank: 该用户当前比赛排名
    """

    uid = request.GET.get('uid', '')
    kind_id = request.GET.get('kind_id', '')
    qa_id = request.GET.get('qa_id', '')

    try:
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        return render(request, 'err.html', ProfileNotFound)

    try:
        kind_info = CompetitionKindInfo.objects.get(kind_id=kind_id)
    except CompetitionKindInfo.DoesNotExist:
        return render(request, 'err.html', CompetitionNotFound)

    try:
        qa_info = CompetitionQAInfo.objects.get(qa_id=qa_id, uid=uid)
    except CompetitionQAInfo.DoesNotExist:
        return render(request, 'err.html', QuestionLogNotFound)

    return render(request, 'competition/result.html', {
        'qa_info': qa_info.detail,
        'user_info': profile.data,
        'kind_info': kind_info.data,
        'rank': get_rank(kind_id, uid)
    })


@check_login
def rank(request):
    """
    排行榜数据视图
    :param request: 请求对象
    :return: 渲染视图: user_info: 用户信息;kind_info: 比赛信息; rank: 所有比赛排名;
    """

    uid = request.GET.get('uid', '')
    kind_id = request.GET.get('kind_id', '')

    try:
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        return render(request, 'err.html', ProfileNotFound)

    try:
        kind_info = CompetitionKindInfo.objects.get(kind_id=kind_id)
    except CompetitionKindInfo.DoesNotExist:
        return render(request, 'err.html', CompetitionNotFound)

    ranks, rank_data = get_rank_data(kind_id)
    for i in range(len(rank_data)):
        rank_data[i].update({'rank': i + 1})
        rank_data[i]['time'] = rank_data[i]['time'] / 1000.000

    return render(request, 'competition/rank.html', {
        'user_info': profile.data,
        'kind_info': kind_info.data,
        'rank': rank_data,
        'total_score': kind_info.total_score
    })


@check_login
def search(request):
    """
    搜索查询视图
    :param request: 请求对象
    :return: 渲染视图: user_info: 用户信息;result:查询结果比赛信息集合;key: 查询结果的关键字,是根据比赛名称查询还是根据赞助商关键字查询的结果
    """

    uid = request.GET.get('uid', '')
    keyword = request.GET.get('keyword', '')

    try:
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        render(request, 'err.html', ProfileNotFound)

    keyword = keyword.strip(' ')

    kinds = CompetitionKindInfo.objects.filter(kind_name__contains=keyword)
    key = 'kind'

    if not kinds:
        kinds = CompetitionKindInfo.objects.filter(sponsor_name__contains=keyword)
        key = 'sponsor'

    return render(request, 'competition/search.html', {
        'result': kinds,
        'key': key or ''
    })


@check_login
def contact(request):
    """
    联系我们视图
    :param request: 请求对象
    :return: 渲染视图: user_info: 用户信息
    """

    uid = request.GET.get('uid', '')
    try:
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'web/contact_us.html', {'user_info': profile.data if profile else None})


def donate(request):
    """
        捐助视图
        :param request: 请求对象
        :return: 渲染视图: user_info: 用户信息
    """

    uid = request.GET.get('uid', '')
    try:
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'web/donate.html', {'user_info': profile.data if profile else None})

def about_us(request):
    """
        捐助视图
        :param request: 请求对象
        :return: 渲染视图: user_info: 用户信息
    """

    uid = request.GET.get('uid', '')
    try:
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'web/about_us.html', {'user_info': profile.data if profile else None})
