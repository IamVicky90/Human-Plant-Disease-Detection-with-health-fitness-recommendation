from src.mongo_db_ops.db_operations import mongo_db_atlas_ops
from src.loggings import add_logger
class sign_up_credentials:
    def __init__(self):
        self.mongo_conn=mongo_db_atlas_ops()
    def credentials_validations(self,email,password):
        '''See whether email and password is already regestered or not'''
        try:
            log=add_logger()
            client=self.mongo_conn.get_mongo_db_connection()
            login_credentials=client['Human_and_Plant_Health_SDM']
            email_validation_flag, password_validation_flag=self.mongo_conn.find_in_database(login_credentials,str(email),str(password))
            log.log(f'credentials_validations funtion run sucessfully and the email_validation_flag: {email_validation_flag} and password_validation_flag: {password_validation_flag} for email {str(email)}','credentials_handling.log',1)
            return email_validation_flag, password_validation_flag
        except Exception as e:
            log.log(f'credentials_validations could not run sucessfully for email {str(email)}, error, {str(e)}','credentials_handling.log',3)
            
    def dump_credentials_to_mongo_atlas(self,fname,lname,email,password,city,state,zip):
        log=add_logger()
        try:
            email_validation_flag, _=self.credentials_validations(email,password)
            if not email_validation_flag:
                log.log(f'dump_credentials_to_mongo_atlas funtion run sucessfully and email {str(email)} is sucessfully registered with us at signup form','credentials_handling.log',1)
                return self.mongo_conn.insert_signup_credentials(fname,lname,email,password,city,state,zip)
            log.log(f'dump_credentials_to_mongo_atlas funtion run sucessfully and email {str(email)} is already registered with us at signup form','credentials_handling.log',2)
            return "<h1>OOPS! Your Email is already registered with us if you forget your password then please click to the foget password at the login page!</h1>"
        except Exception as e:
            log.log(f'dump_credentials_to_mongo_atlas could not run sucessfully for email {str(email)}, error, {str(e)}','credentials_handling.log',3)
        
        