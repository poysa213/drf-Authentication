import random
import string
    
def get_otp():
    generate_pass = ''.join([random.choice( string.ascii_uppercase +
                                            string.ascii_lowercase +
                                            string.digits)
                                            for n in range(8)])
                            
    return generate_pass
    
