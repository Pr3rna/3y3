import sys

map = (False, True)
try:
    val = int(sys.argv[1])
    a = open('config.txt', 'w')
    a.write(str(map[val]))
    a.close()
except:
    pass