import json
from json import JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                print(obj.isoformat())
                return obj.isoformat()
#print(DateTimeEncoder)
