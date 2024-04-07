class BadRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 400


class NotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 404


class ConflictException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 409


class InternalServerErrorException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 500