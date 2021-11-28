from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
from src.loggings import add_logger
class cassandra_ops:
    def __init__(self):
        pass
    def connect_to_cassandra_db(self,keyspace):
        log=add_logger()
        try:
            cloud_config= {
                    'secure_connect_bundle': 'secure-connect-health-app.zip'
            }
            CASSANDRA_USERNAME=os.environ.get('CASSANDRA_USERNAME')
            CASSANDRA_Password=os.environ.get('CASSANDRA_Password')
            auth_provider = PlainTextAuthProvider(CASSANDRA_USERNAME,CASSANDRA_Password )
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect(keyspace)

            row = session.execute("select release_version from system.local").one()
            log.log(f'Sucessfully connected to the cassandra database with keyspace %s' % keyspace,'cassandra_db.log',1)
        except Exception as e:
            log.log(f'Error occured while connecting to cassandra database error: {str(e)}','cassandra_db.log',3)
            
        if row:
            log.log(f'Sucessfully created and return the session of cassandra database with keyspace %s' % keyspace,'cassandra_db.log',1)
            return session
        else:
            log.log(f'Error occured while creating and returning the session of cassandra database with keyspace %s' % keyspace,'cassandra_db.log',3)
    def dump_logging_files_into_cassandra_db(self,keyspace='project_loggings'):
        log=add_logger()
        try:
            session=self.connect_to_cassandra_db(keyspace=keyspace)
            files=os.listdir('Project_Logs')
            for file in files:
                if '.log' in file:
                    table_name=file.split('.')[0]
                    print('file',file)
                    print('table_name',table_name)
                    session.execute(f"CREATE TABLE if not exists {table_name}(date text PRIMARY KEY,status text,logging_info text);")
                    file_path = f'Project_Logs/{file}'
                    f = open(file_path, 'r')
                    Lines = f.readlines()
                    for line in Lines:
                        data=line.strip().split('\t')
                        if "'" in str(data[2]):
                            data[2] = str(data[2].replace("'", '"'))
                        session.execute(f"""INSERT INTO {table_name}("date", "status", "logging_info") VALUES('{data[0]}','{data[1]}','{data[2]}');""")
                        print(f"""INSERT INTO {table_name}("date", "status", "logging_info") VALUES('{data[0]}','{data[1]}','{data[2]}');""")
                    try:
                        os.remove(file_path)
                        log.log(f'Sucessfully remove the file {str(file)} from path {str(file_path)}','cassandra_db.log',1)
                    except Exception as e:
                        log.log(f'Could occured remove the file {str(file)} from path {str(file_path)} error: {str(e)}','cassandra_db.log',3)        
            log.log(f'Sucessfully dump loggings file into cassandra database with keyspace %s'%keyspace,'cassandra_db.log',1)
        except Exception as e:
            log.log(f'Error occured while dumping the loggings file into cassandra database with keyspace %s error: %s'%keyspace %str(e),'cassandra_db.log',3)
