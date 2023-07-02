import re 
import Levenshtein

class Valid:
    
    def __init__(self, email, password, confitm_password=None ,fullname=None):
        self.email = email
        self.password = password
        self.confirm_password= confitm_password
        self.fullname = fullname
        
        
    # Check email is valid or not
    def is_valid_email(self):
        if not self.email :
            return 'empty_email' # Email is empty
        
        if len(self.email) > 320:
            return 'email_length' # Email length is not less than 320 chars
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, self.email):
            return True
        else:
            return 'char_email' # Email chars is not valid


    # Check fullname is valid or not
    def is_valid_fullname(self):
        if not self.fullname :
            return 'empty_fullname' # Fullname is empty
        
        if len(self.fullname) > 320:
            return 'fullname_length'  # Fullname length is not less than 320 chars
        
        fullname_allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ. ')
        if not set(self.fullname).issubset(fullname_allowed_chars):
            return 'char_fullname' # Fullname chars is not valid
    
    # Check password is valid or not
    def is_valid_password(self):
        if not self.password :
            return 'empty_password'
        
        pass_pattern1 = re.compile(r'.{8,30}') # The password must be between 8 and 30 characters long
        pass_pattern2 = re.compile(r'[A-Za-z]+') # The password must have english letter(s)
        pass_pattern3 = re.compile(r'\d+') # The password must have number(s)
        pass_pattern4 = re.compile(r'[!@#$%^&*()<>?/\|}{~:]') # The password must have special character(s)
        
        split_email = self.email.split('@')[0]
        sim = self.calculate_similarity(split_email , self.password)
        if sim >= 75 :
            return 'used_info_in_password'
            
        if pass_pattern1.fullmatch(self.password) is None:
            return 'password_length'
        elif pass_pattern2.search(self.password) is None or pass_pattern3.search(self.password) is None or pass_pattern4.search(self.password) is None:
            return 'char_password'


    # Check confirm password is valid or not
    def is_valid_confirm_password(self):
        if self.password == self.confirm_password:
            return True

    # It checks whether the email and password are valid
    def signin(self):
        check_valid_email = self.is_valid_email()
        if check_valid_email == 'email_length' or check_valid_email == 'char_email' or check_valid_email == 'empty_email':
            return check_valid_email
        
        check_valid_password = self.is_valid_password()
        if check_valid_password == 'password_length' or check_valid_password == 'char_password' or check_valid_password == 'empty_password' or check_valid_password == 'used_info_in_password' :
            return check_valid_password
        return True


    # It checks whether the signup info are valid
    def signup(self):    
        
        check_valid_fullname = self.is_valid_fullname()
        if check_valid_fullname == 'fullname_length' or check_valid_fullname == 'char_fullname' or check_valid_fullname == 'empty_fullname':
            return check_valid_fullname
        
        check_valid_email = self.is_valid_email()
        if check_valid_email == 'email_length' or check_valid_email == 'char_email' or check_valid_email == 'empty_email':
            return check_valid_email
        
        check_valid_password = self.is_valid_password()
        if check_valid_password == 'password_length' or check_valid_password == 'char_password' or check_valid_password == 'empty_password' or check_valid_password == 'used_info_in_password':
            return check_valid_password
        
        check_valid_confirm_password = self.is_valid_confirm_password()
        if not check_valid_confirm_password:
            return 'no_match_passwords'
        
        return True
    
    
    # Used Levenshtein distance to calculate similarity between two strings
    def calculate_similarity(self,string1, string2):
        distance = Levenshtein.distance(string1, string2)
        max_length = max(len(string1), len(string2))
        
        similarity = 1 - (distance / max_length)
        return similarity * 100
