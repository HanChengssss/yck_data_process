import traceback
from yck_data_process.logingDriver import Logger
import pymysql
log_dir_full_path = "D:\YCK\代码\yck_data_process\yck_data_process\log_dir_feature"
log = Logger(filename="{}\outoutData.log".format(log_dir_full_path), level='error')

# def traceback_test_driver():
#     try:
#         raise Exception("this is a error")
#     except:
#         ret = traceback.format_stack()
#         print(ret)

# def traceback_test_driver():
#     try:
#         pymysql.connect("xxxx")
#     except:
#         traceback.print_exc()
#         ret = traceback.format_stack()
#         print(ret)


def traceback_test_driver():
    pymysql.connect("xxxx")

def run_test_driver():
    try:
        traceback_test_driver()
    except:
        ret = traceback.format_exc()
        print(ret)

if __name__ == '__main__':
    run_test_driver()