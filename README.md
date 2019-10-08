# django_mysql_pool
Django mysql pool

------
###### 这个是django中使用原生sql去操作数据库时，所建立的连接池helper

```python
有四种类型可供选择
SS: SSCursor,            # 无缓存，返回元组类型，适合操作级别上万的sql
None: Cursor,            # 有缓存，返回元组类型，默认类型
Dict: DictCursor,        # 有缓存，返回带有字段的字典类型
SSDict: SSDictCursor     # 无缓存，返回带有字段的字典类型，适合操作级别上万的sql
```
------

# 怎么使用
```
1. 初始化 form dbHelper import Database
  dbpool = Database(cursorType=None) # 或以上几种缓存类型与返回值类型
2. sql增删改查
  dbpool.ExecQueryFirst("select * from user where id = 1")  # 只查询一条数据的情况
  dbpool.ExecQueryAll("select * from user")                 # 查询N条数据的情况
  dbpool.ExecNoQuery("")                                    # insert、 update、 delete都使用这个方法
  dbpool.ExecQueryYield("")                                 # 查询N条数据，但是需要把结果格式化为generator时使用的方法
```
