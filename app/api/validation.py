# from typing import Type, Dict, Any

# from pydantic import ValidationError

# from fastapi import status
# from fastapi.encoders import jsonable_encoder
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse

# from database.schema import SCHEMA_TYPE_SELECT, SCHEMA_TYPE_CREATE, SCHEMA_TYPE_PATCH


# SCHEMA_TYPE = Type(SCHEMA_TYPE_SELECT) | Type(SCHEMA_TYPE_CREATE) | Type(SCHEMA_TYPE_PATCH)

# def validate(schema: SCHEMA_TYPE, data: Dict[str, Any], exclude_none: bool = True) -> dict:
#     try:
#         validated = schema(**data).dict(exclude_none=exclude_none)
#     except ValidationError as error:
#         raise JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": RequestValidationError.errors(), "body": RequestValidationError.body}),
#     )
#     return validated