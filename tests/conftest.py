from pathlib import Path
import gitprops

def pytest_report_header(config):
    """Add information on the package version used in the tests.
    """
    modpath = Path(gitprops.__file__).resolve().parent
    return [ "gitprops: %s" % (gitprops.__version__),
             "          %s" % (modpath)]
