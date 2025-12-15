"""
Custom exceptions for the project
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class CustomAPIException(APIException):
    """Base custom API exception"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A server error occurred.'
    default_code = 'error'


class NotFoundException(APIException):
    """Resource not found exception"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found.'
    default_code = 'not_found'


class ValidationException(APIException):
    """Validation error exception"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Validation error.'
    default_code = 'validation_error'


class PermissionDeniedException(APIException):
    """Permission denied exception"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Permission denied.'
    default_code = 'permission_denied'
