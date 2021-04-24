import os
import time
import git
import tarfile
from git.exc import *

from threading import Thread


class DownloadGit(Thread):
    """
    """
    def __init__(self):
        Thread.__init__(self)

    def make_repo_tarfile(self, item):
        with tarfile.open(f"{item}.tar.gz", "w:gz") as tar:
            tar.add(item, arcname=os.path.basename(item))

    def run(self):
        """
        :return:
        """
        full_paths = map(lambda name: os.path.join(os.getcwd(), name), os.listdir(os.getcwd()))
        dirs = []

        for path in full_paths:
            if os.path.isdir(path):
                dirs.append(os.path.basename(path))

        try:
            for item in dirs:
                repo = git.Repo(item)
                origin = repo.remotes.origin
                origin.pull()
                self.make_repo_tarfile(item)
        except InvalidGitRepositoryError:
            pass


def main():
    """
    """
    while True:
        thread = DownloadGit()
        thread.start()
        time.sleep(3600)


if __name__ == "__main__":
    main()
