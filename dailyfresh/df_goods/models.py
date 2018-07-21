# coding=utf-8


from __future__ import unicode_literals
from django.db import models
from tinymce.models import HTMLField


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')


class GoodsInfo(models.Model):
    # 商品名称
    gtitle = models.CharField(max_length=20)
    # 图片
    gpic = models.ImageField(upload_to='df_goods')
    # 价格
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    # 单位
    gunit = models.CharField(max_length=20)
    # 点击量
    gclick = models.IntegerField()
    # 简介
    gjianjie = models.CharField(max_length=200)
    # 库存
    gkucun = models.IntegerField()
    # 详细介绍
    gcontent = HTMLField()
    # 所属商品类
    gtype = models.ForeignKey(TypeInfo)

    def __str__(self):
        return self.gtitle.encode('utf-8')