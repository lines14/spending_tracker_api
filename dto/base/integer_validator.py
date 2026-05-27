class IntegerValidator:
    def __init__(self, value: int):
        self.value = value
    
    def is_in_range(self, min_value : int, max_value: int) -> bool:
        return min_value <= self.value <= max_value