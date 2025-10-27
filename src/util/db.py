import mysql.connector

class DBManager:
    def __init__(self, host='localhost', user='root', password='', database='cleanitup'):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
            
        except mysql.connector.Error as e:
            raise RuntimeError(f"Error al conectar con MySQL: {e}")

    def insert_score(self, player_name, score):
        try:
            sql = "INSERT INTO scores (player_name, score) VALUES (%s, %s)"
            self.cursor.execute(sql, (player_name, score))
            self.conn.commit()

        except mysql.connector.Error as e:
            raise RuntimeError(f"Error al guardar puntaje: {e}")

    def get_top_scores(self, limit=10):
        self.cursor.execute("SELECT player_name, score, date_played FROM scores ORDER BY score DESC LIMIT %s", (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
