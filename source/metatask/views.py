from django.shortcuts import render
from django.http import HttpResponse
import json
from metatask import models
from django.core.mail import send_mail
from django.forms.models import model_to_dict
from approot.settings import BASE_DIR
import os
import ast


# Create your views here.
# 注册（使用了Django内助的邮箱验证功能）
def register(request):
    userName = request.POST.get('userName', 'username')
    password = request.POST.get('password', 'xxx')
    email = request.POST.get('email', 'undefined')
    res = {'retCode': 0, 'message': ''}

    obj = models.UserModel.objects.filter(userName=userName)
    objmail = models.UserModel.objects.filter(email=email)

    if obj.count() == 0 and objmail.count() == 0:
        '''
        try:

            msg = MIMEText('您正在进行ArXiver注册，如果不是您亲自操作，请及时联系管理员邮箱', 'plain', 'utf-8')
            msg['From'] = formataddr(["ArXiver管理员", my_sender])  # 发件人邮件昵称和账号
            msg['To'] = formataddr(["注册用户", email])  # 收件人邮箱昵称和账号
            msg['Subject'] = "ArXiver注册"  # 邮件标题
            server = smtplib.SMTP_SSL("smtp.163.com", 465)  # SMTP服务器和端口
            server.login(my_sender, my_pass)  # 发件人邮箱账号和密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except:
            mailret = False
        '''
        mailret = send_mail('ArXiver注册', '您正在进行ArXiver注册，如果不是您亲自操作，请及时联系本邮箱',
                            'rg_firstgroup@163.com', [email], fail_silently=False)

        if mailret == 1:
            models.UserModel.objects.create(userName=userName, password=password,email=email,
                                            collectDict='{}', focusList=['-1'])
            obj = models.UserModel.objects.get(userName=userName)
            # obj.collectList.remove('-1')
            obj.save()
            res['retCode'] = 1
            res['message'] = '注册成功'

        else:
            res['retCode'] = 2
            res['message'] = '请输入正确的邮箱地址'

    else:
        res['retCode'] = 0
        res['message'] = '用户名或邮箱已注册'

    return HttpResponse(json.dumps({'register': res}))


# 登录
def login(request):
    userName = request.POST.get('userName', 'username')
    password = request.POST.get('password', 'xxx')

    res = {'retCode': 0, 'message': ''}
    obj = models.UserModel.objects.filter(userName=userName)

    if obj.count() == 0:
        res['retCode'] = 0
        res['message'] = '用户不存在'
    else:
        obj = models.UserModel.objects.get(userName=userName)
        if obj.password == password:
            res['retCode'] = 1
            res['message'] = '成功登录'
        else:
            res['retCode'] = 2
            res['message'] = '密码错误'
    return HttpResponse(json.dumps({'login': res}))


# 获取个人信息
def getUserInformation(request):
    userName = request.POST.get('userName', 'username')

    obj = models.UserModel.objects.get(userName=userName)

    res = model_to_dict(obj, fields=['userName', 'profession', 'email', 'phoneNumber',
                                     'area', 'personHomepage', 'note', 'isOnline'])

    res['groupList'] = []
    for group in obj.groupList:
        if group != '-1':
            res['groupList'].append(group)

    res['taskList'] = []
    for task in obj.taskList:
        if task != '-1':
            res['taskList'].append(task)

    return HttpResponse(json.dumps({'userInfo': res}))


# 上传头像
def uploadHeadImg(request):
    # noinspection PyBroadException
    try:
        userName = request.POST.get('userName', '')
        headImg = request.FILES.get('headImg')
        print(headImg)

        obj = models.UserModel.objects.get(userName=userName)
        originImgPath = str(obj.headImg.url)

        obj.headImg = headImg
        obj.save()

        # 删除旧图片
        _, f_name = os.path.split(originImgPath)
        if f_name != "default.jpg":
            originImgFullPath = (BASE_DIR+originImgPath).replace("\\", "/")
            print(originImgFullPath)
            if os.path.exists(originImgFullPath):
                if os.path.isfile(originImgFullPath):
                    os.remove(originImgFullPath)
                    # return HttpResponse(json.demps({'retCode':'222'}))

        return HttpResponse(json.dumps({'retCode': 1, 'message': '成功上传'}))
    except Exception as e:
        return HttpResponse(json.dumps({'retCode': 0, 'message': '上传失败'}))


# 获取头像
def getHeadImg(request):
    userName = request.GET.get('userName', '')
    obj = models.UserModel.objects.get(userName=userName)
    return HttpResponse(json.dumps({'avatar_url': obj.headImg.url}))


# 获取任务信息
def getTaskInformation(request):
    taskName = request.POST.get('taskName', 'taskname')

    obj = models.TaskModel.objects.get(taskName=taskName)

    res = model_to_dict(obj, fields=['taskName'])
    res['userList'] = []
    for user in obj.userList:
        if user != '-1':
            res['userList'].append(user)

    res['ddlTime'] = str(obj.ddlTime)
    return HttpResponse(json.dumps({'taskInfo': res}))


# 获取小组信息
def getGroupInformation(request):
    groupName = request.POST.get('groupName', 'groupname')

    obj = models.GroupModel.objects.get(groupName=groupName)

    res = model_to_dict(obj, fields=['groupName'])
    res['userList'] = []
    for user in obj.userList:
        if user != '-1':
            res['userList'].append(user)

    res['taskList'] = []
    for task in obj.taskList:
        if task != '-1':
            res['taskList'].append(task)

    return HttpResponse(json.dumps({'groupInfo': res}))


# 修改个人信息
def modifyUserInformation(request):
    #print("here")
    userName = request.POST.get('userName', "undefined")
    password = request.POST.get('password', "undefined")
    profession = request.POST.get('profession', "undefined")
    email = request.POST.get('email', "undefined")
    phoneNumber = request.POST.get('phoneNumber', "undefined")
    area = request.POST.get('area', "undefined")
    personHomepage = request.POST.get('personHomepage', "undefined")
    note = request.POST.get('note', "undefined")

    obj = models.UserModel.objects.get(userName=userName)
    if password != "undefined":
        obj.password = password
        obj.save()
    if profession != "undefined":
        obj.profession = profession
        obj.save()
    if email != "undefined":
        obj.email = email
        obj.save()
    if phoneNumber != "undefined":
        obj.phoneNumber = phoneNumber
        obj.save()
    if area != "undefined":
        obj.area = area
        obj.save()
    if personHomepage != "undefined":
        obj.personHomepage = personHomepage
        obj.save()
    if note != "undefined":
        obj.note = note
        obj.save()

    obj = models.UserModel.objects.get(userName=userName)

    res = model_to_dict(obj, fields=['userName', 'profession', 'email', 'phoneNumber',
                                     'area', 'personHomepage', 'note', 'isOnline'])

    res['groupList'] = []
    for group in obj.groupList:
        if group != '-1':
            res['groupList'].append(group)

    res['taskList'] = []
    for task in obj.taskList:
        if task != '-1':
            res['taskList'].append(task)

    return HttpResponse(json.dumps({'userInfo': res}))


