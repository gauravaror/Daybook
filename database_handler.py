import postgresql
import json

class DatabaseHandler:
    def __init__(self, creds):
        c = json.load(open(creds))
        connection_string = """pq://{user}:{password}@{host}/{db}""".format(user=c['user'],
                   password=c['password'],
                   host=c['host'],
                   db=c['db'])
        print(connection_string)
        self.db = postgresql.open(connection_string)

    def create_user(self, chat_id, timezone):
        deletesql = """delete from users where chat_id='{chat_id}'""".format(chat_id=chat_id)
        dsql = self.db.prepare(deletesql)
        dsql()

        sql = """insert into users (chat_id, timezone, created_on) values
                 ('{chat_id}', '{timezone}', current_timestamp);
               """.format(chat_id=chat_id, timezone=timezone)
        insert_user = self.db.prepare(sql)
        insert_user();

    def create_reminder(self, chat_id, reminder_name, reminder_time):
        deletesql = """delete from reminders where chat_id='{chat_id}' and reminder_name='{reminder_name}'""".format(chat_id=chat_id, 
                       reminder_name=reminder_name)
        dsql = self.db.prepare(deletesql)
        dsql()

        sql = """insert into reminders (chat_id, reminder_name, reminder_time, created_on) values
                 ('{chat_id}', '{reminder_name}', '{reminder_time}', current_timestamp);
               """.format(chat_id=chat_id, reminder_name=reminder_name, reminder_time=reminder_time)
        insert_user = self.db.prepare(sql)
        insert_user()

    def delete_reminder(self, chat_id, reminder_name):
        sql = """delete from reminders where chat_id='{chat_id}' and reminder_name='{reminder_name}'
              """.format(chat_id=chat_id, reminder_name=reminder_name)
        delete_user = self.db.prepare(sql)
        delete_user()

    def get_all_reminder(self):
        sql = """select users.chat_id as chat_id, timezone, reminder_name, reminder_time from reminders rem join users users on rem.chat_id = users.chat_id"""
        all_reminders = self.db.prepare(sql)
        return all_reminders()

    def get_all_users(self):
        sql = """select * from users"""
        all_reminders = self.db.prepare(sql)
        return all_reminders()
