# IsSimilar

Use this evaluation function to check if a student's response is within a tolerance range of the correct answer. Works like the [numpy.isclose](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html#numpy.isclose) function.

A response is accepted if:

```
|response - answer| ≤ atol + rtol × |answer|
```

The left-hand side is the absolute difference between the student's response and the correct answer. The right-hand side is the total allowed difference, made up of a fixed part (`atol`) and a part that scales with the size of the answer (`rtol × |answer|`). A response is marked correct whenever the actual difference does not exceed the allowed difference.

## Parameters

`atol` and `rtol` both default to `0` (exact match required) and can be used individually or together. `sig_figs` is an alternative comparison mode and cannot be used together with `atol`/`rtol`.

### `atol` — Absolute tolerance

Specifies a fixed margin around the answer, regardless of its magnitude. Use this when you know the acceptable error in the same units as the answer.

### `rtol` — Relative tolerance

Specifies an acceptable error as a fraction of the answer's magnitude. Use this when the answer is very large or very small and a percentage-based margin makes more sense than a fixed one.

### `sig_figs` — Significant figures

Checks two things: that the response's numeric value rounds to the same value as the answer at the given number of significant figures, and that the response was itself *written* with exactly that many significant figures. Use this when correctness is defined in terms of precision (e.g. "correct to 3 significant figures") rather than a fixed or proportional margin. Cannot be combined with `atol`/`rtol` — supplying both raises an error.

In `sig_figs` mode, **`response` must be supplied as a string** (e.g. `"92.00"`, not `92.0`), so that trailing zeros and decimal points are preserved exactly as written — a parsed number can't distinguish `92` from `92.00`. If `response` isn't a string, or isn't a valid number, the student is asked to enter a number, the same as any other non-numeric response.

Significant figures are counted as follows:
- All non-zero digits are significant.
- Zeros between non-zero digits are significant (e.g. `2051` has 4).
- Leading zeros are not significant (e.g. `0.0032` has 2).
- Trailing zeros after a decimal point are significant (e.g. `92.00` has 4).
- Trailing zeros in a whole number are only significant if a decimal point is shown (e.g. `540` has 2, but `540.` has 3).
- In scientific notation, only the digits before the exponent count (e.g. `5.02e4` has 3).

## Examples

### Exact match (default)

No params needed. The student must enter exactly `42` (floating-point precision is handled automatically).

### Absolute tolerance

```json
{ "atol": 0.05 }
```

With answer `9.81`, accepts any response in the range **9.76 – 9.86**. Good for physical measurements where the acceptable error is known in the same units.

### Relative tolerance

```json
{ "rtol": 0.01 }
```

With answer `6.674e-11`, accepts any response within **1%** of the answer. Good for very large or very small values where a fixed margin would be impractical.

### Combined tolerances

```json
{ "atol": 0.01, "rtol": 0.005 }
```

Both tolerances contribute: with answer `9.81`, the allowed difference is `0.01 + 0.005 × 9.81 ≈ 0.059`. Useful when you want a minimum floor (`atol`) plus a proportional allowance (`rtol`).

### Significant figures

```json
{ "sig_figs": 3 }
```

With answer `3.14159`, the response `"3.14"` is accepted (correct value, 3 significant figures). `"3.1"` is rejected for having too few significant figures, and `"3.14159"` is rejected for having too many — even though both are numerically close to the answer. Unlike `atol`/`rtol`, this cannot be combined with tolerance params — `{ "sig_figs": 3, "atol": 0.01 }` will raise an error rather than be evaluated.

## Notes

**Note:** If the answer is not a number, all responses will generate an error.

**Note:** If the response is not a number, a feedback message asking the student to submit a number will be returned.

**Note:** `sig_figs` and `atol`/`rtol` are mutually exclusive; supplying both will generate an error.
