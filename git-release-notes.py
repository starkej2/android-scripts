#!/usr/bin/env python3

import argparse
import re
from inspect import currentframe, getframeinfo
from pathlib import Path
from pydriller import RepositoryMining

TARGET_GIT_BRANCH_NAME = "master"
ARGUMENT_PARSER = argparse.ArgumentParser()


def _read_arguments():
    ARGUMENT_PARSER.add_argument("--directory", help="the directory containing the target git repository")
    ARGUMENT_PARSER.add_argument("from_tag", metavar="src-dir", help="the tag of the previous version")
    args = ARGUMENT_PARSER.parse_args()
    return args


def _get_current_directory():
    filename = getframeinfo(currentframe()).filename
    return Path(filename).resolve().parent


def _add_brackets_to_issue_number(issue_number):
    naked_issue_number_pattern = '(^[^[]*ISSUE-([0-9])+(\S*))'
    return re.sub(re.compile(naked_issue_number_pattern), r'[\1]', issue_number)


def _capitalize_first_word(text):
    return "%s%s" % (text[0].upper(), text[1:])


def _prettify_commit_title(title):
    title = _add_brackets_to_issue_number(title)
    title = _capitalize_first_word(title)
    return "* {}".format(title)


def _print_formatted_commit_titles(working_directory, from_tag):
    commits = RepositoryMining(
        path_to_repo=working_directory,
        from_tag=from_tag,
        only_in_branch=TARGET_GIT_BRANCH_NAME,
        only_no_merge=True
    ).traverse_commits()

    for commit in commits:
        title = commit.msg.partition('\n')[0]
        print(_prettify_commit_title(title))


def main():
    args = _read_arguments()

    working_directory = args.directory if args.directory is not None else _get_current_directory()

    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    print("Showing commits on the [{branch_name}] branch since tag: [{from_tag}] - {path}"
          .format(from_tag=args.from_tag, path=working_directory, branch_name=TARGET_GIT_BRANCH_NAME))
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    _print_formatted_commit_titles(working_directory, args.from_tag)


main()
