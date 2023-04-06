#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of
the web_static folder of your AirBnB Clone repo, distributes an archive
to your web servers, and deploys it on your servers.
"""

import os.path
from fabric.api import env, put, run
from fabric.operations import sudo


env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder
        archive_name = os.path.basename(archive_path)
        folder_name = '/data/web_static/releases/' + \
            archive_name.split('.')[0]
        run('sudo mkdir -p {}'.format(folder_name))
        run('sudo tar -xzf /tmp/{} -C {}'.
            format(archive_name, folder_name))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(archive_name))

        # Move contents of the folder into folder_name
        run('sudo mv {}/web_static/* {}'.format(folder_name, folder_name))

        # Remove web_static folder
        run('sudo rm -rf {}/web_static'.format(folder_name))

        # Delete the symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create new symbolic link
        run('sudo ln -s {} /data/web_static/current'.
            format(folder_name))
    except:
        return False
    else:
        return True

