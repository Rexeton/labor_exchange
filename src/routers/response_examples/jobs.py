from schemas.status_code_valid import JobMessage

responses_204 = {
    204: {"description": "Zero rezult"},
}
responses_403 = {
    403: {"model": JobMessage, "description": "You have not power here"},
}
responses_422 = {
    422: {"model": JobMessage, "description": "Some proplem with validation"},
}

responses_get_jobs = {
    **responses_204,
    200: {
        "description": "Get job",
    },
}

responses_post_jobs = {
    **responses_403,
    201: {
        "description": "job create",
    },
    200: {
        "description": "job create",
    },
}

responses_update_jobs = {
    **responses_204,
    **responses_403,
    200: {
        "description": "job updated",
    },
}
responses_delete_jobs = {
    **responses_204,
    **responses_403,
    200: {
        "description": "job delete",
    },
}
