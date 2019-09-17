# Dev Guide

## GitPython

- [GitPython](https://github.com/gitpython-developers/GitPython)
- [Documentation](https://gitpython.readthedocs.io/en/stable/)

## Usage

`./comodifiers.sh git-repo-path [commit-json-file]`

```bash
# export git commits
./comodifiers.sh /tmp/git-modifer
export commit logs ...
2019-08-29 16:59:35.219 | INFO     | __main__:<module>:91 - [/var/lib/repo] begin export ...
# commits.json in current path
```

```bash
# after modify commits.json
./comodifiers.sh /tmp/git-modifer commits.json
export commit logs ...
2019-08-29 16:59:35.219 | INFO     | __main__:<module>:91 - [/var/lib/repo] begin export ...
2019-08-29 16:59:35.221 | ERROR    | __main__:<module>:93 - file [/var/run/repo/commits.json] exist, cancel export
modify commit logs ...
2019-08-29 16:59:37.124 | INFO     | __main__:<module>:114 - c7884648a86d359f5daac98965b18ccdca6f6090	2019-08-28 08:48:31+00:00	nsuijun1@infervision.com	Update README.md
Rewrite c7884648a86d359f5daac98965b18ccdca6f6090 (4/6) (1 seconds passed, remaining 0 predicted)
Ref 'refs/heads/master' was rewritten
...
```

`python main.py -p . -m email-to-match -e email-change-to -n name-change-to --verbose`