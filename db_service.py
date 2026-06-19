import mysql.connector
from config import DB_HOST,DB_USER,DB_PASSWORD,DB_DATABAE,DB_PORT



class DbService:

    @staticmethod
    def _connect():
        return mysql.connector.connect(
            host= DB_HOST,
            user= DB_USER,
            password= DB_PASSWORD,
            database= DB_DATABAE,
            port= DB_PORT
        )
    

    # -----------------------------
    # ACTIVITIES
    # -----------------------------
    @staticmethod
    def add_activity(category, sub_category, value):
        conn = DbService._connect()
        cursor = conn.cursor()

        query = """
        INSERT INTO activities (category, sub_category, value)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (category, sub_category, value))
        conn.commit()

        cursor.close()
        conn.close()

# -----------------------------
    # WELLBEING - INSERT
    # -----------------------------
    @staticmethod
    def add_wellbeing(mood, motivation, mindfulness, libido):
        conn = DbService._connect()
        cursor = conn.cursor()

        query = """
        INSERT INTO wellbeing_metrics (mood, motivation, mindfulness, libido)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (mood, motivation, mindfulness, libido))
        conn.commit()

        cursor.close()
        conn.close()

    # -----------------------------
    # WELLBEING - GET
    # -----------------------------
    @staticmethod
    def get_latest_wellbeing():
        conn = DbService._connect()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT *
        FROM wellbeing_metrics
        ORDER BY created_at DESC
        LIMIT 1
        """

        cursor.execute(query)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

# -----------------------------
    # DAILY MACROS - INSERT
    # -----------------------------
    @staticmethod
    def add_daily_macros(energy, protein, fat, carbohydrate, fiber, sugars, salt):
        conn = DbService._connect()
        cursor = conn.cursor()

        query = """
        INSERT INTO daily_macros (
            energy, protein, fat, carbohydrate, fiber, sugars, salt
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            energy, protein, fat, carbohydrate, fiber, sugars, salt
        ))
        conn.commit()

        cursor.close()
        conn.close()

    # -----------------------------
    # DAILY MACROS - GET LATEST
    # -----------------------------
    @staticmethod
    def get_latest_daily_macros():
        conn = DbService._connect()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT *
        FROM daily_macros
        ORDER BY created_at DESC
        LIMIT 1
        """

        cursor.execute(query)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

