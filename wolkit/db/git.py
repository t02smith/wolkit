import sqlite3
from typing import List
import errors.git
from db import _cursor, _connection
from lib.git import GitRepository

def create_git_repo_table():
    _cursor.execute("""CREATE TABLE IF NOT EXISTS git_repos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE NOT NULL,
        last_commit TEXT,
        branch TEXT
    )""")


def new_git_repo(repo: GitRepository):
    try:
        _cursor.execute(
            "INSERT INTO git_repos (url, last_commit, branch) VALUES (?, ?, ?)",
            (repo.url, repo.last_commit, repo.branch)
        )
        _connection.commit()
    except sqlite3.IntegrityError as e:
        raise errors.git.GitRepositoryAlreadyTracker(e.args[0])


def get_all_repositories() -> List[GitRepository]:
    return [ GitRepository(url=g[1], last_commit=g[2], branch=g[3], id=g[0]) for g in _cursor.execute("SELECT * FROM git_repos;").fetchall()]
