from schemas.responses import ResponsesSchema
from schemas.status_code_valid import Response_message

responses = {
    204: {"description": "Zero rezult"},
    403: {"model": Response_message, "description": "You have not power here"},
    422: {"model": Response_message, "description": "Some proplem with validation"},
}
responses_get_responses = {
    **responses,
    200: {
        "description": "Get response\\es",
        "model": ResponsesSchema,
    },
}

responses_post_responses = {
    **responses,
    201: {
        "description": "response create",
        "model": ResponsesSchema,
    },
    200: {
        "description": "response create",
        "model": ResponsesSchema,
    },
}

responses_update_responses = {
    **responses,
    200: {
        "description": "response updated",
        "model": ResponsesSchema,
    },
}
responses_delete_responses = {
    **responses,
    200: {
        "description": "response delete",
        "model": ResponsesSchema,
    },
}
