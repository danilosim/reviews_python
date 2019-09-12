import datetime
import numbers

import app.utils.errors as errors
import app.utils.schema_validator as validator

REVIEW_DB_SCHEMA = {
    "title": {
        "required": True,
        "type": str,
        "minLen": 1,
        "maxLen": 60
        },
    "description": {
        "required": True,
        "type": str,
        "maxLen": 2048
        },
    "rating": {
        "required": True,
        "type": str,
        "minLen": 30,
        "maxLen": 40
        },
    "price": {
        "required": False,
        "type": numbers.Real,
        "min": 0
        },
    "stock": {
        "required": False,
        "type": numbers.Integral,
        "min": 0
        }
}