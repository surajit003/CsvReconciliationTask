class FileUploadError(Exception):
    pass


class InvalidFileHeaderError(FileUploadError):
    pass

