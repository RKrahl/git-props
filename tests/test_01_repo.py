"""Test module gitprops.repo
"""

from collections import namedtuple
import pytest
from gitprops.repo import GitError, GitRepo
from conftest import get_test_repo

Case = namedtuple('Case', [
    'repo', 'tag', 'count', 'node', 'commit', 'dirty', 'date'
])
cases = [
    Case(
        repo = 'empty',
        tag = None,
        count = 0,
        node = None,
        commit = None,
        dirty = False,
        date = None,
    )
]
case_params = [ pytest.param(c, id=c.repo) for c in cases ]

@pytest.fixture(scope="module", params=case_params)
def repo_case(tmpdir, request):
    case = request.param
    r = get_test_repo(tmpdir, case.repo)
    return case._replace(repo=GitRepo(r))

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
