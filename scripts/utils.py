import datetime
import random

def generateId():
    name = 'output' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randrange(1000000))

    return name