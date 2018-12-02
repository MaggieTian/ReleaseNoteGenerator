#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @File    : generate_release_note.py
# @Date    : 2018-11-28
# @Author  : qitian


from util.git_cmd import Git
from util.process_commits import ProcessCommits
from util.options import parse_options,show_usage
from util.write_md import WriteMd
from util.logger import Logger
import sys


if __name__ == '__main__':

    options, args = parse_options()
    log_range = sys.argv[1]
    if not log_range and options:
        show_usage()

    logger = Logger.get_logger()
    try:
        # get git log commits
        commits = Git.log(options.merges, log_range, options.project_path, logger)

        # classify commits in every type
        classification_commits = ProcessCommits(commits, logger).main()

        # write into md file to generate release note
        output_md = WriteMd.write_release_note(classification_commits, options.output, options.version, logger)
        logger.info("generate release note successfully! : {output}".format(output=output_md))

    except Exception:
        raise
