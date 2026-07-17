# IsSimilar

This simple evaluation function checks if the supplied response is within a tolerance range defined in `params`. Works exactly like the [numpy.isclose](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html#numpy.isclose) function.

Valid params include `absolute_tolerance` and `relative_tolerance`, which can be used in combination, or alone. As the comparison made is the following:

```python
is_correct = abs(res - ans) <= (absolute_tolerance + relative_tolerance*abs(ans))
```

## Inputs

```json
{
  "response": "<number>",
  "answer": "<number>",
  "params": {
    "absolute_tolerance": "<number>",
    "relative_tolerance": "<number>"
  }
}
```

### `absolute_tolerance`

Absolute tolerance parameter

### `relative_tolerance`

Relative tolerance parameter

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
Allowed difference between answer and response, calculated using the supplied `absolute_tolerance` and `relative_tolerance` parameters


## Examples