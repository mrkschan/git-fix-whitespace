#!/usr/bin/env python
import argparse
import ast
import itertools
import os
import re
import sys

from git import Repo
from git.cmd import Git


LINE_INFO_REGEX = re.compile(r'\+(\d+),(\d+)')
PATH_INFO_REGEX = re.compile(r'b/(.+)')

LEADING_WS_REGEX = re.compile(r'^(\s+)([^\s]+)$')
SPACE_BEFORE_TAB_REGEX = re.compile(r' +\t+')

TAB_WIDTH = 8


def blank_at_eol_sanitizer(line):
    '''Remove trailing whitespaces'''
    return line.rstrip(' ')


def space_before_tab_sanitizer(line):
    '''Expand non-leading tab characters to whitespaces

    This sanitizer applies to tab characters used in indentation only. It does
    not apply to lines with spacing characters only.
    '''
    m = LEADING_WS_REGEX.match(line)
    if not m:
        return line

    leading = m.group(1)
    trailing = m.group(2)

    m = SPACE_BEFORE_TAB_REGEX.match(leading)
    if not m:
        return line

    return leading.expandtabs(TAB_WIDTH) + trailing


def indent_with_non_tab_sanitizer(line):
    '''Change whitespaces to tab characters according to the TAB_WIDTH setting

    This sanitizer applies to whitespaces used in indentation only. It does
    not apply to lines with spacing characters only.
    '''
    m = LEADING_WS_REGEX.match(line)
    if not m:
        return line

    leading = m.group(1)
    trailing = m.group(2)

    if not ' ' in leading:
        return line

    spaces = 0
    tabs = 0
    for ws in leading:
        if ws == ' ':
            spaces += 1
        if ws == '\t':
            spaces = 0
            tabs += 1
        if spaces == TAB_WIDTH:
            spaces = 0
            tabs += 1
    if spaces > 0:
        tabs += 1

    return '\t' * tabs + trailing


def tab_in_indent_sanitizer(line):
    '''Change tab characters to whitespaces according to the TAB_WIDTH setting

    This sanitizer applies to tab characters used in indentation only. It does
    not apply to lines with spacing characters only.
    '''
    m = LEADING_WS_REGEX.match(line)
    if not m:
        return line

    leading = m.group(1)
    trailing = m.group(2)

    if not '\t' in leading:
        return line

    return leading.expandtabs(TAB_WIDTH) + trailing


def blank_at_eof_sanitizer(line):
    #TODO: implement this
    return line


def cr_at_eol_sanitizer(line):
    '''Remove any trailing <CR> character(s)'''
    return line.rstrip('\r')


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
    global TAB_WIDTH

    git_exec = Git()
    output = git_exec.rev_parse('--show-toplevel', with_extended_output=True,
                                with_exceptions=False)
    err_no, git_root, err_msg = output
    if err_no:
        print >> sys.stderr, err_msg
        sys.exit(1)

    git_repo = Repo(git_root)
    git_config = git_repo.config_reader()

    ws_config = {
        'blank-at-eol': True,
        'space-before-tab': True,
        'indent-with-non-tab': False,
        'tab-in-indent': False,
        'blank-at-eof': False,
        'trailing-space': False,
        'cr-at-eol': False,
    }
    try:
        _config_whitespace = git_config.get('core', 'whitespace')
        for c in _config_whitespace.split(','):
            c = c.strip()

            if 'tabwidth' in c:
                ws_config['tabwidth'] = int(c.split('=').pop())
            else:
                if c[0] == '-':  # e.g. -tab-in-indent
                    ws_config[c[1:]] = False
                else:
                    ws_config[c] = True
    except:
        pass

    if ws_config.get('tab-in-indent', False) and \
       ws_config.get('indent-with-non-tab', False):
        print >> sys.stderr, \
                 'Cannot enforce both tab-in-indent and indent-with-non-tab.'
        sys.exit(1)

    TAB_WIDTH = ws_config.get('tabwidth')
    sanitizers = []

    if ws_config.get('trailing-space', False):
        ws_config['blank-at-eol'] = True
        ws_config['blank-at-eof'] = True

    # Allow overrides gitconfig by cli argument
    arg_parser = argparse.ArgumentParser()
    arg_parser.set_defaults(**ws_config)

    arg_parser.add_argument('--trailing-space', dest='trailing-space',
                            type=ast.literal_eval, metavar='True|False',
                            help='trailing-space is a short-hand to cover '
                                 'both blank-at-eol and blank-at-eof')
    arg_parser.add_argument('--blank-at-eol', dest='blank-at-eol',
                            type=ast.literal_eval, metavar='True|False',
                            help='treats trailing whitespaces at the end of '
                                 'the line as an error')
    arg_parser.add_argument('--space-before-tab', dest='space-before-tab',
                            type=ast.literal_eval, metavar='True|False',
                            help='treats a space character that appears '
                                 'immediately before a tab character in the '
                                 'initial indent part of the line as an error')
    arg_parser.add_argument('--indent-with-non-tab',
                            dest='indent-with-non-tab',
                            type=ast.literal_eval, metavar='True|False',
                            help='treats a line that is indented with 8 or '
                                 'more space characters as an error')
    arg_parser.add_argument('--tab-in-indent', dest='tab-in-indent',
                            type=ast.literal_eval, metavar='True|False',
                            help='treats a tab character in the initial '
                                 'indent part of the line as an error')
#    arg_parser.add_argument('--blank-at-eof', dest='blank-at-eof',
#                            type=ast.literal_eval, metavar='True|False',
#                            help='treats blank lines added at the end of '
#                                 'file as an error')
    arg_parser.add_argument('--cr-at-eol', dest='cr-at-eol',
                            type=ast.literal_eval, metavar='True|False',
                            help='treats a carriage-return at the end of '
                                 'line as part of the line terminator, i.e. '
                                 'with it, trailing-space does not trigger '
                                 'if the character before such a '
                                 'carriage-return is not a whitespace')
    arg_parser.add_argument('--tabwidth', type=int, metavar='',
                            help='tells how many character positions a tab '
                                 'occupies; this is relevant for '
                                 'indent-with-non-tab and when git fixes '
                                 'tab-in-indent errors. The default tab '
                                 'width is 8.')

    args = arg_parser.parse_args()
    ws_config = vars(args)

    # Prepare appropriate sanitizers
    if ws_config.get('blank-at-eol', False):
        sanitizers.append(blank_at_eol_sanitizer)

    if ws_config.get('space-before-tab', False):
        sanitizers.append(space_before_tab_sanitizer)

    if ws_config.get('indent-with-non-tab', False):
        sanitizers.append(indent_with_non_tab_sanitizer)

    if ws_config.get('tab-in-indent', False):
        sanitizers.append(tab_in_indent_sanitizer)

#    if ws_config.get('blank-at-eof', False):
#        sanitizers.append(blank_at_eof_sanitizer)

    if ws_config.get('cr-at-eol', False):
        sanitizers.append(cr_at_eol_sanitizer)

    head_diff = git_repo.head.commit.diff(create_patch=True)
    head_diff_add = head_diff.iter_change_type('A')
    head_diff_modify = head_diff.iter_change_type('M')

    map(lambda i: sanitize_diff(i, git_root, sanitizers),
        itertools.chain(head_diff_add, head_diff_modify))


if __name__ == '__main__':
    main()
