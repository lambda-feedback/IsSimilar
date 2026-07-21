from numpy import spacing


def _is_number(value):
    return isinstance(value, int) or isinstance(value, float)


def _round_to_sig_figs(value, sig_figs):
    if value == 0:
        return 0.0
    return float(f"{value:.{sig_figs}g}")


def _split_numeric_string(value):
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    body = stripped[1:] if stripped[:1] in ("+", "-") else stripped

    mantissa, sep, exponent = body.partition("e") if "e" in body else body.partition("E")
    if sep and not exponent.lstrip("+-").isdigit():
        return None

    has_decimal = "." in mantissa
    int_part, _, frac_part = mantissa.partition(".")
    if not (int_part.isdigit() or frac_part.isdigit()):
        return None
    if int_part and not int_part.isdigit():
        return None
    if frac_part and not frac_part.isdigit():
        return None

    return int_part, frac_part, has_decimal


def _count_sig_figs(int_part, frac_part, has_decimal):
    digits = int_part + frac_part
    first_nonzero = next((i for i, d in enumerate(digits) if d != "0"), None)
    if first_nonzero is None:
        return 1

    trimmed = digits[first_nonzero:]
    if has_decimal:
        return len(trimmed)
    return len(trimmed.rstrip("0")) or 1


def _result(is_correct, real_diff, allowed_diff, feedback=""):
    return {
        "is_correct": bool(is_correct),
        "real_diff": real_diff,
        "allowed_diff": allowed_diff,
        "feedback": feedback,
    }


def _evaluate_sig_figs(response, answer, sig_figs):
    parts = _split_numeric_string(response)
    if parts is None:
        return _result(False, None, None, "Please enter a number.")

    response_value = float(response)
    rounded_answer = _round_to_sig_figs(answer, sig_figs)
    rounded_response = _round_to_sig_figs(response_value, sig_figs)
    numeric_correct = abs(rounded_response - rounded_answer) <= spacing(abs(rounded_answer))

    precision_correct = response_value == 0 or _count_sig_figs(*parts) == sig_figs
    is_correct = numeric_correct and precision_correct

    feedback = ""
    if numeric_correct and not precision_correct:
        feedback = f"Please give your answer to {sig_figs} significant figures."

    return _result(is_correct, abs(response_value - answer), None, feedback)


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
