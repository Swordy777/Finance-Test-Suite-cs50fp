import os
import re
from random import random
from urllib.parse import urlparse, unquote

def extract_filename(link):
        parsed_url = urlparse(link).path
        fullname = os.path.split(parsed_url)[1]
        fullname = unquote(fullname)
        print(fullname)
        name = re.sub(r'(.jpg)$', "" , fullname)
        name = re.sub(r'-', " " , name)
        name = name.upper()
        return name

#pretty sure this can be transformed into fixture
def generate_input(input): # pass fixture that connects to db
        if input == "user" or input == "pass":
            result = input
            for digit in range(6):
                result += str(int(random()*10))
            #after generating the username/password, check the db if it exists, if yes, repeat
            return result
        else:
            raise Exception("generate_input error: received argument is not \"user\" or \"pass\"")
