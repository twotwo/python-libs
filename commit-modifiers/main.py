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

    @staticmethod
    def format(obj):
        template = """
        if test "$GIT_COMMIT" = "{commit_id}"
        then
            GIT_AUTHOR_DATE="{date}"
            GIT_COMMITTER_DATE="{date}"
            GIT_AUTHOR_NAME="{user}"
            GIT_AUTHOR_EMAIL="{email}"
        fi
        """

        return template.format(commit_id=obj.get('id'),
                               date=obj.get('date'),
                               user=obj.get('author').get('name'),
                               email=obj.get('author').get('email'))

    @staticmethod
    def filter_branch(path, msg, verbose=False):
        """
        https://git-scm.com/docs/git-filter-branch

        """
        cmd = f"git -C {path} filter-branch -f --env-filter {msg}"
        if verbose:
            event_logger.info(f"executing...\n{cmd}")
        return GitModifier.execute(cmd)

    @staticmethod
    def execute(cmd: str) -> str:
        """Excuete a shell command, get result
        """
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) as proc:
            lines = proc.stdout.readlines()
            return '\n'.join([line.decode("utf-8").strip() for line in lines])


def chunks(l: list, n: int):
    """
    Yield successive n-sized chunks from l.
    :param list to devide
    :n range to devide
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Console2RabbitMQ')
    parser.add_argument('-p', dest='path', type=str, default="/var/lib/repo")
    parser.add_argument('--export', dest='export', action='store_true')
    parser.add_argument('--modify', dest='modify', action='store_true')
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    parser.add_argument('-r', dest='range', type=int, default=5)
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
        envs = []
        with open(args.file) as f:
            for line in f:
                obj = json.loads(line)
                event_logger.opt(ansi=True).info(
                    f"<level>{obj.get('id')}</level>\t<cyan>{obj.get('date')}</cyan>\t<blue>{obj.get('author').get('email')}</blue>\t<green>{obj.get('message')}</green>")
                envs.append(GitModifier.format(obj))
        
        for chunk in chunks(envs, args.range):
            emit_logger.opt(ansi=True).debug(
                GitModifier.filter_branch(args.path, f"'{''.join(chunk)}' -- --all",args.verbose))
        emit_logger.info('finished.')
