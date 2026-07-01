from decimal import ROUND_DOWN, Decimal


class FloatValidator:
    def __init__(self, value: float):
        self.value = value

    def is_in_range(self, min_value : float, max_value: float) -> bool:
        return min_value <= self.value <= max_value

    def has_two_decimal_places(self) -> bool:
        decimal_value = Decimal(str(self.value))
        quantized_value = decimal_value.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        return decimal_value == quantized_value
