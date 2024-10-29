from schemas.status_code_valid import ResponseMessage

responses_204 = {
    204: {"description": "No content"},
}
responses_403 = {
    403: {"model": ResponseMessage, "description": "You have not power here"},
}
responses_422 = {
    422: {"model": ResponseMessage, "description": "Some proplem with validation"},
}
responses_498 = {
    498: {"model": ResponseMessage, "description": "Special problem"},
}
responses_get_responses = {
    **responses_204,
    **responses_403,
    200: {
        "description": "Get response\\es",
    },
}

responses_post_responses = {
    **responses_403,
    **responses_498,
    201: {
        "description": "response create",
    },
    200: {
        "description": "response create",
    },
}

responses_update_responses = {
    **responses_204,
    **responses_403,
    **responses_422,
    200: {
        "description": "response updated",
    },
}
responses_delete_responses = {
    **responses_204,
    **responses_403,
    200: {
        "description": "response delete",
    },
}
