from fastapi import HTTPException


class ResourceNotFoundException(HTTPException):
    def __init__(self, resource_name: str, resource_id: int):
        detail = f"{resource_name} with id {resource_id} not found"
        super().__init__(status_code=404, detail=detail)


class ResourceAlreadyExistsException(HTTPException):
    def __init__(self, resource_name: str, resource_id: int):
        detail = f"{resource_name} with id {resource_id} already exists"
        super().__init__(status_code=409, detail=detail)


class InvalidRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)