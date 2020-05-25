import os
import time

start = time.time()
os.system('python3 db_banner2.py')
end = time.time()
print('banner rendering took %s seconds.' % (str(end-start)))
