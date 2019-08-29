# -*- coding: utf-8 -*-
############################################################
#
# Read & Modify commits of a Git Reposotory
#
############################################################

import os
import sys

import argparse
import subprocess

import datetime
from git import Repo, RefLog
import json

from loguru_helper import message_logger, event_logger, emit_logger


class GitModifier(object):

    def __init__(self, repo_path):
        self.repo = Repo(repo_path)

    @classmethod
    def format(cls, obj):
        template = """'
        if  test "$GIT_COMMIT" = "{commit_id}"
        then
            export GIT_AUTHOR_DATE="{date}"
            export GIT_COMMITTER_DATE="{date}"
            export GIT_AUTHOR_NAME="{user}"
            export GIT_AUTHOR_EMAIL="{email}"
        fi'
        """

        return template.format(commit_id=obj.get('id'),
                               date=obj.get('date'),
                               user=obj.get('author').get('name'),
                               email=obj.get('author').get('email'))

    @classmethod
    def to_timestamp(cls, date):
        return (date - datetime.datetime(1970, 1, 1)).total_seconds()

    def get_commits(self, branch_name, max_count=50, begin_date=None, end_date=None):
        if end_date is None:
            end_date = datetime.datetime.now()

        if begin_date is None:
            begin_date = end_date - datetime.timedelta(days=30)

        min_age = self.to_timestamp(end_date)
        max_age = self.to_timestamp(begin_date)
        commmits = list(self.repo.iter_commits(
            branch_name, max_count=max_count, max_age=max_age, min_age=min_age))

        cms = []
        for commit in commmits:
            cms.append(dict(
                commit_id=commit.hexsha,
                author_name=commit.author.name,
                author_date=datetime.datetime.fromtimestamp(
                    commit.authored_date).strftime('%Y-%m-%d %H:%M:%S'),
                commit_date=datetime.datetime.fromtimestamp(
                    commit.committed_date).strftime('%Y-%m-%d %H:%M:%S'),
                commit_message=commit.message
            ))
        return cms


def execute(cmd: str) -> str:
    """Excuete a shell command, get result
    """
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) as proc:
        lines = proc.stdout.readlines()
        return '\n'.join([line.decode("utf-8").strip() for line in lines])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Console2RabbitMQ')
    parser.add_argument('-p', dest='path', type=str, default="/var/lib/repo")
    parser.add_argument('--export', dest='export', action='store_true')
    parser.add_argument('--modify', dest='modify', action='store_true')
    parser.add_argument('-f', dest='file', type=str, default="commits.json")
    args = parser.parse_args()
    # event_logger.warning(f'args={args}')
    if(args.export):
        repo = Repo(args.path)
        event_logger.opt(ansi=True).info(f'[{args.path}] begin export ...')
        if os.path.exists(args.file):
            event_logger.error(f"file [{args.file}] exist, cancel export")
            sys.exit(0)
        f = open(args.file, 'w')
        for log in repo.iter_commits():
            committer = log.committer
            obj = {'id': log.hexsha,
                   'author': {'email': committer.email, 'name': committer.name},
                   'date': str(log.authored_datetime),
                   'message': str(log.message.strip())}
            # emit_logger.info(f'{obj}')
            f.write(json.dumps(obj)+'\n')
            emit_logger.opt(ansi=True).debug(
                f'<level>{log.hexsha}</level>\t<cyan>{log.authored_datetime}</cyan>\t<blue>{committer.email}</blue>\t<green>{log.message.strip()}</green>')
        f.close()
        event_logger.opt(ansi=True).info(f'write to {args.file}')
    if(args.modify):
        # repo = Repo(args.path)
        with open(args.file) as f:
            for line in f:
                obj = json.loads(line)
                event_logger.opt(ansi=True).info(
                    f"<level>{obj.get('id')}</level>\t<cyan>{obj.get('date')}</cyan>\t<blue>{obj.get('author').get('email')}</blue>\t<green>{obj.get('message')}</green>")
                cmd = f"git -C {args.path} filter-branch -f --env-filter {GitModifier.format(obj)}"
                # repo.git.filter_branch("-f", "--env-filter \\\n", 'cmd')
                emit_logger.opt(ansi=True).debug(execute(cmd))
