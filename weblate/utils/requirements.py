# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2020 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import unicode_literals

import email.parser
import sys

import pkg_resources
import six
from django.core.exceptions import ImproperlyConfigured

import weblate
from weblate.vcs.git import (
    GithubRepository,
    GitLabRepository,
    GitRepository,
    GitWithGerritRepository,
    SubversionRepository,
)
from weblate.vcs.mercurial import HgRepository

REQUIRES = [
    "Django",
    "siphashc",
    "Whoosh",
    "translate-toolkit",
    "lxml",
    "Pillow",
    "bleach",
    "six",
    "python-dateutil",
    "social-auth-core",
    "social-auth-app-django",
    "django-crispy-forms",
    "oauthlib",
    "django-compressor",
    "djangorestframework",
    "django-appconf",
    "user-agents",
    "filelock",
    "setuptools",
    "jellyfish",
    "openpyxl",
    "celery",
    "kombu",
    "celery-batches",
    "translation-finder",
    "html2text",
    "pycairo",
    "pygobject",
    "diff-match-patch",
    "requests",
    "django-redis",
    "hiredis",
    "sentry_sdk",
    "Cython",
    "misaka",
    "GitPython",
]
if six.PY3:
    REQUIRES.append("borgbackup")

OPTIONAL = [
    "psycopg2",
    "psycopg2-binary",
    "phply",
    "chardet",
    "ruamel.yaml",
    "tesserocr",
    "akismet",
    "boto3",
    "zeep",
    "aeidon",
]


def get_version_module(name, optional=False):
    """Return module object.

    On error raises verbose exception with name and URL.
    """
    try:
        dist = pkg_resources.get_distribution(name)
        metadata = email.parser.Parser().parsestr(dist.get_metadata(dist.PKG_INFO))
        return (
            name,
            metadata.get("Home-page"),
            pkg_resources.get_distribution(name).version,
        )
    except pkg_resources.DistributionNotFound:
        if optional:
            return None
        raise ImproperlyConfigured(
            "Missing dependency {0}, please install using: pip install {0}".format(name)
        )


def get_optional_versions():
    """Return versions of optional modules."""
    result = []

    for name in OPTIONAL:
        module = get_version_module(name, True)
        if module is not None:
            result.append(module)

    if HgRepository.is_supported():
        result.append(
            ("Mercurial", "https://www.mercurial-scm.org/", HgRepository.get_version())
        )

    if SubversionRepository.is_supported():
        result.append(
            (
                "git-svn",
                "https://git-scm.com/docs/git-svn",
                SubversionRepository.get_version(),
            )
        )

    if GitWithGerritRepository.is_supported():
        result.append(
            (
                "git-review",
                "https://pypi.org/project/git-review/",
                GitWithGerritRepository.get_version(),
            )
        )

    if GithubRepository.is_supported():
        result.append(
            ("hub", "https://hub.github.com/", GithubRepository.get_version())
        )

    if GitLabRepository.is_supported():
        result.append(
            ("lab", "https://zaquestion.github.io/lab/", GitLabRepository.get_version())
        )

    return result


def get_versions():
    """Return list of used versions."""
    result = [get_version_module(name) for name in REQUIRES]

    result.append(("Python", "https://www.python.org/", sys.version.split()[0]))

    try:
        result.append(("Git", "https://git-scm.com/", GitRepository.get_version()))
    except OSError:
        raise ImproperlyConfigured("Failed to run git, please install it.")

    return result


def get_versions_list():
    """Return list with version information summary."""
    return (
        [("Weblate", "https://weblate.org/", weblate.GIT_VERSION)]
        + get_versions()
        + get_optional_versions()
    )
