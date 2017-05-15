from flask import Flask
from flask_backstage import Admin

app = Flask(__name__)

# 添加csrf保护配置
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'admin'

admin = Admin(app)

app.run()