from ninja import Schema


class BaseJsonResponse(Schema):
    status: str


class SuccessJsonResponse(BaseJsonResponse):
    status = "success"


class FailJsonResponse(BaseJsonResponse):
    status = "error"
    errors: dict[int, str]
