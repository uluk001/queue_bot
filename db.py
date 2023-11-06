class DatabaseHandler:
    def __init__(self, worker):
        self.cursor = worker
    
    def setup(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY,
            date TEXT, 
            start_time TEXT, 
            end_time TEXT, 
            address TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            event REFERENCES appointments(id),
            full_name TEXT,
            user_id INTEGER,
            queue_number INTEGER
        )
        """)
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY,
            user_id INTEGER
        )""")
    

    def add_appointment(self, date, start_time, end_time, address):
        self.cursor.execute('INSERT INTO appointments VALUES (NULL, ?, ?, ?, ?)', (date, start_time, end_time, address))
        self.conn.commit()

    def add_student(self, event, full_name, user_id, queue_number):
        self.cursor.execute('INSERT INTO students VALUES (NULL, ?, ?, ?, ?)', (event, full_name, user_id, queue_number))


    def add_admin(self, user_id):
        self.cursor.execute('INSERT INTO admins VALUES (NULL, ?)', (user_id,))
        self.conn.commit()

    def get_appointments(self):
        return self.cursor.execute("SELECT * FROM appointments")

    def get_students(self, event):
        self.cursor.execute('SELECT * FROM students WHERE event = ?', (event,))
        return self.cursor.fetchall()

    def get_admins(self):
        self.cursor.execute('SELECT * FROM admins')
        return self.cursor.fetchall()
