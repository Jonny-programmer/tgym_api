from datetime import date

from flask.json import JSONEncoder


class MyJsonEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, date):
            return object.isoformat()
        return super().default(object)