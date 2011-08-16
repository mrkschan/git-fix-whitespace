#!/usr/bin/env python
from git import Repo
from git.cmd import Git


def main():
    git_exec = Git()
    output = git_exec.rev_parse('--show-toplevel', with_extended_output=True,
                                with_exceptions=False)
    err_no, git_root, err_msg = output
    if err_no:
        print err_msg
        return

    git_repo = Repo(git_root)
    git_config = git_repo.config_reader()

    config_whitespace = {
        'blank-at-eol': True,
        'space-before-tab': True,
        'indent-with-non-tab': False,
        'tab-in-indent': False,
        'blank-at-eof': False,
        'trailing-space': False,
        'cr-at-eol': False,
        'tabwidth=<n>': False,  # not supported yet
    }
    try:
        _config_whitespace = git_config.get('core', 'whitespace')
    except:
        _config_whitespace = ''
    for c in _config_whitespace.split(','):
        c = c.strip()

        if c[0] == '-':
            config_whitespace[c[1:]] = False
        else:
            config_whitespace[c] = True

    print config_whitespace


if __name__ == '__main__':
    main()
