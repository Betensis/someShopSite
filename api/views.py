from django.http import JsonResponse
from django.shortcuts import render

from api.schemas.cart import get_error_json_response


def placeholder_view(request):
    return JsonResponse(get_error_json_response({228: "Url not exist yet"}))
