import hashlib
import hmac

import bcrypt

from utils.storage_utils import StorageUtils


class CryptographyUtils:
    @classmethod
    def generate_fingerprint(cls, token: str) -> str:
        return hmac.new(StorageUtils.private_key.encode("utf-8"), token.encode("utf-8"), hashlib.sha256).hexdigest()

    @classmethod
    def verify_fingerprint(cls, token: str, fingerprint: str) -> bool:
        expected_fingerprint = cls.generate_fingerprint(token)
        return hmac.compare_digest(expected_fingerprint, fingerprint)

    @staticmethod
    def hash_password(string: str) -> str:
        string_bytes = string.encode("utf-8")
        hashed_string = bcrypt.hashpw(string_bytes, bcrypt.gensalt())
        return hashed_string.decode("utf-8")

    @staticmethod
    def verify_password(string: str, hashed_string: str) -> bool:
        string_bytes = string.encode("utf-8")
        hashed_string_bytes = hashed_string.encode("utf-8")
        return bcrypt.checkpw(string_bytes, hashed_string_bytes)
