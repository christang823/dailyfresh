# coding=utf-8


from django.shortcuts import render,redirect
from models import *
from hashlib import sha1


def register(request):
    context = {'title': '用户注册'}
    return render(request, 'df_user/register.html', context)


def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # 注册成功，转到登陆页面
    return redirect('/user/login/')


def login(request):
    context = {'title': '用户登陆'}
    return render(request, 'df_user/login.html', context)