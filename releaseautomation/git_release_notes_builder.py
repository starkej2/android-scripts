#!/usr/bin/env python3

import argparse
import re
from inspect import currentframe, getframeinfo
from pathlib import Path
from typing import Optional

from pydriller import RepositoryMining

DEFAULT_TARGET_BRANCH = "master"
ARGUMENT_PARSER = argparse.ArgumentParser()


def _read_arguments():
    ARGUMENT_PARSER.add_argument("from_tag", help="the tag of the previous version")
    ARGUMENT_PARSER.add_argument("--branch_name", help="Git branch name containing the desired commits")
    ARGUMENT_PARSER.add_argument("--path_to_repo", help="the directory containing the target git repository")
    return ARGUMENT_PARSER.parse_args()


def _get_current_directory():
    filename = getframeinfo(currentframe()).filename
    return Path(filename).resolve().parent


def _add_brackets_to_issue_number(issue_number: str):
    naked_issue_number_pattern = "(^[^[]*ISSUE-([0-9])+(\\S*))"
    return re.sub(re.compile(naked_issue_number_pattern), r"[\1]", issue_number)


def _capitalize_first_word(text: str):
    return "%s%s" % (text[0].upper(), text[1:])


def _prettify_commit_title(title: str):
    title = _add_brackets_to_issue_number(title)
    title = _capitalize_first_word(title)
    return "* {}".format(title)


def _print_formatted_commit_titles(from_tag: str, branch_name: str, path_to_repo: str):
    commits = RepositoryMining(
        path_to_repo=path_to_repo,
        from_tag=from_tag,
        only_in_branch=branch_name,
        only_no_merge=True
    ).traverse_commits()

    for commit in commits:
        title = commit.msg.partition('\n')[0]
        print(_prettify_commit_title(title))


def print_notes(from_tag: str,
                branch_name: str = DEFAULT_TARGET_BRANCH,
                path_to_repo: Optional[str] = _get_current_directory()):

    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("Showing commits on the [{branch_name}] branch since tag: [{from_tag}] - {path}"
          .format(from_tag=from_tag, branch_name=branch_name, path=path_to_repo))
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    _print_formatted_commit_titles(from_tag, branch_name, path_to_repo)


def main():
    args = _read_arguments()
    print_notes(
        from_tag=args.from_tag,
        branch_name=args.branch_name if args.branch_name is not None else DEFAULT_TARGET_BRANCH,
        path_to_repo=args.path_to_repo if args.path_to_repo is not None else _get_current_directory()
    )


if __name__ == '__main__':
    main()
