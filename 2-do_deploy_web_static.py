#!/usr/bin/python3
# Fabfile to distribute an archive to web server.

import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.user = "ubuntu"
env.hosts = ['54.174.113.81', '52.23.177.104']


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    """
    if os.path.isfile(archive_path) is False:
        return False
    fullFile = archive_path.split("/")[-1]
    folder = fullFile.split(".")[0]

    # Uploads archive to directory
    if put(archive_path, "/tmp/{}".format(fullFile)).failed is True:
        print("Uploading archive to /tmp/ failed")
        return False

    # Delete the archive folder
    if run("rm -rf /data/web_static/releases/{}/".
           format(folder)).failed is True:
        print("Deleting folder with archive(if already exists) failed")
        return False

    # Create new archive folder
    if run("mkdir -p /data/web_static/releases/{}/".
           format(folder)).failed is True:
        print("Creating new archive folder failed")
        return False

    # Uncompress archive to directory
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(fullFile, folder)).failed is True:
        print("Uncompressing archive to failed")
        return False

    # Deletes latest archive
    if run("rm /tmp/{}".format(fullFile)).failed is True:
        print("Deleting archive from /tmp/ directory dailed")
        return False

    # Move folder from web_static to its parent folder
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".
           format(folder, folder)).failed is True:
        print("Moving content to archive folder before deletion failed")
        return False

    # Delete the empty web_static file
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(folder)).failed is True:
        print("Deleting web_static folder failed")
        return False

    # Delete current folder
    if run("rm -rf /data/web_static/current").failed is True:
        print("Deleting 'current' folder failed")
        return False

    # Create new symbolic link on web
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(folder)).failed is True:
        print("Creating new symbolic link to new code version failed")
        return False

    print("New version deployed!")
    return True
