import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convert import convert, ConversionError, main


def approx(a, b, tol=1e-4):
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


print("=== LENGTH ===")
assert approx(convert(10, "km", "mi"), 6.21371)
assert approx(convert(1, "mi", "km"), 1.609344)
assert approx(convert(12, "in", "cm"), 30.48)
assert approx(convert(3, "ft", "m"), 0.9144)
print("OK")

print("=== WEIGHT ===")
assert approx(convert(5, "kg", "lb"), 11.02311)
assert approx(convert(1, "lb", "oz"), 16.0)
assert approx(convert(1, "ton", "kg"), 1000.0)
print("OK")

print("=== VOLUME ===")
assert approx(convert(1, "gal", "l"), 3.785411784)
assert approx(convert(1, "cup", "tbsp"), 16.0)
print("OK")

print("=== TIME ===")
assert approx(convert(2, "hour", "min"), 120.0)
assert approx(convert(1, "day", "hour"), 24.0)
assert approx(convert(1, "week", "day"), 7.0)
print("OK")

print("=== TEMPERATURE ===")
assert approx(convert(98.6, "f", "c"), 37.0)
assert approx(convert(0, "c", "f"), 32.0)
assert approx(convert(0, "c", "k"), 273.15)
assert approx(convert(100, "c", "f"), 212.0)
assert approx(convert(-40, "f", "c"), -40.0)  # famous crossover point
print("OK")

print("=== CASE / SPACING INSENSITIVITY ===")
assert approx(convert(1, "KM", "Mi"), 0.621371)
assert approx(convert(1, " Kilometer ", "MILES"), 0.621371)
print("OK")

print("=== ERROR: mismatched categories ===")
try:
    convert(1, "km", "kg")
    assert False, "should have raised"
except ConversionError as e:
    print("OK -", e)

print("=== ERROR: unknown unit ===")
try:
    convert(1, "banana", "km")
    assert False, "should have raised"
except ConversionError as e:
    print("OK -", e)

print("=== CLI: main() end-to-end ===")
code = main(["10", "km", "mi"])
assert code == 0

code = main(["--list"])
assert code == 0

code = main(["1", "banana", "km"])
assert code == 1  # error path returns nonzero

code = main([])
assert code == 1  # no args -> help + nonzero

print("OK")

print("\nAll tests passed.")
