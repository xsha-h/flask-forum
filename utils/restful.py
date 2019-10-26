class HttpCode(object):
    ok = 200
    paramserror = 400
    unautherror = 401
    servererror = 500


def restful_result(code, message, data):
    return {
        "code": code,
        "message": message,
        "data": data,
    }


def success(message="", data=None):
    return restful_result(code=HttpCode.ok, message=message, data=data)


def params_error(message=""):
    return restful_result(code=HttpCode.paramserror, message=message, data=None)


def unauth_error(message=""):
    return restful_result(code=HttpCode.unautherror, message=message, data=None)


def server_error(message=""):
    return restful_result(code=HttpCode.servererror, message=message, data=None)
