#!/usr/bin/env python
import itertools
import os
import re
import sys

from git import Repo
from git.cmd import Git


LINE_INFO_REGEX = re.compile(r'\+(\d+),(\d+)')
PATH_INFO_REGEX = re.compile(r'b/(.+)')


def blank_at_eol_sanitizer(line):
    return line.rstrip(' ')


def space_before_tab_sanitizer(line):
    #TODO: implement this
    return line


def indent_with_non_tab_sanitizer(line):
    #TODO: implement this
    return line


def tab_in_indent_sanitizer(line):
    #TODO: implement this
    return line


def blank_at_eof_sanitizer(line):
    #TODO: implement this
    return line


def cr_at_eol_sanitizer(line):
    #TODO: implement this
    return line


def sanitize_line(line, sanitizers):
    return reduce(lambda a, b: b(a), sanitizers, line)


def sanitize_diff(git_diff, git_root, sanitizers):
    '''Sanitize lines in diff

    Only files add or modify are sanitized.
    '''
    if git_diff.deleted_file or git_diff.renamed:
        #TODO: Verify this checker
        return

    _patch = git_diff.diff.split('\n')
    file_path_info = _patch[1]
    patch = _patch[2:]

    m = PATH_INFO_REGEX.search(file_path_info)
    if not m:
        # Cannot find file path of working file
        return

    file_path = os.path.join(git_root, m.group(1))
    backup_path = '%s.orig' % file_path

    line_changes = {}  # line no. -> sanitized line
    for line in patch:
        if line.startswith('@@'):
            m = LINE_INFO_REGEX.search(line)
            if not m:
                # Cannot find line_start, line_count
                return
            line_start, line_count = m.group(1), m.group(2)
            line_no = int(line_start)
        elif line.startswith('+'):
            line_changes[line_no] = sanitize_line(line[1:], sanitizers) + '\n'
            line_no += 1
        elif line.startswith(' '):
            line_changes[line_no] = line[1:] + '\n'
            line_no += 1

    os.rename(file_path, backup_path)
    raw_fileobj = open(backup_path, 'rb')
    working_fd = os.open(file_path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
                         os.fstat(raw_fileobj.fileno()).st_mode)
    working_fileobj = os.fdopen(working_fd, 'wb')

    line_no = 1
    for line in raw_fileobj:
        working_fileobj.write(line_changes.get(line_no, line))
        line_no += 1

    raw_fileobj.close()
    working_fileobj.close()


def main():
    git_exec = Git()
    output = git_exec.rev_parse('--show-toplevel', with_extended_output=True,
                                with_exceptions=False)
    err_no, git_root, err_msg = output
    if err_no:
        print >> sys.stderr, err_msg
        sys.exit(1)

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
        for c in _config_whitespace.split(','):
            c = c.strip()

            if c[0] == '-':
                config_whitespace[c[1:]] = False
            else:
                config_whitespace[c] = True
    except:
        pass

    sanitizers = []
    if config_whitespace.get('trailing-space', False):
        config_whitespace['blank-at-eol'] = True
        config_whitespace['blank-at-eof'] = True
    if config_whitespace.get('blank-at-eol', False):
        sanitizers.append(blank_at_eol_sanitizer)
    if config_whitespace.get('space-before-tab', False):
        sanitizers.append(space_before_tab_sanitizer)
    if config_whitespace.get('indent-with-non-tab', False):
        sanitizers.append(indent_with_non_tab_sanitizer)
    if config_whitespace.get('tab-in-indent', False):
        sanitizers.append(tab_in_indent_sanitizer)
    if config_whitespace.get('blank-at-eof', False):
        sanitizers.append(blank_at_eof_sanitizer)
    if config_whitespace.get('cr-at-eol', False):
        sanitizers.append(cr_at_eol_sanitizer)

    head_diff = git_repo.head.commit.diff(create_patch=True)
    head_diff_add = head_diff.iter_change_type('A')
    head_diff_modify = head_diff.iter_change_type('M')

    map(lambda i: sanitize_diff(i, git_root, sanitizers),
        itertools.chain(head_diff_add, head_diff_modify))


if __name__ == '__main__':
    main()
