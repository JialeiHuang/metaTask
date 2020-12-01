from django.shortcuts import render
from django.http import HttpResponse
import json
from metatask import models
from django.core.mail import send_mail


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
