from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_add_task(self):
        sql = """
        CREATE TABLE IF NOT EXISTS add_task (
        id SERIAL PRIMARY KEY,
        task_title VARCHAR(355) NULL unique,
        priority VARCHAR(100) NULL,
        completed BOOLEAN NULL,
        time VARCHAR(150) NULL,
        from_who VARCHAR(255) NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)
    
    async def add_task(self, task_title, priority, completed, time, from_who):
        sql = "INSERT INTO add_task (task_title, priority, completed, time, from_who) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, task_title, priority, completed, time, from_who, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_tasks(self, from_who):
        sql = "SELECT * FROM add_task WHERE from_who=$1"
        return await self.execute(sql, from_who, fetch=True)
    
    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)
    
    async def update_task_complete(self, task_completed, id):
        sql = "UPDATE add_task SET completed=$1 WHERE id=$2"
        return await self.execute(sql, task_completed, id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_task(self, task_id):
        sql = "DELETE FROM add_task WHERE id=$1"
        return await self.execute(sql, task_id, execute=True)
    
    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def drop_tasks(self):
        await self.execute("DROP TABLE add_task", execute=True)
