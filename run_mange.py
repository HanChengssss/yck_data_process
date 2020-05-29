from manage import Manage


def run_manage():
    source_type = "mysql"
    Manage.run_from_muiltiprocess(source_type)


if __name__ == '__main__':
    run_manage()
