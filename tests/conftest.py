from pathlib import Path
import shutil
import tarfile
import tempfile
import pytest
import gitprops

testdir = Path(__file__).resolve().parent
testdatadir = testdir / "data"


def get_testdata(fname):
    fname = testdatadir / fname
    assert fname.is_file()
    return fname

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


def pytest_report_header(config):
    """Add information on the package version used in the tests.
    """
    modpath = Path(gitprops.__file__).resolve().parent
    return [ "gitprops: %s" % (gitprops.__version__),
             "          %s" % (modpath)]
