
import re
import phonenumbers

x = '+442083661177--'
if re.search('[a-zA-Z]', x):
    print 'Invalid'
else:
    x = phonenumbers.parse(x, None)
    print x
    print phonenumbers.is_possible_number(x)
    print phonenumbers.is_valid_number(x)
