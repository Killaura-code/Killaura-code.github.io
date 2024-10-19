import aiosqlite

async def setup_db():
    async with aiosqlite.connect('bot_database.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            )
        ''')
        await db.commit()

async def add_user(user_id, username, first_name, last_name):
    async with aiosqlite.connect('bot_database.db') as db:
        await db.execute('''
            INSERT OR IGNORE INTO users (id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect('bot_database.db') as db:
        async with db.execute('SELECT * FROM users WHERE id = ?', (user_id,)) as cursor:
            user = await cursor.fetchone()
            return user
