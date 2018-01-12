#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__="2018.01.12"
# __purpose__="聚合数据，分析结果，使用snownlp作情感分析"

from MongoData import getData
import asyncio
import numpy as np


class Meta(type):
    def __new__(cls, name, bases, attrs):
        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except Exception as e:
            print(e)
        attrs['loop'] = asyncio.get_event_loop()
        return type.__new__(cls, name, bases, attrs)


class MakeResult(metaclass=Meta):
    """取出数据 -》 数据分词 -》
    1.统计言论中词频
    2.统计提到动物的词的数量
    """

    def __init__(self, **kw):
        pass

    colls = {
        'tianya':['yangchongxinqing','feichangchongwu','chongmixuetang','chongwuxinxi','liuyankanban'],
        'cpn':['nuoyafangzhou','gouhualianpian','maomaoxiyu','lengxuejiazu','bainiaoyuan'],
        'lele':['xinshouijaoxue','chongwuyisheng','chongwumeiong','gougouxunlian'],
        'baidu':['chongwuba']
    }
    @classmethod
    def collection(cls):
        # 从mongo取数据
        tasks = [asyncio.ensure_future(getData(i,j)) for i in cls.colls for j in cls.colls[i]]
        # 执行异步组数据
        r = cls.loop.run_until_complete(asyncio.gather(*tasks))
        # 存储到np.array里面
        ar = np.array([j for i in r for j in i])
        return ar
    @classmethod
    def top10(cls):
        """
        前十关键词和数量
        :return: [name] [count]
        """
        r = ((1,2),(2,3),(3,4,1))
        n = np.array([j for i in r for j in i])
        print(type(n))
    @classmethod
    def sem(cls):
        """
        统计情感分析
        :return: [name] [count]

        """
MakeResult.top10()
