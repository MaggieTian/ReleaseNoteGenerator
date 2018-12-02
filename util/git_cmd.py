#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @File    : git_cmd.py
# @Date    : 2018-11-13
# @Author  : qitian

import os
import re
from .logger import Logger


class Git:

    def __init__(self):
        pass

    @staticmethod
    # run git log cm to get commit msg
    def log(merges, range, path, logger):
        '''

        :param merges: merges flag is None,stand for all git log,
                       True,stand for git log that only merge request
                       False is that git log contains normal commits which is not merge quest
        :param range:  get the git history in the range
        :param path:   the path of project
        :return: commits object that contains all commits
        '''

        # the format of git log
        format_options = "%n".join([

             "newCommit", "sha1:%H", "authorName:%an", "authorEmail:%ae", "authorDate:%aD",
             "committerName:%cn", "committerEmail:%ce", "committerDate:%cD",
             "title:%s", "%w(80,1,1)%b"
        ])

        git_args = ["log", "--no-color"]
        if merges is not None:
            merge_commits = ("--merges" if merges else "--no-merges")
            git_args.append(merge_commits)
        git_args.append('--format="{format_options}"'.format(format_options=format_options))

        logs_cmd = " ".join(git_args)
        range = range if range else ""
        cmd = "cd {path} && git {log} {range}".format(path=path, log=logs_cmd, range=range)
        logger.info("git log cmd:"+cmd)

        try:
            commits_result = os.popen(cmd)
            data = ""
            for line in commits_result:
                data += line
            commits = Git.process_commits(data)
            return commits
        except Exception:
            raise

    @classmethod
    def process_commits(cls, data):
        commits = []
        working_commit = None
        data = data.split("\n")
        for line_data in data:
            if len(line_data) > 0:
                line = Git.paser_line(line_data)
                if line["type"] == "new":
                    working_commit = {
                        "message_line": []
                    }
                    commits.append(working_commit)
                elif line["type"] == "message":
                    if not Git.filter_msg(line["message"]):
                        working_commit["message_line"].append(line["message"])
                else:
                    working_commit[line["type"]] = line["message"]
        return commits

    @classmethod
    def paser_line(cls, line):

        # a new commit
        if line == "newCommit":

            return {
                 "type": "new"
              }
        # identify every key:value pair in line data,such as authorName:qi.tian
        pattern = r"^([a-zA-Z]+1?)\s?:\s?(.*)$"
        re.compile(pattern)
        msg = re.match(pattern, line)
        if msg:
            return {
                "type": msg.group(1),
                "message": msg.group(2).strip()
            }
        # identify commit message body
        else:

            return {
                "type": "message",
                "message": line.strip()
            }

    @classmethod
    def normalize_newlines(cls, data):
        return data.replace(r"\r\n?|[\n\u2028\u2029]", "\n").replace(r"^\uFEFF", '')

    @staticmethod
    def get_merge_or_revert_msg():
        return ['See merge request', 'This reverts merge request', 'Revert "Merge branch']

    @staticmethod
    def filter_msg(line):
        flag = False
        for pattern in Git.get_merge_or_revert_msg():
            if line.find(pattern) >= 0:
                flag = True
                break
        return flag


if __name__ == '__main__':

    logger = Logger.get_logger()
    Git.log(None, None, r"/home/qitian/test", None, logger)