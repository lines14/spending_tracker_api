import os


class Logger:
    @staticmethod
    def log(log_str: str) -> None:
        log_path = os.path.join(os.path.dirname(__file__), "../error_logs.txt")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        if os.path.exists(log_path):
            with open(log_path, encoding="utf-8") as file:
                old_content = file.read()
        else:
            old_content = ""

        with open(log_path, "w", encoding="utf-8") as file:
            file.write(log_str + old_content)
