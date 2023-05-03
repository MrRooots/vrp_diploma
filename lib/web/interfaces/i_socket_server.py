import socket


class ISocketServer:
  """
  Simplest socket server
  """

  @staticmethod
  def _initialize_socket() -> socket.socket:
    """ Initialize server socket """

  @staticmethod
  def _parse_request(request: str) -> tuple[str, str]:
    """ Parse given request. Get method and code """

  @staticmethod
  def _generate_header(method: str, url: str) -> tuple[str, int]:
    """ Generate response header """

  @staticmethod
  def _generate_content(code, url, data=None) -> str:
    """ Generate response content """

  @staticmethod
  def _generate_response(request: str) -> bytes:
    """ Generate response based on given request """

  def run(self) -> None:
    """ Start server """
