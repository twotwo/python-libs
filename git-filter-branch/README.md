# README

## Reference for development

- [GitPython](https://github.com/gitpython-developers/GitPython)/[Documentation](https://gitpython.readthedocs.io/en/stable/) // only for read
- [git-filter-branch](https://git-scm.com/docs/git-filter-branch) // modify by `git filter-branch`
- [commit information](https://git-scm.com/docs/git-commit-tree#_commit_information) //modify info in `git filter-branch`
- build images: `docker build --network=host -t git-filter-branch .`

## Usage

### Depandancy
Mac/Unix/Linux with Docker installed

download [modifier.sh](./modifier.sh) &

`chmod +x modifier.sh`

### 导出 commits

`./modifier.sh export {git-repo-path}` 或者

`ops=--verbose ./modifier.sh export {git-repo-path}` 用来显示执行过程详情

```bash
./modifier.sh export /tmp/docking-toolbox 
export commit log as ./commits.json file ...
2019-09-18 11:10:08.815 | INFO     | __main__:<module>:94 - [/var/lib/repo] begin export ...
2019-09-18 11:10:09.386 | INFO     | __main__:<module>:111 - write to /var/run/repo/commits.json
# commits.json is in current folder
```

### 根据修订好的提交记录更新 commits

`./modifier.sh modify {git-repo-path} {commit-json-file}`  或者

`ops="--verbose -r 100" ./modifier.sh modify {git-repo-path} {commit-json-file}` 用来显示执行过程详情，指定每次更新的行数(默认20条)


```bash
# modify commits in ok.json
ops=" -r 1" ./modifier.sh modify /tmp/docking-toolbox ok.json 
modify commit logs ...
2019-09-18 13:58:00.830 | INFO     | __main__:<module>:114 - read config [/var/run/repo/ok.json]...
2019-09-18 13:58:00.848 | INFO     | __main__:<module>:123 - begin filter-branch ...
Rewrite 1d0f6da27f644a7a610d068a64e654058f23ce43 (45/1215) (8 seconds passed, remaining 208 predicted)
...
```

### 根据邮件地址更新 commits 中的邮件地址和作者

`./modifier.sh {email-to-match} {git-repo-path} {email-change-to} {name-change-to}`


```bash
./modifier.sh li3huo@infervision.com  /tmp/docking-toolbox lyan@infervision.com liyan
Modify by Email, find li3huo@infervision.com, change to email=lyan@infervision.com, name=liyan
2019-09-18 14:17:30.957 | INFO     | __main__:<module>:148 - executing...
git -C /var/lib/repo filter-branch -f --env-filter '
    if test "$GIT_COMMITTER_EMAIL" = "li3huo@gmail.com"
    then
        GIT_AUTHOR_NAME="lyan"
        GIT_AUTHOR_EMAIL="test@gmail.com"
        GIT_COMMITTER_NAME="lyan"
        GIT_COMMITTER_EMAIL="test@gmail.com"
    fi
    ' -- --all
        
Rewrite fbf56282948f2dcb658691edd2aaf05024cf8335 (1211/1215) (235 seconds passed, remaining 0 predicted)     
WARNING: Ref 'refs/heads/master' is unchanged               # 没有修改的分支会有 warning
Ref 'refs/heads/1.4.2-WithStatusCode' was rewritten         # 成功写入的分支
```