#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @File    : process_commits.py
# @Date    : 2018-11-28
# @Author  : qitian

from .git_cmd import Git
import re


class ProcessCommits:

    def __init__(self, commits, logger):
        self.TYPES = ['Add', 'Fixed', 'Removed', 'Performance', 'Append', 'Docs', 'Refactor', 'Test', 'Chore','Other']
        self.commits = commits
        self.change_msg = {}
        self.logger = logger

    # initialize entries,every type is a list
    def init_entries(self):
        for t in self.TYPES:
            self.change_msg[t] = []

    def classfy_commit(self):

        for commit in self.commits:
            title_msg = ProcessCommits.check_msg(commit["title"])
            commit_msg = ProcessCommits.check_msg(commit["message_line"][0] if commit["message_line"] else "")
            if title_msg:
                self.change_msg[title_msg.group(1)].append(commit)
            elif commit_msg:
                self.change_msg[commit_msg.group(1)].append(commit)
        self.logger.info("the result commits is:")

        for i in self.change_msg.items():
            self.logger.debug(i)

        return self.change_msg

    @staticmethod
    def check_msg(msg):

        pattern = r"^(Add|Fixed|Removed|Performance|Append|Docs|Refactor|Test|Chore|Other)\s*:\s*#WARP-[0-9]+(.*)$"
        return re.match(pattern, msg)

    # main function
    def main(self):
        self.init_entries()
        data = self.classfy_commit()
        return data

# debug
if __name__ == '__main__':

    commits = Git.log(None, None, r"/home/qitian/test", None)
    logger = Logger.get_logger()
    p = ProcessCommits(commits,logger).main()
    for i in p.items():
        print(i)