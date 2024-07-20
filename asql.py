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
    async def execute(cls, *args)->None:
        """Executes SQL commands without commiting changes to the database"""
        for command in args:
            await cls.cursor.execute(command)
            
    @classmethod
    async def commit(cls)->None:
       """Commits changes to the database"""
       await cls.database.commit()