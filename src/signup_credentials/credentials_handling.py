from src.mongo_db_ops.db_operations import mongo_db_atlas_ops
class sign_up_credentials:
    def __init__(self):
        self.mongo_conn=mongo_db_atlas_ops()
    def credentials_validations(self,email,password):
        '''See whether email and password is already regestered or not'''
        client=self.mongo_conn.get_mongo_db_connection()
        login_credentials=client['Human_and_Plant_Health_SDM']
        email_validation_flag, password_validation_flag=self.mongo_conn.find_in_database(login_credentials,str(email),str(password))
        return email_validation_flag, password_validation_flag
    def dump_credentials_to_mongo_atlas(self,fname,lname,email,password,city,state,zip):
        email_validation_flag, _=self.credentials_validations(email,password)
        if not email_validation_flag:
            return self.mongo_conn.insert_signup_credentials(fname,lname,email,password,city,state,zip)
        return "<h1>Your Email is already registered with us if you forget your password then please click to the foget password.</h1>"
        
        