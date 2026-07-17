from numpy import spacing


def _is_number(value):
    return isinstance(value, int) or isinstance(value, float)


def _round_to_sig_figs(value, sig_figs):
    if value == 0:
        return 0.0
    return float(f"{value:.{sig_figs}g}")


def _result(is_correct, real_diff, allowed_diff, feedback=""):
    return {
        "is_correct": bool(is_correct),
        "real_diff": real_diff,
        "allowed_diff": allowed_diff,
        "feedback": feedback,
    }


def _evaluate_sig_figs(response, answer, sig_figs):
    if not _is_number(response):
        return _result(False, None, None, "Please enter a number.")

    rounded_answer = _round_to_sig_figs(answer, sig_figs)
    rounded_response = _round_to_sig_figs(response, sig_figs)
    is_correct = abs(rounded_response - rounded_answer) <= spacing(abs(rounded_answer))

    return _result(is_correct, abs(response - answer), None)


def _evaluate_tolerance(response, answer, relative_tolerance, absolute_tolerance):
    allowed_diff = absolute_tolerance + relative_tolerance * abs(answer) + spacing(answer)

    if not _is_number(response):
        return _result(False, None, allowed_diff, "Please enter a number.")

    real_diff = abs(response - answer)

    return _result(real_diff <= allowed_diff, real_diff, allowed_diff)


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

    sig_figs = params.get("significant_figures", params.get("sig_figs"))
    relative_tolerance = params.get("relative_tolerance", params.get("rtol", 0))
    absolute_tolerance = params.get("absolute_tolerance", params.get("atol", 0))

    uses_tolerance = any(
        key in params
        for key in ("relative_tolerance", "rtol", "absolute_tolerance", "atol")
    )

    if sig_figs is not None and uses_tolerance:
        raise Exception(
            "significant_figures/sig_figs cannot be used together with "
            "relative_tolerance/rtol or absolute_tolerance/atol."
        )

    if sig_figs is not None and (not isinstance(sig_figs, int) or sig_figs < 1):
        raise Exception("significant_figures must be a positive integer.")

    if not _is_number(answer):
        raise Exception("Answer must be a number.")

    if sig_figs is not None:
        return _evaluate_sig_figs(response, answer, sig_figs)
    return _evaluate_tolerance(response, answer, relative_tolerance, absolute_tolerance)
