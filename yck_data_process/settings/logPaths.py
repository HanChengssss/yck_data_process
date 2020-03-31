import glob
import os

logDirNameDic = {
    "normalLog": "log_dir",
    "testLog": "log_dir_test",
}

projectBasePathDic = {
    "local": "D:\YCK\代码\yck_data_process\yck_data_process\dir",
}

class LogPathManage():

    @staticmethod
    def get_logDirName(model):
        return logDirNameDic.get("testLog") if model == "test" else logDirNameDic.get("normalLog")

    @staticmethod
    def get_projectBasePath():
        # 检查文件夹是否存在
        projectBasePathExistResultDic = {
            "isExist": False,
            "projectBasePath": None
        }
        for projectBasePath in projectBasePathDic.values():
            if os.path.exists(projectBasePath):
                projectBasePathExistResultDic["isExist"] = True
                projectBasePathExistResultDic["projectBasePath"] = projectBasePath
        return projectBasePathExistResultDic


    @staticmethod
    def get_logDirFullPathDic(model):
        findDirFullPathResult = {
            "logDirFullPath": None,
            "isFound": False
        }
        logdirName = LogPathManage.get_logDirName(model)
        try:
            projectBasePathExistResultDic = LogPathManage.get_projectBasePath()
            assert projectBasePathExistResultDic.get("isExist")
            projectBasePath = projectBasePathExistResultDic.get("projectBasePath")
            for relPath, dirs, files in os.walk(projectBasePath):
                if logdirName in dirs:
                    logDirFullPath = os.path.join(projectBasePath, relPath, logdirName)
                    findDirFullPathResult["logDirFullPath"] = logDirFullPath
                    findDirFullPathResult["isFound"] = True
                    break
        except:
            print("projectBasePath no exist!")
        finally:
            return findDirFullPathResult



if __name__ == '__main__':
    ret = LogPathManage.get_logDirFullPathDic(model="normal")
    print(ret)