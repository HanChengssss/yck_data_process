from manage import run_from_muiltiprocess
import time
from apscheduler.schedulers.blocking import BlockingScheduler

# 每间隔1小时执行一次任务
def run_manage():
    sched = BlockingScheduler()
    sched.add_job(run_from_muiltiprocess, 'interval', seconds=60*60)
    sched.print_jobs()
    sched.start()


if __name__ == '__main__':
    run_manage()
