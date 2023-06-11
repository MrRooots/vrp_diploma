from flask import Flask

from src.web.config import Config

app = Flask(__name__)
app.config.from_object(Config)
