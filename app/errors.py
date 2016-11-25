from werkzeug.exceptions import HTTPException


class TenantNotFound(HTTPException):
    def __init__(self, data):
        self.code = 404
        self.data = data
        HTTPException.__init__(self)


class BindAddressFail(HTTPException):
    def __init__(self, code, addr, namespace):
        self.code = code
        self.data = {
            'message': "fail binding address %s to tenant %s " % (addr, namespace)
        }
        HTTPException.__init__(self)


class Unauthorized(HTTPException):
    def __init__(self):
        self.code = 401
        self.data = {
            'message': "invalid auth token."
        }
        HTTPException.__init__(self)
