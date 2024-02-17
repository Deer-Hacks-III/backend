from authlib.integrations.flask_client import OAuth
from flask import Flask

app = Flask(__name__)


oauth = OAuth(app)
