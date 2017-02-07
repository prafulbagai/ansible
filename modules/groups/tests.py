
import ast
import json


response = 'BMSOTP'

try:
    response = json.loads(response)
except:
    try:
        response = ast.literal_eval(response)
    except:
        try:
            response = eval(response)
        except:
            pass

print response
