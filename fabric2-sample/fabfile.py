from fabric import Connection, task


@task
def install_zsh(c):
    """install oh-my-zsh

    c [context](http://docs.pyinvoke.org/en/latest/api/context.html)

    https://github.com/ohmyzsh/ohmyzsh
    """
    c.run("echo $SHELL")
    # http://docs.pyinvoke.org/en/latest/api/runners.html
    if c.run("test -d ~/.oh-my-zsh", warn=True).failed:
        print("install zsh")
        c.sudo("apt install zsh -y")
        print("install oh-my-zsh")
        # c.run('sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')
        c.put("install.sh", "/tmp/install.sh")
        c.run("sh /tmp/install.sh")
    # c.sudo("chsh -s $(which zsh)", warn=True)
    if c.run("test -f ~/.zshrc", warn=True).ok:
        print(f"install on {c.config['user']}@{c.host}")

    # c.run("source ~/.zshrc", shell="/bin/zsh", env={})
    # c.run("omz theme use ys")
    # c.run("omz update")
