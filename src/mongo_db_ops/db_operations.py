import os
import pymongo
import hashlib
from src.loggings import add_logger
class mongo_db_atlas_ops:
    def __init__(self):
        self.log=add_logger()
    def get_mongo_db_connection(self):
        '''Responsible for the connection with MongoDB Atlas'''
        try:
            user=os.environ.get('MONGO_USER')
            mongo_password=os.environ.get('MONGO_PASSWORD')
            con=pymongo.MongoClient(f"mongodb+srv://{user}:{mongo_password}@cluster0.hpbfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            self.log.log(f'Sucessfully connected to the mongodb database','db_operations.log',1)
            return con
        except Exception as e:
            self.log.log(f'Couldnot connected to the mongodb database error, {str(e)}','db_operations.log',3)
    def find_in_database(self,table_name,email,password)->bool:
        try:
            email_validation=table_name['login_credentials'].find({'email':str(email)})
            password_validation=table_name['login_credentials'].find({'password':password})
            if email_validation.count()>0:
                for item in email_validation:
                    email_id=item.get('_id')
                email_validation_flag= True
            else:
                email_validation_flag= False
            password_validation_flag=False
            if email_validation_flag:
                if password_validation.count()>0:
                    for item in password_validation:
                        pass_id=item.get('_id')
                        if email_id==pass_id:
                            password_validation_flag= True
                            break
                        else:
                            password_validation_flag= False
                            
            else:
                password_validation_flag= False
            self.log=add_logger()
            self.log.log(f'Email: {str(email)} validation flag, email_validation_flag: {str(email_validation_flag)},password_validation_flag: {str(password_validation_flag)}','db_operations.log',1)
            return email_validation_flag, password_validation_flag
        except Exception as e:
            self.log.log(f'Email: {str(email)} validation flag, email_validation_flag: {str(email_validation_flag)},password_validation_flag: {str(password_validation_flag)}; error: {str(e)}','db_operations.log',3)
            
    def insert_signup_credentials(self,fname,lname,email,password,city,state,zip):
        try:
            client=self.get_mongo_db_connection()
            login_credentials=client['Human_and_Plant_Health_SDM']
            table=login_credentials['login_credentials']
            result = hashlib.sha256(password.encode())
            table.insert_one({'fname':str(fname),'lname':str(lname),'email':str(email),'password':str(result.hexdigest()),'city':str(city),'state':str(state),'zip':str(zip)})
            self.log=add_logger()
            self.log.log(f'sign_up credentials for email: {str(email)} sucessfully inserted into database','db_operations.log',1)
        except Exception as e:
            self.log.log(f'sign_up credentials for email: {str(email)} couldnot inserted into database error, {str(e)}','db_operations.log',3)
    def update_password(self,email,password):
        try:
            client=self.get_mongo_db_connection()
            login_credentials=client['Human_and_Plant_Health_SDM']
            table=login_credentials['login_credentials']
            email_validation=login_credentials['login_credentials'].find({'email':str(email)})
            self.log=add_logger()
            self.log.log(f'sign_up credentials sucessfully inserted into database','db_operations.log',1)
            for password_ in email_validation:
                old_password=password_['password']
            myquery = { "password": old_password }
            Result = hashlib.sha256(password.encode())
            newvalues = { "$set": { "password": Result.hexdigest() } }
            table.update_one(myquery, newvalues)
            self.log.log(f'password for email: {str(email)} sucessfully updated in the database','db_operations.log',1)
        except Exception as e:
            self.log.log(f'password for email: {str(email)} could not updated in the database error, {str(e)}','db_operations.log',3)
            
            