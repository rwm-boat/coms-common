import matplotlib as plt
import json



i = 0
with open('log.txt', 'r') as log_file:
    for line in log_file.readlines():
        print(line)
        print(i)