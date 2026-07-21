# IsSimilar

This simple evaluation function checks if the supplied response is within a tolerance range defined in `params`. Works exactly like the [numpy.isclose](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html#numpy.isclose) function.

Valid params include `atol` and `rtol`, which can be used in combination, or alone. As the comparison made is the following:

```python
is_correct = abs(res - ans) <= (atol + rtol*abs(ans))
```

Alternatively, `sig_figs` (or `significant_figures`) can be supplied to require both a numeric match and a precision match to N significant figures:

```python
is_correct = (
    round_to_sig_figs(res, sig_figs) == round_to_sig_figs(ans, sig_figs)
    and count_sig_figs(res) == sig_figs
)
```

`sig_figs` cannot be combined with `atol`/`rtol` — supplying both raises an exception.

In `sig_figs` mode, `response` must be a **string** (e.g. `"92.00"`), not a pre-parsed `int`/`float` — significant-figure counting depends on the exact digits written (trailing zeros, decimal point placement), which a parsed number can't preserve (`92.0 == 92.00 == 92`). `_split_numeric_string` in `evaluation.py` validates and decomposes the string (sign / integer part / fractional part / exponent) using `str.isdigit()` on each part; if `response` isn't a string, or isn't a valid numeral, the sig-figs check returns the standard "Please enter a number." result rather than raising. `_count_sig_figs` then applies the standard significant-figures counting rules (non-zero digits always count; zeros between digits count; leading zeros don't; trailing zeros only count if a decimal point was written) to the parsed parts.

## Inputs

```json
{
  "response": "<number | string, use string for sig_figs mode>",
  "answer": "<number>",
  "params": {
    "atol": "<number>",
    "rtol": "<number>",
    "sig_figs": "<int>"
  }
}
```

### `atol`

Absolute tolerance parameter

### `rtol`

Relative tolerance parameter

### `sig_figs`

Significant-figures parameter. Mutually exclusive with `atol`/`rtol`.

## Outputs
```json
{
  "is_correct": "<bool>",
  "real_diff": "<number>",
  "allowed_diff": "<number>",
}
```

### `real_diff`
Real difference between the given answer and response

### `allowed_diff`
Allowed difference between answer and response, calculated using the supplied `atol` and `rtol` parameters


## Examples