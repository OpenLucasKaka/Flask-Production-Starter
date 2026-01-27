"""
测试基础配置和 Fixtures
"""
import pytest
from app import create_app
from app.extensions.extensions import db
from config import DevConfig


@pytest.fixture(scope='session')
def app():
    """创建测试应用"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    return app


@pytest.fixture(scope='session')
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture(scope='function')
def db_init(app):
    """在每个测试前创建数据库表，测试后清理"""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture
def runner(app):
    """CLI 测试运行器"""
    return app.test_cli_runner()
