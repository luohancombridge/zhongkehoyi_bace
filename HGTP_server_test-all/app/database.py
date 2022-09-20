__author__ = 'SUNZHEN519'
from app import db
from fileconfig import SQLALCHEMY_DATABASE_URI
from fileconfig import SQLALCHEMY_MIGRATE_REPO
from app import db
ROLE_USER = 0
ROLE_ADMIN = 1
import os.path
class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    benname = db.Column(db.String(64),index = True)
    leiname = db.Column(db.String(120),)

    def __repr__(self):
        return '<User %r,%r>' % (self.benname,self.leiname)
db.create_all()
admin_role = user(benname='sss',leiname='qwqwqwqwq')
db.session.add(admin_role)
db.session.commit()

#增加运行表格，第一个字段为用户名，第二个字段为运行时间，第三个字段为运行方式，第四个字段为是否运行标志位
#type=1 及时运行  2  计划运行   statu=0 运行完毕 ，2未运行
#create table runing(user nvarchar(50),time nvarchar(50),type nvarchar(300),statu nvarchar(300)))




#增加非自动化脚本类表格
#create table runing(user nvarchar(50),time nvarchar(50),type nvarchar(300),statu nvarchar(300)))