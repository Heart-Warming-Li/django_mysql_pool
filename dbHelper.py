#!/usr/bin/env python
# coding=utf-8
# ------------------------------------- #
# @author   Heart-Warming-Li            #
# @email    954172807@qq.com            #
# @qq       954172807                   #
# @wechat                               #
# @copyleft Heart-Warming-Li            #
# ------------------------------------- #
import os
import pymysql
from DBUtils.PooledDB import PooledDB
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testDjango.settings')
config = settings.DATABASES['default']

class Database:
    def __init__(self,cursorType=None):
        """
        :param cursorType: 游标类型
        SS: SSCursor,            # 无缓存，返回元组类型，适合操作级别上万的sql
        None: Cursor,            # 有缓存，返回元组类型，默认类型
        Dict: DictCursor,        # 有缓存，返回带有字段的字典类型
        SSDict: SSDictCursor     # 无缓存，返回带有字段的字典类型，适合操作级别上万的sql
        """
        # mysql数据库
        self.host = config.get('HOST','127.0.0.1')
        self.port = config.get('PORT',3306)
        self.user = config.get('USER','root')
        self.pwd  = config.get('PASSWORD','')
        self.db   = config.get('NAME','test')
        self.charset = config.get('charset','utf8')
        self.port = int(self.port)
        self.cursorType = cursorType
        self._Cursor = self._cursorType()
        self._CreatePool()

    def _cursorType(self):
        if self.cursorType == 'SS':
            return pymysql.cursors.SSCursor
        elif self.cursorType == 'SSDict':
            return pymysql.cursors.SSDictCursor
        elif self.cursorType == 'Dict':
            return pymysql.cursors.DictCursor
        else:
            return pymysql.cursors.Cursor

    def _CreatePool(self):
        # mincached 初始化时,连接池至少创建的空闲连接,0表示不创建
        # maxcached 连接池中空闲的最多连接数,0和None表示没有限制
        # maxshared 连接池中最多共享的连接数量,0和None表示全部共享(其实没什么卵用)
        self.Pool = PooledDB(creator=pymysql, mincached=20, maxcached=5, maxshared=5,host=self.host, port=self.port,
                             user=self.user, password=self.pwd, database=self.db, charset=self.charset)

    def _Getconnect(self):
        self.conn = self.Pool.connection()
        cur = self.conn.cursor(self._Cursor)
        if not cur:
            raise NameError + "数据库连接不上"
        else:
            return cur

    # 显示查询中的第一条记录
    def ExecQueryFirst(self, *args, **kwargs):
        cur = self._Getconnect()
        cur.execute(args[0], kwargs)
        resultFirst = cur.fetchone()
        cur.close()
        self.conn.close()
        return resultFirst

    # 显示查询中的所有记录
    def ExecQueryAll(self, *args, **kwargs):
        cur = self._Getconnect()
        cur.execute(args[0], kwargs)
        resultList = cur.fetchall()
        cur.close()
        self.conn.close()
        return resultList

    # 非查询的sql,增删改
    def ExecNoQuery(self, *args, **kwargs):
        cur = self._Getconnect()        
        try:
            cur.execute(args[0],kwargs)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            return '[Error]: {}'.format(e)
        finally:
            cur.close()
            self.conn.close()

    # 显示查询中的所有记录，并一条一条返回生成器中，返回结果也是生成器
    def ExecQueryYield(self, *args, **kwargs):
        cur = self._Getconnect()
        cur.execute(args[0], kwargs)
        resultOne = cur.fetchone()
        while resultOne is not None:
            yield resultOne
            resultOne = cur.fetchone()
        cur.close()
        self.conn.close()
