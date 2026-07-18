from drf_spectacular.utils import OpenApiResponse

UNAUTHORIZED_RESPONSE = OpenApiResponse(
    description="Authentication credentials were not provided."
)

NOT_FOUND_RESPONSE = OpenApiResponse(
    description="Requested resource not found."
)

BAD_REQUEST_RESPONSE = OpenApiResponse(
    description="Invalid request."
)