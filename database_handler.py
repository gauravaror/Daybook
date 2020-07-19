import json
import mariadb


class DatabaseHandler:
    def __init__(self, creds):
        c = json.load(open(creds))
        try:
            conn = mariadb.connect(
                user=c['user'],
                password=c['password'],
                host=c['host'],
                port=3306,
                database=c['db']
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        self.db = conn.cursor()


    def create_user(self, chat_id, timezone):
        deletesql = """delete from users where chat_id='{chat_id}'""".format(chat_id=chat_id)
        self.db.execute(deletesql)

        sql = """insert into users (chat_id, timezone, created_on) values
                 ('{chat_id}', '{timezone}', current_timestamp);
               """.format(chat_id=chat_id, timezone=timezone)
        self.db.execute(sql)

    def create_reminder(self, chat_id, reminder_name, reminder_time):
        deletesql = """delete from reminders where chat_id='{chat_id}' and reminder_name='{reminder_name}'""".format(chat_id=chat_id, 
                       reminder_name=reminder_name)
        self.db.execute(deletesql)

        sql = """insert into reminders (chat_id, reminder_name, reminder_time, created_on) values
                 ('{chat_id}', '{reminder_name}', '{reminder_time}', current_timestamp);
               """.format(chat_id=chat_id, reminder_name=reminder_name, reminder_time=reminder_time)
        self.db.execute(sql)

    def delete_reminder(self, chat_id, reminder_name):
        sql = """delete from reminders where chat_id='{chat_id}' and reminder_name='{reminder_name}'
              """.format(chat_id=chat_id, reminder_name=reminder_name)
        self.db.execute(sql)

    def get_all_reminder(self):
        sql = """select users.chat_id as chat_id, timezone, reminder_name, reminder_time from reminders rem join users users on rem.chat_id = users.chat_id"""
        self.db.execute(sql)
        return list(self.db)

    def get_all_users(self):
        sql = """select * from users"""
        self.db.execute(sql)
        return list(self.db)
