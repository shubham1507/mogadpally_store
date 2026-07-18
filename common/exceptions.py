from rest_framework.views import exception_handler

from .responses import ApiResponse


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is None:
        return response

    return ApiResponse.error(
        message="Request failed",
        errors=response.data,
        status_code=response.status_code,
    )