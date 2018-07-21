# coding=utf-8


from django.shortcuts import render
from models import *
from django.core.paginator import Paginator,Page


# 查询每类商品最新的4个和点击率最高的4个
def index(request):
    """
    index函数负责查询页面中需要展示的商品内容，
    主要是每类最新的4种商品和4种点击率最高的商品，
    每类商品需要查询2次
    """
    typelist = TypeInfo.objects.all()
    # 1代表新品，2代表热门
    fruit1 = typelist[0].goodsinfo_set.order_by('-id')[:4]
    fruit2 = typelist[0].goodsinfo_set.order_by('-gclick')[:4]
    seafood1 = typelist[1].goodsinfo_set.order_by('-id')[:4]
    seafood2 = typelist[1].goodsinfo_set.order_by('-gclick')[:4]
    meat1 = typelist[2].goodsinfo_set.order_by('-id')[:4]
    meat2 = typelist[2].goodsinfo_set.order_by('-gclick')[:4]
    egg1 = typelist[3].goodsinfo_set.order_by('-id')[:4]
    egg2 = typelist[3].goodsinfo_set.order_by('-gclick')[:4]
    vege1 = typelist[4].goodsinfo_set.order_by('-id')[:4]
    vege2 = typelist[4].goodsinfo_set.order_by('-gclick')[:4]
    froz1 = typelist[5].goodsinfo_set.order_by('-id')[:4]
    froz2 = typelist[5].goodsinfo_set.order_by('-gclick')[:4]
    context = {'guest_cart': 1,
               'title': '首页',
               'fruit1': fruit1, 'fruit2':fruit2,
               'seafood1': seafood1, 'seafood2': seafood2,
               'meat1': meat1, 'meat2': meat2,
               'egg1': egg1, 'egg2': egg2,
               'vege1': vege1, 'vege2': vege2,
               'froz1': froz1, 'froz2': froz2,
               }
    return render(request, 'df_goods/index.html', context)


def list(request, typeid, pindex, sort):
    '''
    typeid: 商品所属的类的id
    pageid: 页面的id
    sort: 排序的方式，1根据id查询，2根据价格查询，3根据点击量查询
    '''
    # 获取最新的商品
    type = TypeInfo.objects.get(pk=int(typeid))
    newgoods = type.goodsinfo_set.order_by('-id')[0:2]
    # 根据sort查询方式查询所有商品
    if sort == '1':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(typeid)).order_by('-id')
    elif sort == '2':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(typeid)).order_by('-gprice')
    elif sort == '3':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(typeid)).order_by('-gclick')
    paginator = Paginator(goods_list,10)
    page = paginator.page(int(pindex))
    context = {
        'title': type.ttitle,
        'list': 1,
        'guest_cart': 1,
        'paginator': paginator,
        'page': page,
        'type': type,
        'sort': sort,
        'news': newgoods
    }
    return render(request, 'df_goods/list.html', context)


def detail(request, gid):
    goods = GoodsInfo.objects.get(pk=int(gid))
    type = goods.gtype
    goods.gclick = goods.gclick+1
    goods.save()
    newgoods = goods.gtype.goodsinfo_set.order_by('-id')[:2]
    context = {
        'title': goods.gtitle,
        'list': 1,
        'isDetail': 1,
        'guest_cart': 1,
        'type':type,
        'goods': goods,
        'news': newgoods,
    }
    response =  render(request, 'df_goods/detail.html', context)

    # 记录最近浏览，在用户中心使用
    # 获取cookies
    goods_ids = request.COOKIES.get('goods_ids', '')
    # 获取当前点击商品id
    goods_id = gid
    # 判断cookies中商品id是否为空
    if goods_ids != '':
        # 分割出每个商品id
        goods_id_list = goods_ids.split(',')
        # 判断商品是否已经存在于列表
        if goods_id_list.count(goods_id)>=1:
            # 存在则移除并在第一位添加
            goods_id_list.remove(goods_id)
            goods_id_list.insert(0, goods_id)
        # 判断列表数是否超过5个
        if len(goods_id_list) > 5:
            # 超过5个删除第6个
            del goods_id_list[5]
        goods_ids = ','.join(goods_id_list)
    else:
        # 第一次添加
        goods_ids = goods_id

    response.set_cookie('goods_ids', goods_ids)
    return response