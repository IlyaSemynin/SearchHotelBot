from sqlitedict import SqliteDict


class History:
    count = -1

    def __init__(self, db_file, user_id):
        self.db = SqliteDict(db_file)
        self.user_id = user_id
        History.count += 1

    def fill(self, user_id, command, date, hotels):
        """Заполнение БД"""
        self.db[self.count] = {
            "user_id": user_id,
            "command": command,
            "date": date,
            "hotels": hotels,
        }
        self.db.commit()

    def get_count(self):
        """Получение счетчика обращений"""
        return self.count

    def get_current_history(self):
        """Получение БД по последнему обращению"""
        return self.db[self.count]

    def get_history_target(self, cnt):
        """Получение БД по конкретному обращению"""
        return self.db[cnt]

    def get_user_id(self, key):
        """Получение последнего user_id"""
        return self.db[key]["user_id"]

    def get_command(self, key):
        """Получение последнего command"""
        return self.db[key]["command"]

    def get_date(self, key):
        """Получение последнего date"""
        return self.db[key]["date"]

    def get_hotels(self, key):
        """Получение последнего списка отелей"""
        return self.db[key]["hotels"]

    def close(self):
        self.db.close()
