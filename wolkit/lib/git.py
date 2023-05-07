from pydantic import BaseModel
from git import Repo


class GitRepository:
    id: int
    url: str
    last_commit: str
    branch: str
    repo: Repo

    def __init__(self, url, branch, last_commit=None, id=None):
        self.id = id
        self.url = url
        self.branch = branch
        self.repo = Repo(url)
        self.repo.git.checkout(branch)
        self.last_commit = last_commit if last_commit is not None else self.repo.head.commit.hexsha

    def check_for_changes(self):
        """
        Check if a given repository has had a new commit since
        we last checked
        :return:
        """
        self.repo.remotes.origin.pull()
        latest_commit = self.repo.head.commit.hexsha
        output = latest_commit != self.last_commit
        self.last_commit = latest_commit
        return output
