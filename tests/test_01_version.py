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

@pytest.mark.parametrize("vstr", [
    "1.dev0", "v1.dev0",
    "1.0.dev456", "v1.0.dev456",
    "1.0a1", "v1.0a1",
    "1.0a2.dev456", "v1.0a2.dev456",
    "1.0a12.dev456", "v1.0a12.dev456",
    "1.0a12", "v1.0a12",
    "1.0b1.dev456", "v1.0b1.dev456",
    "1.0b2", "v1.0b2",
    "1.0b2.post345.dev456", "v1.0b2.post345.dev456",
    "1.0b2.post345", "v1.0b2.post345",
    "1.0rc1.dev456", "v1.0rc1.dev456",
    "1.0rc1", "v1.0rc1",
    "1.0", "v1.0",
    "1.0+abc.5", "v1.0+abc.5",
    "1.0+abc.7", "v1.0+abc.7",
    "1.0+5", "v1.0+5",
    "1.0.post456.dev34", "v1.0.post456.dev34",
    "1.0.post456", "v1.0.post456",
    "1.0.15", "v1.0.15",
    "1.1.dev1", "v1.1.dev1",
])
def test_version_string(vstr):
    assert str(Version(vstr)) == vstr
