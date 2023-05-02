import random
import string

def get_random_string(length = 10):
    # choose from all lowercase letter
    letters = string.ascii_uppercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))

    return result_str