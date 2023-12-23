"""Test module gitprops.repo
"""

import pytest
from gitprops.repo import GitError, GitRepo
from conftest import get_test_repo


def test_repo_version_meta(repo_case):
    repo = repo_case.repo
    meta = repo.get_version_meta()
    assert meta.tag == repo_case.tag
    assert meta.count == repo_case.count
    assert meta.node == repo_case.node

def test_repo_commit(repo_case):
    repo = repo_case.repo
    if repo_case.commit is not None:
        assert repo.get_last_commit() == repo_case.commit
    else:
        with pytest.raises(GitError):
            repo.get_last_commit()

def test_repo_last_version(repo_case):
    repo = repo_case.repo
    assert repo.get_last_version() == repo_case.tag

def test_repo_dirty(repo_case):
    repo = repo_case.repo
    assert repo.is_dirty() == repo_case.dirty

def test_repo_date(repo_case):
    repo = repo_case.repo
    assert repo.get_date() == repo_case.date