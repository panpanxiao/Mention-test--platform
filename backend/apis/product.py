# -*- coding:utf-8 -*-
import pymysql.cursors
from flask import Blueprint
from flask import request
from flask import json

app_product = Blueprint("app_product", __name__)


def connectDB():
    db_con = pymysql.connect(host="localhost",
                             user="root",
                             password="xpp950405..",
                             database="productInfo",
                             charset="utf8",
                             cursorclass=pymysql.cursors.DictCursor
                             )
    return db_con


# [POST方法]实现新建数据的数据库插入
@app_product.route("/api/product/create", methods=["POST"])
def product_create():
    # 初始化数据库链接
    connection = connectDB()

    # 定义默认返回结构体
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": []
    }

    # 获取请求传递json body
    body = request.get_data()
    body = json.loads(body)

    with connection:
        # 先做个查询，判断keyCode是否重复（这里的关键词最初定义为唯一项目编号或者为服务的应用名）
        with connection.cursor() as cursor:
            select = "SELECT * FROM `products` WHERE `keyCode`=%s"
            cursor.execute(select, (body["keyCode"],))
            result = cursor.fetchall()

        # 有数据说明存在相同值，封装提示直接返回
        if len(result) > 0:
            resp_data["code"] = 20001
            resp_data["message"] = "唯一编码keyCode已存在"
            return resp_data

        with connection.cursor() as cursor:
            # 拼接插入语句,并用参数化%s构造防止基本的SQL注入
            # 其中id为自增，插入数据默认数据设置的当前时间
            sql = "INSERT INTO `products` (`keyCode`,`title`,`desc`,`operator`) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, (body["keyCode"], body["title"], body["desc"], body["operator"]))
            # 提交执行保存插入数据
            connection.commit()

        # 按返回模版格式进行json结果返回
        return resp_data


@app_product.route("/api/product/update", methods=['POST'])
def product_update():
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": []
    }

    body = request.get_data()
    body = json.loads(body)

    connection = connectDB()

    with connection:
        with connection.cursor() as cursor:
            select = "SELECT * FROM `products` WHERE `keyCode`=%s"
            cursor.execute(select, (body['keyCode'],))
            result = cursor.fetchall()

        # if len(result) > 0 and result[0]["id"] == body["id"]:
        #     resp_data["code"] = 20001
        #     resp_data["message"] = "唯一编码keyCode已存在"
        #     return resp_data

        with connection.cursor() as cursor:
            sql = "UPDATE `products` SET `keyCode`=%s, `title`=%s,`desc`=%s,`operator`=%s, `update`= NOW() WHERE id=%s"
            cursor.execute(sql, (body["keyCode"], body["title"], body["desc"], body["operator"], body['id']))
            connection.commit()

        return resp_data


@app_product.route("/api/product/delete", methods=["DELETE"])
def product_delete():
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": []
    }

    ID = request.args.get('id')
    if ID is None:
        resp_data["code"] = 20002
        resp_data["message"] = "请求id参数为空"
        return resp_data

    connection = connectDB()
    with connection.cursor() as cursor:
        sql = "DELETE from `products` where id=%s"
        cursor.execute(sql, ID)
        connection.commit()

    return resp_data


@app_product.route("/api/product/search", methods=['GET'])
def product_search():
    title = request.args.get('title')
    keyCode = request.args.get('keyCode')

    sql = "SELECT * FROM `products`"

    # 如果title不为空，拼接tilite的模糊查询
    # if title is not None:
    #     sql = sql + " AND `title` LIKE '%{}%'".format(title)
    # 如果keyCode不为空，拼接tilite的模糊查询
    if keyCode is not None:
        sql = sql + " WHERE `keyCode` LIKE '%{}%'".format(keyCode)

    # 排序最后拼接
    sql = sql + " ORDER BY `update` DESC"

    connection = connectDB()
    # 使用python的with..as控制流语句（相当于简化的try except finally）
    with connection.cursor() as cursor:
        # 按照条件进行查询
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()

    # 按返回模版格式进行json结果返回
    resp_data = {
        "code": 20000,
        "data": data
    }

    return resp_data


@app_product.route("/api/product/list", methods=['GET'])
def product_list():
    db_con = connectDB()
    with db_con.cursor() as cursor:
        # 查询产品信息表-按更新时间新旧排序
        sql = "SELECT * FROM `products`"
        cursor.execute(sql)
        data = cursor.fetchall()
    # 按返回模版格式进行json结果返回
    resp_data = {
        "code": 20000,
        "data": data
    }
    return resp_data
