from collections import namedtuple
from pathlib import Path
import shutil
import tarfile
import tempfile
import yaml
import pytest
import gitprops
from gitprops.repo import GitRepo

testdir = Path(__file__).resolve().parent
testdatadir = testdir / "data"
_cleanup = True

Case = namedtuple('Case', [
    'repo', 'tag', 'count', 'node', 'commit', 'dirty', 'date', 'marks',
])

def get_testdata(fname):
    fname = testdatadir / fname
    assert fname.is_file()
    return fname

def get_test_cases():
    casefile = get_testdata("caselist.yaml")
    with open(casefile, "rt") as f:
        for c in yaml.load(f, Loader=yaml.CLoader):
            case = Case(**c)
            marks = case.marks if case.marks else ()
            id = case.repo + "-dirty" if case.dirty else case.repo
            yield pytest.param(case, id=id, marks=marks)

def get_test_repo(base, repo, dirty=False):
    repo_archive = get_testdata("%s.tar.bz2" % repo)
    repo_name = repo + "-dirty" if dirty else repo
    repo_dir = base / repo_name
    tmp_dir = Path(tempfile.mkdtemp(dir=base))
    with tarfile.open(repo_archive, "r") as tarf:
        try:
            tarf.extraction_filter = tarfile.fully_trusted_filter
        except AttributeError:
            pass
        tarf.extractall(path=tmp_dir)
    (tmp_dir / repo).rename(repo_dir)
    tmp_dir.rmdir()
    if dirty:
        (repo_dir / "_taint").touch(exist_ok=False)
        GitRepo(repo_dir)._exec("git add _taint")
    return repo_dir


@pytest.fixture(scope="module")
def tmpdir():
    path = Path(tempfile.mkdtemp(prefix="git-props-test-"))
    yield path
    if _cleanup:
        shutil.rmtree(path)

@pytest.fixture(scope="module", params=get_test_cases())
def repo_case(tmpdir, request):
    case = request.param
    r = get_test_repo(tmpdir, case.repo, case.dirty)
    return case._replace(repo=GitRepo(r))


def pytest_addoption(parser):
    parser.addoption("--no-cleanup", action="store_true", default=False,
                     help="do not clean up temporary data after the test.")

def pytest_configure(config):
    global _cleanup
    _cleanup = not config.getoption("--no-cleanup")

def pytest_report_header(config):
    """Add information on the package version used in the tests.
    """
    modpath = Path(gitprops.__file__).resolve().parent
    return [ "gitprops: %s" % (gitprops.__version__),
             "          %s" % (modpath)]
