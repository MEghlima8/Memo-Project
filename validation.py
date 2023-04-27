import re 

# Check email is valid or not
def is_valid_email(email):
    if not email :
        return 'empty_email' # Email is empty
    
    if len(email) > 320:
        return 'email_length' # Email length is not less than 320 chars
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return 'char_email' # Email chars is not valid


# Check fullname is valid or not
def is_valid_fullname(fullname):
    if not fullname :
        return 'empty_fullname' # Fullname is empty
    
    if len(fullname) > 320:
        return 'fullname_length'  # Fullname length is not less than 320 chars
    
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ. ')
    if not set(fullname).issubset(allowed_chars):
        return 'char_fullname' # Fullname chars is not valid
    

# Check password is valid or not
def is_valid_password(password):
    if not password :
        return 'empty_password'
    
    pattern1 = re.compile(r'.{8,30}') # The password must be between 8 and 30 characters long
    pattern2 = re.compile(r'[A-Za-z]+') # The password must have english letter(s)
    pattern3 = re.compile(r'\d+') # The password must have number(s)
    pattern4 = re.compile(r'[!@#$%^&*()<>?/\|}{~:]') # The password must have special character(s)
    
    if pattern1.fullmatch(password) is None:
        return 'password_length'
    elif pattern2.search(password) is None or pattern3.search(password) is None or pattern4.search(password) is None:
        return 'char_password'


# Check confirm password is valid or not
def is_valid_confirm_password(password,confirm_password):
    if password == confirm_password:
        return True

# It checks whether the email and password are valid
def signin(email, password):
    if is_valid_email(email) == 'email_length' or is_valid_email(email) == 'char_email' or is_valid_email(email) == 'empty_email':
        return is_valid_email(email)
    
    if is_valid_password(password) == 'password_length' or is_valid_password(password) == 'char_password' or is_valid_password(password) == 'empty_password':
        return is_valid_password(password)
    return True


# It checks whether the signup info are valid
def signup(fullname, email, password,confirm_password):
    
    if is_valid_fullname(fullname) == 'fullname_length' or is_valid_fullname(fullname) == 'char_fullname' or is_valid_fullname(fullname) == 'empty_fullname':
        return is_valid_fullname(fullname)
    
    if is_valid_email(email) == 'email_length' or is_valid_email(email) == 'char_email' or is_valid_email(email) == 'empty_email':
        return is_valid_email(email)
    
    if is_valid_password(password) == 'password_length' or is_valid_password(password) == 'char_password' or is_valid_password(password) == 'empty_password':
        return is_valid_password(password)
    
    if not is_valid_confirm_password(password,confirm_password):
        return 'no_match_passwords'
    
    return True