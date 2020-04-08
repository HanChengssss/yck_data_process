from manage import Manage
import time

def run_mange():
    Manage.run_from_muiltiprocess()
    time.sleep(60*60)

if __name__ == '__main__':
    run_mange()