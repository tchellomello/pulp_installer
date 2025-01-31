# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by bootstrap.py. Please use
# bootstrap.py to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

import glob
import os
import re
import subprocess
import sys

from github import Github

KEYWORDS = ["fixes", "closes", "re", "ref"]
NO_ISSUE = "[noissue]"
STATUSES = ["NEW", "ASSIGNED", "POST", "MODIFIED"]
CHANGELOG_EXTS = [".feature", ".bugfix", ".doc", ".removal", ".misc", ".dev"]

sha = sys.argv[1]
message = subprocess.check_output(["git", "log", "--format=%B", "-n 1", sha]).decode("utf-8")
g = Github(os.environ.get("GITHUB_TOKEN"))
repo = g.get_repo("pulp/pulp_installer")


def __check_status(issue):
    gi = repo.get_issue(int(issue))
    if gi.pull_request:
        sys.exit(f"Error: issue #{issue} is a pull request.")
    if gi.closed_at:
        sys.exit(f"Error: issue #{issue} is closed.")


def __check_changelog(issue):
    matches = glob.glob("CHANGES/{issue}.*".format(issue=issue))

    if len(matches) < 1:
        sys.exit("Could not find changelog entry in CHANGES/ for {issue}.".format(issue=issue))
    for match in matches:
        if os.path.splitext(match)[1] not in CHANGELOG_EXTS:
            sys.exit("Invalid extension for changelog entry '{match}'.".format(match=match))


print("Checking commit message for {sha}.".format(sha=sha[0:7]))

# validate the issue attached to the commit
if NO_ISSUE in message:
    print("Commit {sha} has no issue attached. Skipping issue check".format(sha=sha[0:7]))
else:
    regex = r"(?:{keywords})[\s:]+#(\d+)".format(keywords=("|").join(KEYWORDS))
    pattern = re.compile(regex, re.IGNORECASE)

    issues = pattern.findall(message)

    if issues:
        for issue in pattern.findall(message):
            __check_status(issue)
            __check_changelog(issue)
    else:
        sys.exit(
            "Error: no attached issues found for {sha}. If this was intentional, add "
            " '{tag}' to the commit message.".format(sha=sha[0:7], tag=NO_ISSUE)
        )

print("Commit message for {sha} passed.".format(sha=sha[0:7]))
