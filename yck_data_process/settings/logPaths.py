import glob
import os

logDirName = {
    "normalLog": "log_dir"
}

projectBasePath = {

}
# ../*.py
# ../log_dir
# print(glob.glob(r'*.py'))

def findfile(start, name):
    # print(os.walk(start))
    for relpath, dirs, files in os.walk(start):
        # print(relpath, dirs, files)
        if name in dirs:
            print(relpath)
            full_path = os.path.join(start, relpath, name)
            print(os.path.normpath(os.path.abspath(full_path)))

if __name__ == '__main__':
    findfile(start="D:\YCK\代码\yck_data_process\yck_data_process", name="log_dir")