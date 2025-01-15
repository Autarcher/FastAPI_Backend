from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

from pathlib import Path
import platform
from loguru import logger
import yaml

THIS_DIR = Path(__file__).parent
ENV_FILE = Path(THIS_DIR, "../../.env")
# TODO: 配置文件路径未测试
CONFIG_FILES = [
    Path("C:\\config.yml") if platform.system() == "Windows" else Path("~/.config.yml").expanduser(),
    Path(THIS_DIR, "../config.yml"),
    Path(THIS_DIR, "../config/config.yml"),
]

class Mysql(BaseModel):
    host: str = Field(default="10.13.3.184", required=True)
    port: int = Field(default=3306, required=True)
    db: str = Field(default="lya_test", required=True)
    username: str = Field(default="root", required=True)
    password: str = Field(default="123456", required=True)

    @property
    def database_url(self):
        return f"mysql+aiomysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"
    


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CHANGEME_', env_file=ENV_FILE.resolve(),
                                      env_nested_delimiter='__') # 以双下划线作为嵌套分隔符
    
    testing: bool = Field(default=False)
    mysql: Mysql = Field(default_factory=Mysql, required=True)

    @staticmethod
    def load() -> "AppSettings":
        # 依次从配置文件列表中，按优先级读取配置文件。
        # 如果未找到配置文件，则返回默认配置。
        for path in CONFIG_FILES:
            if not path.is_file():
                logger.debug(f"未发现配置文件在：`{path.resolve()}`")
                continue

            logger.info(f"读取配置文件从： `{path.resolve()}`")
            with open(path, "r", encoding='utf8') as yaml_file:
                config_data = yaml.safe_load(yaml_file)
                s = AppSettings(**config_data)
                return s
        else:
            return AppSettings()