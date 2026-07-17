# IsSimilar

Use this evaluation function to check if a student's response is within a tolerance range of the correct answer. Works like the [numpy.isclose](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html#numpy.isclose) function.

A response is accepted if:

```
|response - answer| ≤ absolute_tolerance + relative_tolerance × |answer|
```

The left-hand side is the absolute difference between the student's response and the correct answer. The right-hand side is the total allowed difference, made up of a fixed part (`absolute_tolerance`) and a part that scales with the size of the answer (`relative_tolerance × |answer|`). A response is marked correct whenever the actual difference does not exceed the allowed difference.

## Parameters

Both parameters default to `0` (exact match required) and can be used individually or together.

### `absolute_tolerance` — Absolute tolerance

Specifies a fixed margin around the answer, regardless of its magnitude. Use this when you know the acceptable error in the same units as the answer.

### `relative_tolerance` — Relative tolerance

Specifies an acceptable error as a fraction of the answer's magnitude. Use this when the answer is very large or very small and a percentage-based margin makes more sense than a fixed one.

## Examples

### Exact match (default)

No params needed. The student must enter exactly `42` (floating-point precision is handled automatically).

### Absolute tolerance

```json
{ "absolute_tolerance": 0.05 }
```

With answer `9.81`, accepts any response in the range **9.76 – 9.86**. Good for physical measurements where the acceptable error is known in the same units.

### Relative tolerance

```json
{ "relative_tolerance": 0.01 }
```

With answer `6.674e-11`, accepts any response within **1%** of the answer. Good for very large or very small values where a fixed margin would be impractical.

### Combined tolerances

```json
{ "absolute_tolerance": 0.01, "relative_tolerance": 0.005 }
```

Both tolerances contribute: with answer `9.81`, the allowed difference is `0.01 + 0.005 × 9.81 ≈ 0.059`. Useful when you want a minimum floor (`absolute_tolerance`) plus a proportional allowance (`relative_tolerance`).

## Notes

**Note:** If the answer is not a number, all responses will generate an error.

**Note:** If the response is not a number, a feedback message asking the student to submit a number will be returned.
