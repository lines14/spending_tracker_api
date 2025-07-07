import os
import asyncio
import traceback
from typing import Dict
from config import Config
from alembic import context
from logging.config import fileConfig
from sqlalchemy.engine import reflection
from sqlalchemy import engine_from_config, pool, text
from alembic.runtime.migration import MigrationContext
from repositories.base.redis_client import RedisClient

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

config = context.config
current_dir = os.path.dirname(os.path.abspath(__file__))
migrations_dir = os.path.join(current_dir, '../migrations')
config.set_main_option('sqlalchemy.url', Config().DB_URL_SYNC)

# Interpret the config file for Python logging.
# This line sets up loggers basically.

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support

from models import *
from utils.logger import Logger
from database.base.database import Database

target_metadata = Database.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def has_table(engine, table_name):
    inspector = reflection.Inspector.from_engine(engine)
    tables = inspector.get_table_names()

    return table_name in tables

def filter_migrations(migrations: Dict[str, any], version: tuple) -> Dict[str, any]:
    sorted_keys = sorted(migrations.keys())

    if len(version) != 0:
        filtered_keys = [key for key in sorted_keys if key <= version[0]]
    else:
        filtered_keys = [sorted_keys[0]]

    filtered_dict = {key: migrations[key] for key in filtered_keys}

    return filtered_dict

def get_migrations(dirname):
    migrations = {}

    for filename in os.listdir(dirname):
        if filename.endswith('.py'):
            delimiter = '_'
            first_delimiter_index = filename.find(delimiter)
            second_delimiter_index = filename.find(delimiter, first_delimiter_index + 1)
            first_part = filename[:second_delimiter_index]
            second_part = filename[second_delimiter_index + 1:]
            parts = [first_part] + second_part.split(delimiter, 3)

            if len(parts) >= 5:
                version = '_'.join(parts[:4])
                name = '_'.join(parts[4:]).strip('.py')
            else:
                continue

            name = name.replace('_', ' ').strip()
            migrations[version] = name

    return migrations

def log_migrations(connection, version, migrations):
    truncated_migrations = filter_migrations(migrations, version)

    if has_table(connection.engine, 'migrations'):
        for key, value in truncated_migrations.items():
            try:
                sql = text(
                    "INSERT INTO migrations (version, name) VALUES (:version, :name) "
                    "ON DUPLICATE KEY UPDATE name = :name;"
                )
                
                connection.execute(sql, {"version": key, "name": value})
                connection.commit()
            except Exception as e:
                Logger.log('\n' + '-' * 100 + '\n')
                Logger.log(traceback.format_exc())

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def clear_cache():
    redis_client = RedisClient()
    await redis_client.clear_cache()
    await redis_client.close()
    await redis_client.disconnect()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        asyncio.run(clear_cache())

        with context.begin_transaction():
            context.run_migrations()
            mc = MigrationContext.configure(connection)
            version = mc.get_current_heads()
            migrations = get_migrations(migrations_dir)
            log_migrations(connection, version, migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()