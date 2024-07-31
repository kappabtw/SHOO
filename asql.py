# -*- coding: windows-1251 -*-
import aiosqlite  

class ASQL:
    
    database_name = "shoo.db"
    database = None
    cursor = None

    @classmethod
    async def connect(cls)->None:
        """Connects to the database"""
        if cls.database is None:
            cls.database = await aiosqlite.connect(cls.database_name)
            cls.cursor = await cls.database.cursor()
        
    @classmethod
    async def close(cls)->None:
        """Closes the connection to the database"""
        await cls.database.close()
    @classmethod
    async def execute(cls, command, *args)->None:
        """Выполняет SQL-команды c фиксацикй изменений в базе данных"""
        if cls.cursor is None:
            raise RuntimeError("Соединение с базой данных не установлено")
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        await cls.cursor.execute(command, args)
        result = await cls.cursor.fetchall()
        await cls.database.commit()
        return result
            
    @classmethod
    async def commit(cls)->None:
       """Commits changes to the database"""
       await cls.database.commit()
       