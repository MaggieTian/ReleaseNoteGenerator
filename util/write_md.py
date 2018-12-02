#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @File    : write_md.py
# @Date    : 2018-11-28
# @Author  : qitian
import os
import datetime
import tempfile
from .git_cmd import Git
from .process_commits import ProcessCommits
from .logger import Logger


class WriteMd:
    def __init__(self, ):
        pass

    @staticmethod
    def write_md(change_msg, output_md, version, logger):

        # copy the original file to a temp file
        flag = 0
        if os.path.exists(output_md):
            flag = 1
            temp_file = tempfile.TemporaryFile(mode='wb+')
            with open(output_md, "r") as origin_file:
                for f in origin_file:
                    temp_file.write(bytes(f, encoding="utf-8"))

        # 开始写最新版本的changelog到md文件
        release_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if change_msg:
            version = "## {version} ({date}) ".format(version=version, date=release_time)
            output = open(output_md, "wb")
            output.write(bytes(version + '\n', encoding="utf-8"),)
            output.write(bytes("___" + '\n', encoding="utf-8"))
            for k, v in change_msg.items():

                # if a type has no change,then should not write in md
                if len(v) == 0:
                    continue
                output.write(bytes("\n### {msg}".format(msg=k), encoding="utf-8"))
                output.write(bytes("({cnt} changes)\n".format(cnt=len(v)), encoding="utf-8"))
                output.write(bytes("___" + '\n', encoding="utf-8"))
                for commit in v:

                    title_msg = ProcessCommits.check_msg(commit["title"])
                    commit_msg = ProcessCommits.check_msg(commit["message_line"][0] if commit["message_line"] else "")
                    # title is in format
                    if title_msg:
                        output.write(bytes("* {msg} \n".format(msg=commit["title"]), encoding="utf-8"))
                        # title and commit msg are in format
                        if commit_msg and commit["message_line"]:
                            for line in commit["message_line"]:
                                output.write(bytes("  --{msg} \n".format(msg=line), encoding="utf-8"))

                    # only commit msg is in format(merge request)
                    elif commit_msg:
                        for index, line in enumerate(commit["message_line"]):
                            if index == 0:
                                output.write(bytes("* {msg} \n".format(msg=line), encoding="utf-8"))
                            else:
                                output.write(bytes("  --{msg} \n".format(msg=line), encoding="utf-8"))

                output.write(bytes("\n", encoding="utf-8"))
            output.close()

            # write the origin md file in new md file
            if flag == 1:
                temp_file.seek(0)
                with open(output_md, "ab+") as f:
                    line = temp_file.readline()
                    while line:
                        f.write(line)
                        line = temp_file.readline()
                    temp_file.close()
                f.close()

    @staticmethod
    def write_release_note(change_msg, output_md, version, logger):

        if not change_msg:
            logger.info("there is no commits that fit in format")
            return

        # check outputmd,if it is a dir,then specify the file name
        if output_md:
            output_md = os.path.abspath(output_md)
            if os.path.isdir(output_md):
                output_md = os.path.join(output_md, "CHANGELOG.md")
                WriteMd.write_md(change_msg, output_md, version, logger)

            if os.path.isfile(output_md):
                WriteMd.write_md(change_msg, output_md, version, logger)
            else:
                logger.error('''the output_md is not right path:{output}'''.format(output=output_md))
                raise Exception('''the output_md is not right path:{output}'''.format(output=output_md))
        else:
            output_md = "CHANGELOG.md"
            WriteMd.write_md(change_msg, output_md, version, logger)
        return output_md


if __name__ == '__main__':

    logger = Logger.get_logger()
    commits = Git.log(None, None, r"/home/qitian/test",logger)
    p = ProcessCommits(commits,logger).main()
    WriteMd.write_md(p, "CHANGELOG.md", "1.0", logger)