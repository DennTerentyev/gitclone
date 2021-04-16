import os
import git
import config
import tarfile

from threading import Thread


class DownloadGit(Thread):
    """
    """
    def __init__(self, url, thread_name, repo_name):
        Thread.__init__(self)
        self.thread_name = thread_name
        self.url = url
        self.repo_name = repo_name

    def make_repo_tarfile(self):
        with tarfile.open(f"{self.repo_name}.tar.gz", "w:gz") as tar:
            tar.add(self.repo_name, arcname=os.path.basename(self.repo_name))

    def run(self):
        """
        :return:
        """
        full_paths = map(lambda name: os.path.join(os.getcwd(), name), os.listdir(os.getcwd()))
        dirs = []
        print(self.thread_name)
        for path in full_paths:
            if os.path.isdir(path):
                dirs.append(os.path.basename(path))

        if self.repo_name in dirs:
            repo = git.Repo(self.repo_name)
            origin = repo.remotes.origin
            origin.pull()
            self.make_repo_tarfile()
        else:
            git.Repo.clone_from(self.url, self.repo_name)
            self.make_repo_tarfile()


def main(urls):
    """
    """
    for item, url in enumerate(urls):
        repo_name = os.path.basename(url)
        thread_name = "Thread %s" % (item + 1)
        thread = DownloadGit(url, thread_name, repo_name)
        thread.start()


if __name__ == "__main__":
    urls = config.REPOSITORY_NAME
    main(urls)
