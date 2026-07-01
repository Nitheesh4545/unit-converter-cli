# Unit Converter (CLI)

A command-line tool for converting values between units of length, weight,
volume, time, and temperature. Pure Python — no dependencies.

## Usage

```bash
python convert.py <value> <from_unit> <to_unit>
```

### Examples

```bash
python convert.py 10 km mi
# 10 km = 6.213712 mi

python convert.py 98.6 f c
# 98.6 f = 37 c

python convert.py 5 kg lb
# 5 kg = 11.02311 lb

python convert.py 2 hour min
# 2 hour = 120 min

python convert.py --list
# Lists every supported unit, grouped by category
```

## Supported categories

| Category | Example units |
|---|---|
| Length | m, km, cm, mm, mi, yd, ft, in, nmi |
| Weight | g, kg, mg, lb, oz, st, ton |
| Volume | l, ml, gal, qt, pt, cup, floz, tbsp, tsp |
| Time | s, min, h, day, week, ms |
| Temperature | c, f, k |

Unit names are case-insensitive and accept both abbreviations and full words
(`km` or `kilometer`, `lb` or `pound`, etc.). Run `python convert.py --list`
for the full list.

## Error handling

- Converting between incompatible categories (e.g. km → kg) gives a clear error.
- Unknown units give a clear error and point you to `--list`.
- Running with no arguments shows usage help.

## Tests

```bash
python test_convert.py
```

Covers all five categories, case/spacing insensitivity, mismatched-category
errors, unknown-unit errors, and the CLI entry point end-to-end.

## Possible extensions

- Add an interactive REPL mode
- Add data/currency units (needs a live exchange rate source)
- Add a `--precision N` flag to control decimal places
- Batch conversion from a CSV file
