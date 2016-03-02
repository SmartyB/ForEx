import sqlite3, json, time
# import database.db_spec as db_spec
import environment

class DataBase:
    def store_to_db(self, try_counter=0):
        if try_counter > 1:
            print('Error saving to DB - probably locked')
            return
        try:
            db_spec = environment.env.get_db_spec()
            db_path = db_spec.db_path
            spec    = db_spec.spec

            object_class = self.__class__.__name__
            if object_class not in spec.keys():
                raise DbErrorNotInSpec

            spec = spec[self.__class__.__name__]

            db = sqlite3.connect(db_path)
            c = db.cursor()

            # check if row exists
            c.execute(
                "SELECT * FROM `{0}` WHERE `{1}` = {2}".format(
                    spec['table'],
                    spec['primary_key'],
                    self.__dict__[spec['primary_key']]
                    ))

            # if it doesn't exist create
            if len(c.fetchall()) == 0:
                c.execute("INSERT INTO `{0}`({1}) VALUES ({2})".format(
                    spec['table'],
                    spec['primary_key'],
                    self.__dict__[spec['primary_key']]
                ))

            value_set = False

            # set values
            q = "UPDATE `{0}` SET ".format(spec['table'])
            object_fields = self.__dict__.keys()
            for field in spec['fields']:
                if not field in object_fields:
                    continue
                if not self.__dict__[field]:
                    continue
                value_set = True
                q += "`{0}` = '{1}', ".format(field, self.__dict__[field])

            if not value_set: return

            q = q[:-2] + " WHERE `{0}` = '{1}'".format(spec['primary_key'], self.__dict__[spec['primary_key']])

            c.execute(q)
            db.commit()
        except sqlite3.OperationalError:
            time.sleep(5)
            self.store_to_db(try_counter=try_counter+1)

    def load_from_db(self):
        db_spec = environment.env.get_db_spec()
        db_path = db_spec.db_path
        spec    = db_spec.spec

        object_class = self.__class__.__name__
        if object_class not in spec.keys():
            raise DbErrorNotInSpec

        db = sqlite3.connect(db_path)
        c = db.cursor()

        spec = spec[self.__class__.__name__]
        table           = spec['table']
        primary_key     = spec['primary_key']
        primary_value   = self.__dict__[spec['primary_key']]

        c.execute("SELECT * FROM `{0}` WHERE `{1}` = '{2}'".format(table, primary_key, primary_value))
        columns = list(map(lambda x: x[0], c.description))
        rows = c.fetchall()
        if not len(rows) == 1:
            return
        row = rows[0]

        for field in spec['fields']:
            if not field in columns:
                continue
            column_id = columns.index(field)
            value = row[column_id]
            if value == 'None':
                value = None
            self.__dict__[field] = value

    def exists_in_db(self, table, primary_key, primary_value):
        db_spec = environment.env.get_db_spec()
        db_path = db_spec.db_path
        db = sqlite3.connect(db_path)
        c = db.cursor()
        c.execute("SELECT * FROM `{0}` WHERE `{1}` = '{2}'".format(table, primary_key, primary_value))
        return len(c.fetchall()) == 1

    def get_from_db(self, table, primary_key, primary_value):
        db_spec = environment.env.get_db_spec()
        db_path = db_spec.db_path
        db = sqlite3.connect(db_path)
        c = db.cursor()
        c.execute("SELECT * FROM `{0}` WHERE `{1}` = '{2}'".format(table, primary_key, primary_value))
        columns = list(map(lambda x: x[0], c.description))
        rows = c.fetchall()
        if len(rows) == 1:
            ob = {}
            for i in range(len(columns)):
                ob[columns[i]] = rows[0][i]
            return ob
        return False

class DbErrorNotInSpec(Exception):
    pass
