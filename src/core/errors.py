from rest_framework.exceptions import APIException


class CodeExpired(APIException):
    status_code = 400
    default_detail = 'Email code has been expired'
    default_code = 'code_expired'