import sqlite3

class TokenDBSystem:
    def __init__(self, db_name="tokens.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    # Создание таблицы для хранения токенов студентов
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                tokens INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    # Добавить нового студента
    def add_student(self, student_id):
        self.cursor.execute('INSERT OR IGNORE INTO students (student_id) VALUES (?)', (student_id,))
        self.conn.commit()

    # Начислить токены студенту
    def reward_student(self, student_id, tokens):
        self.cursor.execute('UPDATE students SET tokens = tokens + ? WHERE student_id = ?', (tokens, student_id))
        self.conn.commit()

    # Использовать токены студентом
    def use_tokens(self, student_id, tokens):
        self.cursor.execute('SELECT tokens FROM students WHERE student_id = ?', (student_id,))
        balance = self.cursor.fetchone()
        
        if balance and balance[0] >= tokens:
            self.cursor.execute('UPDATE students SET tokens = tokens - ? WHERE student_id = ?', (tokens, student_id))
            self.conn.commit()
            print(f"Студент {student_id} использовал {tokens} токенов. Осталось токенов: {balance[0] - tokens}")
        else:
            print(f"Недостаточно токенов у студента {student_id}")

    # Получить количество токенов у студента
    def get_balance(self, student_id):
        self.cursor.execute('SELECT tokens FROM students WHERE student_id = ?', (student_id,))
        balance = self.cursor.fetchone()
        return balance[0] if balance else 0

    # Закрыть соединение с базой данных
    def close(self):
        self.conn.close()
