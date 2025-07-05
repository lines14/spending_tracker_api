import os

class Logger:
    @staticmethod
    def log(stack: list) -> None:
        log_path = os.path.join(os.path.dirname(__file__), "../error_logs.txt")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as file:
            file.writelines(stack)