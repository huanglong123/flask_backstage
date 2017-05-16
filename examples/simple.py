from flask import Flask
from flask_backstage import Admin

app = Flask(__name__)

admin = Admin(app)

app.run()