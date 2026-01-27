# """
# Swagger API 文档配置,推荐使用apifox测试接口 有需要可自行打开注释
# 提供自动生成的 API 文档和交互式界面
# """
# from flask_restx import Api, fields, Namespace
# from flask import Blueprint
#
# api_bp = Blueprint('api_doc', __name__, url_prefix='/api/v1')
#
# # Swagger 配置
# api = Api(
#     api_bp,
#     title='Flask-Py API',
#     version='1.0',
#     description='一个企业级 Flask 应用的 API 文档',
#     doc='/docs',  # 访问 /api/v1/docs 查看文档
#     prefix=''
# )
#
# # 定义响应模型
# success_model = api.model('SuccessResponse', {
#     'status': fields.String(required=True, description='状态'),
#     'message': fields.String(required=True, description='消息'),
#     'data': fields.Raw(description='响应数据'),
# })
#
# error_model = api.model('ErrorResponse', {
#     'status': fields.String(required=True, description='状态'),
#     'message': fields.String(required=True, description='错误信息'),
#     'code': fields.String(description='错误代码'),
# })
#
# # 用户模型
# user_model = api.model('User', {
#     'id': fields.Integer(description='用户ID'),
#     'username': fields.String(required=True, description='用户名'),
#     'email': fields.String(required=True, description='邮箱'),
#     'created_at': fields.DateTime(description='创建时间'),
# })
#
# register_model = api.model('Register', {
#     'username': fields.String(required=True, description='用户名'),
#     'email': fields.String(required=True, description='邮箱'),
#     'password': fields.String(required=True, description='密码'),
# })
#
# login_model = api.model('Login', {
#     'email': fields.String(required=True, description='邮箱或用户名'),
#     'password': fields.String(required=True, description='密码'),
# })
#
#
# # 健康检查的文档
# health_ns = api.namespace('health', description='健康检查')
#
# health_response = api.model('HealthResponse', {
#     'status': fields.String(description='状态'),
#     'message': fields.String(description='消息'),
#     'database': fields.String(description='数据库连接状态'),
# })
#
# # 认证命名空间
# auth_ns = api.namespace('auth', description='用户认证')
#
# # 健康检查 Resource
# from flask_restx import Resource
#
# @health_ns.route('')
# class HealthCheck(Resource):
#     @health_ns.doc('health_check')
#     @health_ns.marshal_with(health_response)
#     def get(self):
#         """获取应用健康状态"""
#         return {
#             'status': 'healthy',
#             'message': 'Application is running'
#         }, 200
#
#
# @health_ns.route('/readiness')
# class ReadinessCheck(Resource):
#     @health_ns.doc('readiness_check')
#     @health_ns.marshal_with(health_response)
#     def get(self):
#         """获取应用就绪状态"""
#         try:
#             from app.extensions.extensions import db
#             db.session.execute('SELECT 1')
#             db.session.commit()
#             return {
#                 'status': 'ready',
#                 'message': 'Application is ready to serve traffic',
#                 'database': 'connected'
#             }, 200
#         except Exception as e:
#             return {
#                 'status': 'not_ready',
#                 'message': 'Application is not ready',
#                 'database': 'disconnected'
#             }, 503
#
#
# # 认证 Resource
# @auth_ns.route('/register')
# class Register(Resource):
#     @auth_ns.expect(register_model)
#     @auth_ns.marshal_with(success_model)
#     @auth_ns.response(400, 'Validation Error')
#     def post(self):
#         """用户注册"""
#         from flask import g
#         from app.services import register_user
#         from app.utils import success, error
#
#         data = api.payload
#         try:
#             result = register_user(data)
#             return success(result)
#         except ValueError as e:
#             return error(code='400', message=str(e))
#
#
# @auth_ns.route('/login')
# class Login(Resource):
#     @auth_ns.expect(login_model)
#     @auth_ns.marshal_with(success_model)
#     @auth_ns.response(401, 'Authentication Failed')
#     def post(self):
#         """用户登录"""
#         from app.services.auth_service import user_login
#         from app.utils import success, error
#
#         data = api.payload
#         try:
#             result = user_login(data.get('email'), data.get('username'), data.get('password'))
#             return success(result)
#         except Exception as e:
#             return error(code='401', message=str(e))
