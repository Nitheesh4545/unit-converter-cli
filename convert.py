#!/usr/bin/env python3
"""
convert.py — A command-line unit converter.

Supports length, weight/mass, temperature, volume, and time conversions.

Usage:
    python convert.py <value> <from_unit> <to_unit>
    python convert.py 10 km mi
    python convert.py 98.6 f c
    python convert.py 5 kg lb
    python convert.py --list          Show all supported units
"""

import argparse
import sys

# ---------------------------------------------------------------------------
# Conversion definitions.
# For linear categories (length, weight, volume, time), each unit stores a
# factor to convert TO the category's base unit.
# Temperature is handled specially since it's not a simple multiplication.
# ---------------------------------------------------------------------------

LENGTH = {  # base unit: meter
    "m": 1.0, "meter": 1.0, "meters": 1.0,
    "km": 1000.0, "kilometer": 1000.0,
    "cm": 0.01, "centimeter": 0.01,
    "mm": 0.001, "millimeter": 0.001,
    "mi": 1609.344, "mile": 1609.344, "miles": 1609.344,
    "yd": 0.9144, "yard": 0.9144,
    "ft": 0.3048, "foot": 0.3048, "feet": 0.3048,
    "in": 0.0254, "inch": 0.0254, "inches": 0.0254,
    "nmi": 1852.0, "nauticalmile": 1852.0,
}

WEIGHT = {  # base unit: gram
    "g": 1.0, "gram": 1.0, "grams": 1.0,
    "kg": 1000.0, "kilogram": 1000.0,
    "mg": 0.001, "milligram": 0.001,
    "lb": 453.59237, "lbs": 453.59237, "pound": 453.59237, "pounds": 453.59237,
    "oz": 28.349523125, "ounce": 28.349523125,
    "st": 6350.29318, "stone": 6350.29318,
    "ton": 1_000_000.0, "tonne": 1_000_000.0,
}

VOLUME = {  # base unit: liter
    "l": 1.0, "liter": 1.0, "liters": 1.0, "litre": 1.0,
    "ml": 0.001, "milliliter": 0.001,
    "gal": 3.785411784, "gallon": 3.785411784, "gallons": 3.785411784,
    "qt": 0.946352946, "quart": 0.946352946,
    "pt": 0.473176473, "pint": 0.473176473,
    "cup": 0.2365882365, "cups": 0.2365882365,
    "floz": 0.0295735295625, "fluidounce": 0.0295735295625,
    "tbsp": 0.01478676478125, "tablespoon": 0.01478676478125,
    "tsp": 0.00492892159375, "teaspoon": 0.00492892159375,
}

TIME = {  # base unit: second
    "s": 1.0, "sec": 1.0, "second": 1.0, "seconds": 1.0,
    "min": 60.0, "minute": 60.0, "minutes": 60.0,
    "h": 3600.0, "hr": 3600.0, "hour": 3600.0, "hours": 3600.0,
    "day": 86400.0, "days": 86400.0,
    "week": 604800.0, "weeks": 604800.0,
    "ms": 0.001, "millisecond": 0.001,
}

TEMPERATURE_UNITS = {"c", "celsius", "f", "fahrenheit", "k", "kelvin"}

CATEGORIES = {
    "length": LENGTH,
    "weight": WEIGHT,
    "volume": VOLUME,
    "time": TIME,
}


class ConversionError(Exception):
    """Raised when a conversion request can't be fulfilled."""


def normalize(unit: str) -> str:
    return unit.strip().lower().replace(" ", "").replace("_", "")


def find_category(unit: str):
    """Return the category dict a unit belongs to, or 'temperature', or None."""
    norm = normalize(unit)
    if norm in TEMPERATURE_UNITS:
        return "temperature"
    for name, table in CATEGORIES.items():
        if norm in table:
            return name
    return None


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    f = normalize(from_unit)
    t = normalize(to_unit)

    # Convert source to Celsius first
    if f in ("c", "celsius"):
        celsius = value
    elif f in ("f", "fahrenheit"):
        celsius = (value - 32) * 5 / 9
    elif f in ("k", "kelvin"):
        celsius = value - 273.15
    else:
        raise ConversionError(f'Unknown temperature unit "{from_unit}"')

    # Convert Celsius to target
    if t in ("c", "celsius"):
        return celsius
    elif t in ("f", "fahrenheit"):
        return celsius * 9 / 5 + 32
    elif t in ("k", "kelvin"):
        return celsius + 273.15
    else:
        raise ConversionError(f'Unknown temperature unit "{to_unit}"')


def convert(value: float, from_unit: str, to_unit: str) -> float:
    from_cat = find_category(from_unit)
    to_cat = find_category(to_unit)

    if from_cat is None:
        raise ConversionError(f'Unknown unit "{from_unit}". Use --list to see supported units.')
    if to_cat is None:
        raise ConversionError(f'Unknown unit "{to_unit}". Use --list to see supported units.')
    if from_cat != to_cat:
        raise ConversionError(
            f'Cannot convert between "{from_unit}" ({from_cat}) and "{to_unit}" ({to_cat}) '
            f"— they're different unit categories."
        )

    if from_cat == "temperature":
        return convert_temperature(value, from_unit, to_unit)

    table = CATEGORIES[from_cat]
    base_value = value * table[normalize(from_unit)]
    return base_value / table[normalize(to_unit)]


def list_units() -> str:
    lines = ["Supported unit categories:\n"]
    for cat_name, table in CATEGORIES.items():
        # show only the "canonical" short units to keep the list readable
        units = sorted(set(table.keys()))
        lines.append(f"  {cat_name.capitalize()}: {', '.join(units)}")
    lines.append(f"  Temperature: {', '.join(sorted(TEMPERATURE_UNITS))}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="convert",
        description="Convert values between units of length, weight, volume, time, and temperature.",
    )
    parser.add_argument("value", nargs="?", type=float, help="Numeric value to convert")
    parser.add_argument("from_unit", nargs="?", help="Unit to convert from, e.g. km")
    parser.add_argument("to_unit", nargs="?", help="Unit to convert to, e.g. mi")
    parser.add_argument("--list", action="store_true", help="List all supported units and exit")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list:
        print(list_units())
        return 0

    if args.value is None or args.from_unit is None or args.to_unit is None:
        parser.print_help()
        return 1

    try:
        result = convert(args.value, args.from_unit, args.to_unit)
    except ConversionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Trim trailing zeros for cleaner output, but keep reasonable precision
    formatted = f"{result:.6f}".rstrip("0").rstrip(".")
    print(f"{args.value:g} {args.from_unit} = {formatted} {args.to_unit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
