from django.http import JsonResponse


def get_ok_json_response():
    return JsonResponse(
        {
            "status": "success",
        }
    )


def get_error_json_response(errors: dict[int, str]):
    return JsonResponse(
        {"status": "error"} | {"errors": errors},
    )
