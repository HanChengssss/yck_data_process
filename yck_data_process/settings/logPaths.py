import glob
import os

logDirNameDic = {
    "normalLog": "log_dir",
    "testLog": "log_dir_test",
}

projectBasePathDic = {
    "local": "D:\YCK\代码\yck_data_process",
}

class LogPathManage():
    def __init__(self, model):
        self.model = model

    def get_logDirName(self):
        logDirName = logDirNameDic.get("testLog") if self.model == "test" else logDirNameDic.get("normalLog")
        if not logDirName:
            raise Exception("logDirName not exist !")
        return logDirName

    def get_projectBasePath(self):
        # 检查文件夹是否存在
        projectBasePath = None
        for pbp in projectBasePathDic.values():
            if os.path.exists(pbp):
                projectBasePath = pbp
                break
        if not projectBasePath:
            raise Exception("projectBasePath not exist !")
        return projectBasePath

    def get_logDirFullPath(self):
        logDirFullPath = None
        projectBasePath = self.get_projectBasePath()
        logDirName = self.get_logDirName()
        for relPath, dirs, files in os.walk(projectBasePath):
            if logDirName in dirs:
                logDirFullPath = os.path.join(projectBasePath, relPath, logDirName)
                break
        if not logDirFullPath:
            raise Exception("logDirFullPath not exist !")
        return logDirFullPath




if __name__ == '__main__':
    ret = LogPathManage.get_logDirFullPath(model="normal")
    print(ret)