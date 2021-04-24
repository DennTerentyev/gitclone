import os
import sys
import git
import shutil


from threading import Thread


class DownloadGit(Thread):
    """
    """

    def __init__(self, url, repo_name, destination):
        Thread.__init__(self)
        self.url = url
        self.repo_name = repo_name
        self.destination = destination

    def run(self):
        """
        :return:
        """
        cache_dir = os.getcwd() + '/cache/'

        current_full_paths = map(lambda name: os.path.join(self.destination, name), os.listdir(self.destination))
        cache_full_paths = map(lambda name: os.path.join(cache_dir, name), os.listdir(cache_dir))

        current_dirs = []
        cache_dirs = []

        for path in current_full_paths:
            if os.path.isdir(path):
                current_dirs.append(os.path.basename(path))

        for path in cache_full_paths:
            if os.path.isdir(path):
                cache_dirs.append(os.path.basename(path))

        if self.repo_name in current_dirs and self.repo_name in cache_dirs:
            pass
        elif self.repo_name not in current_dirs and self.repo_name in cache_dirs:
            cache_repo = f'{self.destination}/cache/{self.repo_name}'
            repo = git.Repo(cache_repo)
            origin = repo.remotes.origin
            origin.pull()
            shutil.copytree(
                cache_repo,
                f'{self.destination}/{self.repo_name}',
                dirs_exist_ok=True
            )
        else:
            cache = f'{self.destination}/cache/{self.repo_name}'
            git.Repo.clone_from(url=self.url, to_path=cache)
            destination = f'{self.destination}/{self.repo_name}'
            shutil.copytree(cache, destination, dirs_exist_ok=True)


def main(url, destination):
    """
    """
    repo_name = os.path.basename(url)
    thread = DownloadGit(url, repo_name, destination)
    thread.start()


if __name__ == "__main__":
    url = sys.argv[1]
    destination = sys.argv[2]
    # url = 'https://github.com/DennTerentyev/Dockerfiles'
    # destination = os.getcwd()
    main(url, destination)
