from typing import NoReturn

from fastapi import HTTPException, status

from services.exceptions import ConflictError, NotFoundError


def raise_http_error(error: Exception) -> NoReturn:
    if isinstance(error, NotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    if isinstance(error, ConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    raise error
