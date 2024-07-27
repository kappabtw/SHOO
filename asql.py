import aiosqlite  

class ASQL:
    
    database_name = "shoo.db"
    database = None
    cursor = None

    @classmethod
    async def connect(cls)->None:
        """Connects to the database"""
        cls.database = await aiosqlite.connect(cls.database_name)
        cls.cursor = await cls.database.cursor()
        
    @classmethod
    async def close(cls)->None:
        """Closes the connection to the database"""
        await cls.database.close()
    @classmethod
    async def execute(cls, command, *args)->None:
        """Executes SQL commands without commiting changes to the database"""
        async with aiosqlite.connect(cls.database_name) as connection:
            cursor = await connection.cursor()
            if len(args) == 1 and isinstance(args[0], (list, tuple)):
                args = args[0]
            await cursor.execute(command, args)
            result = await cursor.fetchall()
            await connection.commit()
            return result
            
    @classmethod
    async def commit(cls)->None:
       """Commits changes to the database"""
       await cls.database.commit()
       
async def load_image():
    pass