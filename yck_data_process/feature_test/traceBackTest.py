import traceback
from yck_data_process.logingDriver import Logger

log_dir_full_path = ""
log = Logger(filename="{}\outoutData.log".format(log_dir_full_path), level='error')