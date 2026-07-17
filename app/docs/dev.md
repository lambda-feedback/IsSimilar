# IsSimilar

This simple evaluation function checks if the supplied response is within a tolerance range defined in `params`. Works exactly like the [numpy.isclose](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html#numpy.isclose) function.

Valid params include `atol` and `rtol`, which can be used in combination, or alone. As the comparison made is the following:

```python
is_correct = abs(res - ans) <= (atol + rtol*abs(ans))
```

Alternatively, `sig_figs` (or `significant_figures`) can be supplied to round both `res` and `ans` to N significant figures and require them to be equal:

```python
is_correct = round_to_sig_figs(res, sig_figs) == round_to_sig_figs(ans, sig_figs)
```

`sig_figs` cannot be combined with `atol`/`rtol` — supplying both raises an exception.

## Inputs

```json
{
  "response": "<number>",
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