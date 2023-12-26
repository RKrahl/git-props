"""Provide class Verson
"""

import itertools
import packaging.version


class Version(packaging.version.Version):
    """Represent a version number.

    This class extends :class:`packaging.version.Version`:

    + add a __hash__() method,
    + add comparison with strings.

    >>> version = Version('4.11.1')
    >>> version == '4.11.1'
    True
    >>> version < '4.9.3'
    False
    >>> version = Version('5.0.0a1')
    >>> str(version)
    '5.0.0a1'
    >>> version > '4.11.1'
    True
    >>> version < '5.0.0'
    True
    >>> version == '5.0.0a1'
    True
    """
    def __hash__(self):
        # strip trailing zero components from release
        release = tuple(
            reversed(list(
                itertools.dropwhile(
                    lambda x: x == 0,
                    reversed(self._version.release),
                )
            ))
        )
        return hash(self._version._replace(release=release))

    def __lt__(self, other):
        if isinstance(other, str):
            other = type(self)(other)
        return super().__lt__(other)

    def __le__(self, other):
        if isinstance(other, str):
            other = type(self)(other)
        return super().__le__(other)

    def __eq__(self, other):
        if isinstance(other, str):
            other = type(self)(other)
        return super().__eq__(other)

    def __ge__(self, other):
        if isinstance(other, str):
            other = type(self)(other)
        return super().__ge__(other)

    def __gt__(self, other):
        if isinstance(other, str):
            other = type(self)(other)
        return super().__gt__(other)

    def __ne__(self, other):
        if isinstance(other, str):
            other = type(self)(other)
        return super().__ne__(other)
