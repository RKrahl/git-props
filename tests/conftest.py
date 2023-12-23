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
            yield pytest.param(case, id=case.repo, marks=marks)

def get_test_repo(base, repo):
    repo_archive = get_testdata("%s.tar.bz2" % repo)
    with tarfile.open(repo_archive, "r") as tarf:
        try:
            tarf.extraction_filter = tarfile.fully_trusted_filter
        except AttributeError:
            pass
        tarf.extractall(path=base)
    return base / repo


@pytest.fixture(scope="module")
def tmpdir():
    path = Path(tempfile.mkdtemp(prefix="git-props-test-"))
    yield path
    shutil.rmtree(path)

@pytest.fixture(scope="module", params=get_test_cases())
def repo_case(tmpdir, request):
    case = request.param
    r = get_test_repo(tmpdir, case.repo)
    return case._replace(repo=GitRepo(r))


def pytest_report_header(config):
    """Add information on the package version used in the tests.
    """
    modpath = Path(gitprops.__file__).resolve().parent
    return [ "gitprops: %s" % (gitprops.__version__),
             "          %s" % (modpath)]
