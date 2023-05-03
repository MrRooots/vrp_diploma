class ResponseCode:
  """
  Available response codes
  """
  SUCCESS = 200
  NOT_FOUND = 404
  METHOD_NOT_ALLOWED = 405
  SERVER_FAILURE = 500


class RequestMethod:
  """
  Available request methods
  """
  GET = 'GET'
  POST = 'POST'
  PATCH = 'PATCH'
  DELETE = 'DELETE'
