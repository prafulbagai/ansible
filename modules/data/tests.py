
import os

file_name = '1'
command = 'mysqldump -uroot -p17 message_groups > ' + file_name
os.system(command)
