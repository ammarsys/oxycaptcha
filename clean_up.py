import os
import time

while True:
    files = os.listdir('./images')
    if len(files) > 10:
        for file in files:
            os.remove(f'./images/{file}')
        print('Successfully did a cleanup!')
    time.sleep(500)
