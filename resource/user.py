import pymysql
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
import util
from . import user_router_model
from flask_jwt_extended import create_access_token, jwt_required
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

def get_access_token(account): #token
    token = create_access_token(
        identity={"account": account},
        expires_delta=timedelta(days=1)
    )
    return token

####### API Action #########

class Users(MethodResource):
    # GET_ALL
    @doc(description='Get Users info.', tags=['會員中心']) #框架
    @use_kwargs(user_router_model.UserGetSchema, location="query") #功能
    @marshal_with(user_router_model.UserGetResponse, code=200) #範例
    @jwt_required()
    def get(self, **kwargs):
        db, cursor = db_init()
        name = kwargs.get("name")
        if name is not None:
            sql = f"SELECT * FROM shop.members WHERE name = '{name}';"
        else:
            sql = 'SELECT * FROM shop.members;'
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close() #一定要加close,不然db會爆掉
        return util.success(users)

    # POST
    @doc(description='Create User.', tags=['會員中心'])
    @use_kwargs(user_router_model.UserPostSchema, location="form")
    @marshal_with(user_router_model.UserCommonResponse, code=201)
    def post(self, **kwargs):
        db, cursor = db_init()
        user = {
            'name': kwargs['name'],
            'account': kwargs['account'],
            'password': kwargs['password'],
            'gender': kwargs['gender'],
            'birth': kwargs.get('birth') or '1900-01-01',
            'note': kwargs.get('note'),
        }

        sql = """

        INSERT INTO `shop`.`members` (`name`,`gender`,`account`,`password`,`birth`,`note`)
        VALUES ('{}','{}','{}','{}','{}','{}');

        """.format(
            user['name'], user['gender'], user['account'], user['password'], user['birth'], user['note'])
        result = cursor.execute(sql)
        db.commit()  # 測試,將執行成功的結果存進database裡
        db.close()

        if result == 0:
            return util.failure({"message": "error"})

        return util.success()


class User(MethodResource):
    @doc(description='Get Single user info.', tags=['會員中心'])
    @marshal_with(user_router_model.UserGetResponse, code=200)
    # @jwt_required()
    def get(self, id):
        db, cursor = db_init()
        sql = f"SELECT * FROM shop.members WHERE id = '{id}';"
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return util.success(users)
    #patch
    @doc(description='Update User info.', tags=['會員中心'])
    @use_kwargs(user_router_model.UserPatchSchema, location="form")
    @marshal_with(user_router_model.UserCommonResponse, code=201)
    def patch(self, id, **kwargs):
        db, cursor = db_init()
        user = {
            'name': kwargs.get('name'),
            'account': kwargs.get('account'),
            'password': kwargs.get('password'),
            'gender': kwargs.get('gender'),
            'birth': kwargs.get('birth') or '1900-01-01',
            'note': kwargs.get('note')
        }

        query = []
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)

        sql = """
            UPDATE `shop`.`members`
            SET {}
            WHERE id = {};
        """.format(query, id)

        result = cursor.execute(sql)
        db.commit()
        db.close()
        if result == 0:
            return util.failure({"message": "error"})

        return util.success()

    @doc(description='Delete User info.', tags=['User'])
    @marshal_with(None, code=204)
    def delete(self, id):
        db, cursor = db_init()
        sql = f'DELETE FROM shop.members WHERE id = {id};'
        result = cursor.execute(sql)
        db.commit()
        db.close()
        

class Login(MethodResource):
    @doc(description='User Login', tags=['會員登入'])
    @use_kwargs(user_router_model.LoginSchema, location="form")
    #@marshal_with(user_router_model.UserGetResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        account, password = kwargs["account"], kwargs["password"]
        sql = f"SELECT * FROM shop.members WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()

        if user != ():
            token = get_access_token(account)
            data = {
                "message": f"Welcome back {user[0]['name']}",
                "token": token}
            return util.success(data)
        
        return util.failure({"message":"Account or password is wrong"})
