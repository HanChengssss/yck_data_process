import glob
import os

logDirNameDic = {
    "normalLog": "log_dir",
    "testLog": "log_dir_test",
}

projectBasePathDic = {
    "local": "D:\YCK\代码\yck_data_process\yck_data_process",
}

class LogPathManage():

    @staticmethod
    def get_logDirName(model):
        logDirName = logDirNameDic.get("testLog") if model == "test" else logDirNameDic.get("normalLog")
        if not logDirName:
            raise Exception("logDirName not exist !")
        return logDirName

    @staticmethod
    def get_projectBasePath():
        # 检查文件夹是否存在
        projectBasePath = None
        for pbp in projectBasePathDic.values():
            if os.path.exists(pbp):
                projectBasePath = pbp
        if not projectBasePath:
            raise Exception("projectBasePath not exist !")
        return projectBasePath

    @staticmethod
    def get_logDirFullPath(model):
        logDirFullPath = None
        projectBasePath = LogPathManage.get_projectBasePath()
        logDirName = LogPathManage.get_logDirName(model)
        for relPath, dirs, files in os.walk(projectBasePath):
            if logDirName in dirs:
                logDirFullPath = os.path.join(projectBasePath, relPath, logDirName)
                break
        return logDirFullPath




if __name__ == '__main__':
    ret = LogPathManage.get_logDirFullPath(model="normal")
    print(ret)