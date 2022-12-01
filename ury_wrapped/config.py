import yaml
import pydantic


class Config(pydantic.BaseSettings):
    db_host: str
    db_port: int = 5432
    db_user: str
    db_password: pydantic.SecretStr


cfg: Config = Config(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore