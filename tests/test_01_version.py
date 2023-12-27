"""Test module icat.helper
"""

import packaging.version
import pytest
from gitprops.version import Version


@pytest.mark.parametrize(("vstr", "checks"), [
    ("4.11.1", [
        (lambda v: v == "4.11.1", True),
        (lambda v: v < "4.11.1", False),
        (lambda v: v > "4.11.1", False),
        (lambda v: v < "5.0.0", True),
        (lambda v: v > "4.11.0", True),
        (lambda v: v > "4.9.3", True),
        (lambda v: v == Version("4.11.1"), True),
    ]),
    ("5.0.0a1", [
        (lambda v: v == "5.0.0", False),
        (lambda v: v < "5.0.0", True),
        (lambda v: v > "4.11.1", True),
        (lambda v: v == "5.0.0a1", True),
        (lambda v: v < "5.0.0a2", True),
        (lambda v: v < "5.0.0b1", True),
    ]),
])
def test_version(vstr, checks):
    """Test class Version.
    """
    version = Version(vstr)
    for check, res in checks:
        assert check(version) == res

def test_version_set():
    s = set()
    s.add(Version("1.0"))
    s.add(Version("1.0.1"))
    assert len(s) == 2
    s.add(Version("1.0.0"))
    assert len(s) == 2
    assert Version("1") in s
    assert Version("1.0") in s
    assert Version("1.0.0") in s
    assert Version("1.0.1") in s
    assert Version("1.0.0.0") in s
