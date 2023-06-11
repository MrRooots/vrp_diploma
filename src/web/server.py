from src.web.app import app
from src.web.view import *


def run_server() -> None:
  app.run(host='localhost', port=8000)
