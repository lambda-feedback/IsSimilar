from numpy import spacing

def evaluation_function(response, answer, params) -> dict:
    """
    Function used to grade a student response.
    ---
    The handler function passes only one argument to evaluation_function(),
    which is a dictionary of the structure of the API request body
    deserialised from JSON.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. This is also subject to
    standard response specifications.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that evaluation_function() is the main function used
    to output the grading response.
    """

    relative_tolerance = params.get("relative_tolerance", params.get("rtol", 0))
    absolute_tolerance = params.get("absolute_tolerance", params.get("atol", 0))

    if not (isinstance(answer, int) or isinstance(answer, float)):
        raise Exception("Answer must be a number.")

    allowed_diff = absolute_tolerance + relative_tolerance * abs(answer)
    allowed_diff += spacing(answer)

    if not (isinstance(response, int) or isinstance(response, float)):
        return {
            "is_correct": False,
            "real_diff": None,
            "allowed_diff": allowed_diff,
            "feedback": "Please enter a number.",
        }


    real_diff = abs(response - answer)
    is_correct = bool(real_diff <= allowed_diff)

    return {
        "is_correct": is_correct,
        "real_diff": real_diff,
        "allowed_diff": allowed_diff,
        "feedback": "",
    }
