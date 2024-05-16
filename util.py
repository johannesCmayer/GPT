import datetime

def timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
