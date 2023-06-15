from src.web.app import app
from src.web import views


def run_server() -> None:
  app.run(host='localhost', port=8000)
