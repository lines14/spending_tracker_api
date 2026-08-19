from pathlib import Path


class StorageUtils:
    _storage_path = Path(__file__).resolve().parent.parent / "storage" / "jwt"
    private_key: str = (_storage_path / "private.pem").read_text()
    public_key: str = (_storage_path / "public.pem").read_text()
