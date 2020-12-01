from django.db import models
from typing import Iterable
import django.utils.timezone as timezone


# Create your models here.

class ListField(models.TextField):
    """
    A custom Django field to represent lists as comma separated strings
    """

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['token'] = self.token
        return name, path, args, kwargs

    def to_python(self, value):

        class SubList(list):
            def __init__(self, token, *args):
                self.token = token
                super().__init__(*args)

            def __str__(self):
                return self.token.join(self)

        if isinstance(value, list):
            return value
        if value is None:
            return SubList(self.token)
        return SubList(self.token, value.split(self.token))

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if not value:
            return
        assert (isinstance(value, Iterable))
        return self.token.join(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)


class UserModel(models.Model):
    userName = models.CharField(max_length=32, default='userName')  # 登录用户名
    password = models.CharField(max_length=32, default='000000')  # 登陆密码

    profession = models.CharField(max_length=32, default='undefined')  # 职业
    email = models.CharField(max_length=32, default='undefined')  # 电子邮件
    phoneNumber = models.CharField(max_length=32, default='undefined')  # 电话号码
    area = models.CharField(max_length=32, default='undefined')  # 地区
    personHomepage = models.CharField(max_length=200, default='undefined')  # 个人主页
    note = models.TextField(default='undefined')  # 备注
    headImg = models.ImageField(upload_to="img/", default="img/default.jpg")  # 头像

    isOnline = models.IntegerField(default=0)

    groupList = ListField(default=['-1'])
    taskList = ListField(default=['-1'])

    def __str__(self):
        return self.userName


class GroupModel(models.Model):
    groupName = models.CharField(max_length=32, default='groupName')
    userList = ListField(default=['-1'])
    taskList = ListField(default=['-1'])


class TaskModel(models.Model):
    taskName = models.CharField(max_length=32, default='taskName')
    userList = ListField(default=['-1'])
    ddlTime = models.DateTimeField(default=timezone.now)
