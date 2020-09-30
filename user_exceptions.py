class UnexpectedRequestError(Exception):
    def __init__(self):
        pass


class PhotoError(Exception):
    pass


class InvalidPhotoError(PhotoError):
    def __init__(self, message):
        self.message = message


class NotFoundError(PhotoError):
    def __init__(self, message):
        self.message = message


class PhotoCountError(PhotoError):
    def __init__(self, message):
        self.message = message


class FaceDataError(PhotoError):
    def __init__(self, message):
        self.message = message

