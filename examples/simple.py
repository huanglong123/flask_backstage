from flask import Flask
from flask_backstage import Admin

app = Flask(__name__)

# 添加csrf保护配置
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = '0\xda\xb3+xAj\x88\x98\x00\x02\xcaR\x9d\xb5QD\x0c\x1aX"\x89{S'

admin = Admin(app)

app.run()