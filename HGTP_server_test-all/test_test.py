import os, sys


project_root =r'D:\zheng_da\2020.9.10\HGTP_server_test-all'
print(project_root)


python_root = sys.exec_prefix
print(python_root)


command = python_root + '\Scripts\pip freeze > ' + project_root + '\\requirements.txt'
print(command)


os.system(command)