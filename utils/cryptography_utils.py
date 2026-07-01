import bcrypt


class CryptographyUtils:
    @staticmethod
    def hash_string(string: str) -> str:
        string_bytes = string.encode('utf-8')
        hashed_string = bcrypt.hashpw(string_bytes, bcrypt.gensalt())
        return hashed_string.decode('utf-8')

    @staticmethod
    def verify_string(string: str, hashed_string: str) -> bool:
        string_bytes = string.encode('utf-8')
        hashed_string_bytes = hashed_string.encode('utf-8')
        return bcrypt.checkpw(string_bytes, hashed_string_bytes)
