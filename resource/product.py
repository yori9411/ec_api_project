import pymysql
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
import util
from . import products_router_model
from datetime import timedelta

def db_init():
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=8889,
        db='shop'
    )

    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor


####### API Action #########

#Products
class Products(MethodResource):
    # GET_Product_ALL
    @doc(description='Get Products info.', tags=['商品庫存']) #框架
    @use_kwargs(products_router_model.ProductGetSchema, location="query") #功能
    @marshal_with(products_router_model.ProductGetResponse, code=200) #範例
    def get(self, **kwargs):
        db, cursor = db_init()
        name = kwargs.get("name")
        if name is not None:
            sql = f"SELECT * FROM shop.goods WHERE name = '{name}';"
        else:
            sql = 'SELECT * FROM shop.goods;'
        cursor.execute(sql)
        products = cursor.fetchall()
        db.close() #一定要加close,不然db會爆掉
        return util.success(products)

    # POST Products
    @doc(description='Create Products.', tags=['商品庫存'])
    @use_kwargs(products_router_model.ProductPostSchema, location="form")
    @marshal_with(products_router_model.ProductCommonResponse, code=201)
    def post(self, **kwargs):
        db, cursor = db_init()
        products = {
            'name': kwargs['name'],
            'price': kwargs['price'],
            'amount': kwargs['amount']
        }

        sql = """

        INSERT INTO `shop`.`goods` (`name`,`price`,`amount`)
        VALUES ('{}','{}','{}');

        """.format(
            products['name'], products['price'], products['amount'])
        result = cursor.execute(sql)
        db.commit()  # 測試,將執行成功的結果存進database裡
        db.close()

        if result == 0:
            return util.failure({"message": "error"})

        return util.success()


class Product(MethodResource):
    #get Products by id
    @doc(description='Get Single Products info.', tags=['商品庫存'])
    @marshal_with(products_router_model.ProductGetResponse, code=200)
    def get(self, id):
        db, cursor = db_init()
        sql = f"SELECT * FROM shop.goods WHERE id = '{id}';"
        cursor.execute(sql)
        products = cursor.fetchall()
        db.close()
        return util.success(products)

    #patch Products
    @doc(description='Update Products info.', tags=['商品庫存'])
    @use_kwargs(products_router_model.ProductPatchSchema, location="form")
    @marshal_with(products_router_model.ProductCommonResponse, code=201)
    def patch(self, id, **kwargs):
        db, cursor = db_init()
        products = {
            'name': kwargs.get('name'),
            'price': kwargs.get('price'),
            'amount': kwargs.get('amount')
        }

        query = []
        for key, value in products.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)

        sql = """
            UPDATE `shop`.`goods`
            SET {}
            WHERE id = {};
        """.format(query, id)

        result = cursor.execute(sql)
        db.commit()
        db.close()
        if result == 0:
            return util.failure({"message": "error"})

        return util.success()

#Cart
class Cart(MethodResource):
    #藉由account，查詢購物車所有內容
    @doc(description='Get Cart info.', tags=['購物車']) 
    @use_kwargs(products_router_model.CartGetSchema, location="query") 
    def get(self, **kwargs):
        db, cursor = db_init()
        account = kwargs.get("account")
        if account is not None:
            sql = f"SELECT * FROM shop.cart WHERE account = '{account}';"
        else:
            sql = 'SELECT * FROM shop.cart;'
        cursor.execute(sql)
        cartlist = cursor.fetchall()
        db.close()
        return util.success(cartlist)

    #增添商品至購物車內
    @doc(description='Cart', tags=['購物車'])
    @use_kwargs(products_router_model.CartPostSchema, location="form")
    def post(self, **kwargs):
        db, cursor = db_init()
        name, amount,account = kwargs["name"], kwargs["amount"], kwargs["account"]
        #step1:從商品庫存中找出商品
        sql_selcet = f"SELECT * FROM shop.goods WHERE name ='{name}';"
        cursor.execute(sql_selcet)
        products = cursor.fetchall()

        #step2:判斷是否庫存足夠，再塞進購物車
        if int(amount)>products[0]["amount"]:
            return util.failure({"message":"庫存量不足"})

        else:
            total=int(amount)*products[0]["price"]
            sql_cart ="""

            INSERT INTO `shop`.`cart` (`account`,`name`,`price`,`amount`)
            VALUES ('{}','{}','{}','{}');

            """.format(
                account,name, total, amount)
            cursor.execute(sql_cart)
            cart={
                "購買會員":account,
                "購買商品":name,
                "購買總額":total,
                "購買數量":amount,
                }
            
            #step3:從商品庫存中扣除商品
            amount=products[0]["amount"]-int(amount)
            id=products[0]["id"]
            sql_goods =f'UPDATE `shop`.`goods` SET amount={amount} WHERE id = {id};'
            cursor.execute(sql_goods)
            db.commit()
            db.close()
        return  util.success(cart)
       
        
        