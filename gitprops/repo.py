"""Provide class GitRepo
"""

from collections import namedtuple
import datetime
import os
from pathlib import Path
import subprocess
from gitprops.version import Version


class GitError(Exception):
    pass


VersionMeta = namedtuple('VersionMeta', ['tag', 'count', 'node'])


class GitRepo:
    """Determine properties of the git repository.
    """

    def _exec(self, cmd):
        try:
            proc = subprocess.run(cmd.split(),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  cwd=self.root,
                                  check=True,
                                  env=dict(os.environ, LC_ALL='C'),
                                  universal_newlines=True)
            return proc.stdout.strip()
        except subprocess.CalledProcessError as exc:
            raise GitError("git command '%s' failed" % cmd) from exc

    def __init__(self, root="."):
        self.root = Path(root).resolve()
        # Run git version mostly in order to fail early should the git
        # command not be available
        self.git_version = self._exec("git version")
        self.root = Path(self._exec("git rev-parse --show-toplevel"))
        self._version_meta = None

    def get_version_meta(self):
        if not self._version_meta:
            try:
                descr = self._exec("git describe --tags --long --match *.*")
                tag, count, node = descr.split('-')
                self._version_meta = VersionMeta(tag, int(count), node)
            except GitError:
                try:
                    revs = self._exec("git rev-list HEAD")
                    count = revs.count('\n') + 1
                    commit = self.get_last_commit()
                    node = 'g' + commit[:7]
                    self._version_meta = VersionMeta(None, count, node)
                except GitError:
                    self._version_meta = VersionMeta(None, 0, None)
        return self._version_meta

    def get_last_commit(self):
        return self._exec("git rev-parse --verify --quiet HEAD")

    def get_last_version(self):
        candidate_tags = set()
        shadowed_tags = set()
        try:
            tags = self._exec("git tag --merged").split('\n')
        except GitError:
            return None
        for t in tags:
            try:
                candidate_tags.add(Version(t))
            except ValueError:
                continue
            for t1 in self._exec("git tag --merged %s" % t).split('\n'):
                if t1 == t:
                    continue
                try:
                    shadowed_tags.add(Version(t1))
                except ValueError:
                    continue
        versions = candidate_tags - shadowed_tags
        if versions:
            return sorted(versions)[-1]
        else:
            return None

    def is_dirty(self):
        return bool(self._exec("git status --porcelain --untracked-files=no"))

    def get_date(self):
        if self.is_dirty():
            return datetime.date.today()
        else:
            try:
                ts = int(self._exec("git log -1 --format=%ad --date=unix"))
                return datetime.date.fromtimestamp(ts)
            except GitError:
                return None
