from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)


class Config(object):
    """配置引數"""
    # 設定連線資料庫的URL
    user = 'root'
    password = "zxc123109"
    database = 'flask_test'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@127.0.0.1:3306/%s' % (user, password, database)

    # 設定sqlalchemy自動更跟蹤資料庫
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查詢時會顯示原始SQL語句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自動提交資料處理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False


# 讀取配置
app.config.from_object(Config)

# 建立資料庫sqlalchemy工具物件
db = SQLAlchemy(app)


class Role(db.Model):
    # 定義表名
    __tablename__ = 'roles'
    # 定義欄位
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')  # 反推與role關聯的多個User模型物件


class User(db.Model):
    # 定義表名
    __tablename__ = 'users'
    # 定義欄位
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    pswd = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 設定外來鍵


if __name__ == '__main__':

    # 刪除所有表
    db.drop_all()

    # 建立所有表
    db.create_all()

    # 插入一條角色資料
    role1 = Role(name='admin')
    db.session.add(role1)
    db.session.commit()

    # 再次插入一條資料
    role2 = Role(name='user')
    db.session.add(role2)
    db.session.commit()
