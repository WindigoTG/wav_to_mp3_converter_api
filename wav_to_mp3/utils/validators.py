import re
from abc import ABC, abstractmethod
from typing import Any

from fastapi import HTTPException, UploadFile, status


class FileValidator(ABC):
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def __call__(self, file: UploadFile) -> Any:
        pass


class AllowedExtensions(FileValidator):
    def __init__(self, allowed_extensions: str) -> None:
        self.allowed_extensions = allowed_extensions

    @property
    def description(self) -> str:
        return "Allowed extensions: {}".format(self.allowed_extensions)

    def __call__(self, file: UploadFile) -> Any:
        if not re.match(
                r"^.*\.({})$".format(self.allowed_extensions),
                file.filename,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file extension.",
            )
        return file


class LimitedSize(FileValidator):
    def __init__(self, size_limit: int) -> None:
        self.size_limit = size_limit

    @property
    def description(self) -> str:
        return "File size limit: {} bytes".format(self.size_limit)

    def __call__(self, file: UploadFile) -> Any:
        if file.size > self.size_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size is too large.",
            )
        return file


def validated(initial_file: UploadFile, *validators: FileValidator):
    initial_file.description = "{}\n- {}".format(
        initial_file.description or "",
        "\n- ".join(validator.description for validator in validators)
    )

    def validate(file: UploadFile = initial_file):
        for validator in validators:
            validator(file)
        return file

    return validate
