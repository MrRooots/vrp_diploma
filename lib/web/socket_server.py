import socket
import json

from lib.web.data.enums import RequestMethod, ResponseCode
from lib.web.interfaces.i_socket_server import ISocketServer
from lib.web.views.views import Views

ADDRESS = 'localhost'
PORT = 5000
URLS = {
  '/': Views.index,
  '/solve': Views.solve_vrp,
  '/static/scripts.js': Views.load_scripts,
  '/static/style.css': Views.load_styles,
}


class SocketServer(ISocketServer):
  def __init__(self):
    self._server_socket = SocketServer._initialize_socket()

  @staticmethod
  def _initialize_socket() -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((ADDRESS, PORT))
    server_socket.listen()

    return server_socket

  @staticmethod
  def _parse_request(request: str) -> tuple[str, str, dict | None]:
    parsed = request.split('\r\n')
    method, url, _ = parsed[0].split(' ')
    host = parsed[1].split(' ')[-1]
    data = json.loads(parsed[-1]) if method == 'POST' else None

    return method, url, data

  @staticmethod
  def _generate_header(method: str, url: str) -> tuple[str, int]:
    if method not in (RequestMethod.GET, RequestMethod.POST):
      header, code = 'HTTP/1.1 405 Method not allowed', ResponseCode.METHOD_NOT_ALLOWED
    elif url not in URLS:
      header, code = 'HTTP/1.1 404 Not found', ResponseCode.NOT_FOUND
    else:
      header, code = 'HTTP/1.1 200 OK', ResponseCode.SUCCESS

    return f'{header}\r\n\r\n', code

  @staticmethod
  def _generate_content(code, url, data=None) -> str:
    if code == ResponseCode.NOT_FOUND:
      return Views.not_found()
    elif code == ResponseCode.METHOD_NOT_ALLOWED:
      return '<h1>405</h1><p>Method not allowed</p>'
    elif code == ResponseCode.SERVER_FAILURE:
      return Views.internal_server_error()
    else:
      return URLS[url]() if data is None else URLS[url](data)

  @staticmethod
  def _generate_response(request: str) -> bytes:
    try:
      method, url, data = SocketServer._parse_request(request)
      headers, code = SocketServer._generate_header(method, url)
      body = SocketServer._generate_content(code, url, data)

      return (headers + body).encode('utf-8')
    except IndexError:
      return b''

  def run(self) -> None:
    print(f'Server started at: {ADDRESS}:{PORT}')

    while True:
      client_socket, address = self._server_socket.accept()
      request = client_socket.recv(1024).decode('utf-8')

      if request:
        print('Incoming request: {}'.format(request.split('\r\n')[0]))

        response = self._generate_response(request)
        client_socket.sendall(response)

      client_socket.close()
