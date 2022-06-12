import flask
from flask_restful import Api
from resource.user import Users, User, Login
from resource.product import Product,Products,Cart
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager

# Flask setting
app = flask.Flask(__name__)

# Flask restful setting
api = Api(app)

app.config["DEBUG"] = True # Able to reload flask without exit the process
app.config["JWT_SECRET_KEY"] = "secret_key" #JWT token setting 

# Swagger setting
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Ecommerce Api Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

# URL(router)
api.add_resource(Users, "/users")
docs.register(Users)
api.add_resource(User, "/user/<int:id>")
docs.register(User)
api.add_resource(Login, "/login")
docs.register(Login)
api.add_resource(Products, "/products")
docs.register(Products)
api.add_resource(Product, "/products/<int:id>")
docs.register(Product)
api.add_resource(Cart, "/Cart")
docs.register(Cart)

if __name__ == '__main__':
    # JWT token setting
    jwt = JWTManager().init_app(app)
    app.run(host='127.0.0.1', port=10011)
