responses_204 = {
    204: {"description": "Zero rezult"},
}

responses_get_user = {
    **responses_204,
    200: {
        "description": "Get user",
    },
}

responses_post_user = {
    200: {
        "description": "User create",
    },
    201: {
        "description": "User create",
    },
}

responses_update_user = {
    200: {
        "description": "User updated",
    },
}

responses_delete_user = {
    200: {
        "description": "User delete",
    },
}
