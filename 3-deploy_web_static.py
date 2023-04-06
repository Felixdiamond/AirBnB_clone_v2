#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to your web servers
"""

from datetime import datetime
from fabric.api import env, put, run
import os


env.hosts = ['100.26.173.94', '35.153.79.52']
env.user = 'ubuntu'


def do_pack():
    """Create a tgz archive of web_static content"""

    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = "versions/web_static_{}.tgz".format(date)
        command = "tar -cvzf {} web_static".format(file_path)
        os.system(command)
        return file_path
    except:
        return None


def do_deploy(archive_path):
    """Deploy archive to web servers"""

    if not os.path.exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_ext_name = file_name.split(".")[0]
        path = "/data/web_static/releases/{}/".format(no_ext_name)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, path))
        run("rm /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(path, path))
        run("rm -rf {}web_static".format(path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path))
        return True
    except:
        return False


def deploy():
    """Create and distribute archive to web servers"""

    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

