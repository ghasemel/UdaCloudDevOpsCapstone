from configparser import ConfigParser


class Config(object):
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self, filename='database.ini', section='db-prod'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))        

        hostname = db["host"]
        database = db["database"]
        user = db["user"]
        password = db["password"]
        port = db["port"]

        # postgres://{user}:{password}@{hostname}:{port}/{database-name}
        self.SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{hostname}:{port}/{database}"
