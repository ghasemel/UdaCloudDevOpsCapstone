"""we are not using this script"""

import psycopg2
from configparser import ConfigParser
import uuid

import os
import logging

FORMAT = '%(asctime)-15s %(relativeCreated)6d %(threadName)s %(message)s'
logging.basicConfig(format=FORMAT)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class DAL:        

    def config(self, filename='database.ini', section='postgresql'):
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

        return db

    def test_connection(self):
        log.debug("test_connection(): start")
        """ Test Connection to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = self.config()

            # connect to the PostgreSQL server
            log.info('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            
            # create a cursor
            cur = conn.cursor()
            
            # execute a statement
            log.info('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            log.info(db_version)
        
            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            log.error(error)
        finally:
            if conn is not None:
                conn.close()
                log.info('Database connection closed.')


    def __connection(self):
        log.debug("connect(): start")
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = self.config()

            # connect to the PostgreSQL server
            log.info('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            log.error(error)
            raise 'error on connecting to database'
        
    def insert(self, name, description, stock, price):
        conn = self.__connection()
        try:            
            uid = str(uuid.uuid4())
            log.debug(f"goods id: {uid}")

            cursor = conn.cursor()        
            cursor.execute("""INSERT INTO goods(goods_id, name, description, stock_number, price) 
                            VALUES(%s,%s,%s,%s,%s) RETURNING goods_id;""", (uid, name, description, stock, price))
            conn.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            log.error(error)
            raise 'error on inserting to database'
        finally:
            #closing database connection.
            if conn is not None:        
                conn.close()
                print("PostgreSQL connection is closed")