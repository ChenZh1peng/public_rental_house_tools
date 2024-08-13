from enum import Enum, unique

@unique
class RequestType(Enum):
    """Enum types for Requests Library
    """
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'