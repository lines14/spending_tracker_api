class BaseCustomError(Exception):
    def __init__(self, error_config: list):
        self.message = error_config[0]
        self.data = error_config[1] if len(error_config) > 1 else None
        self.status_code = error_config[2] if len(error_config) > 2 else None

        super().__init__(self.message)
