import git_fix_whitespace as gfws


def test_blank_at_eol_sanitizer():
    before = ''
    after = ''
    now = gfws.blank_at_eol_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = ' '
    after = ''
    now = gfws.blank_at_eol_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '     '
    after = ''
    now = gfws.blank_at_eol_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = 'abc def'
    after = 'abc def'
    now = gfws.blank_at_eol_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = 'abc def '
    after = 'abc def'
    now = gfws.blank_at_eol_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = 'abc def    '
    after = 'abc def'
    now = gfws.blank_at_eol_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)


def test_space_before_tab_sanitizer():
    # NOTE: The defaut TAB_WIDTH is 8.
    before = ''
    after = ''
    now = gfws.space_before_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = ' '
    after = ' '
    now = gfws.space_before_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '  	'
    after = '  	'
    now = gfws.space_before_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '  	 '
    after = '  	 '
    now = gfws.space_before_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = 'abc'
    after = 'abc'
    now = gfws.space_before_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = ' 	abc'
    after = '        abc'
    now = gfws.space_before_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = 'abc	efg'
    after = 'abc	efg'
    now = gfws.space_before_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '	abc'
    after = '	abc'
    now = gfws.space_before_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '	  abc'
    after = '	  abc'
    now = gfws.space_before_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)


def test_indent_with_non_tab_sanitizer():
    # NOTE: The defaut TAB_WIDTH is 8.
    before = ''
    after = ''
    now = gfws.indent_with_non_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = ' '
    after = ' '
    now = gfws.indent_with_non_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '  	'
    after = '  	'
    now = gfws.indent_with_non_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = 'abc'
    after = 'abc'
    now = gfws.indent_with_non_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = ' abc'
    after = '	abc'
    now = gfws.indent_with_non_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '	abc'
    after = '	abc'
    now = gfws.indent_with_non_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = ' 	abc'
    after = '	abc'
    now = gfws.indent_with_non_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '	        abc'
    after = '		abc'
    now = gfws.indent_with_non_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '	          	 abc'
    after = '				abc'
    now = gfws.indent_with_non_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = 'abc	efg'
    after = 'abc	efg'
    now = gfws.indent_with_non_tab_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)


def test_tab_in_indent_sanitizer():
    # NOTE: The defaut TAB_WIDTH is 8.
    before = ''
    after = ''
    now = gfws.tab_in_indent_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = ' '
    after = ' '
    now = gfws.tab_in_indent_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '  	'
    after = '  	'
    now = gfws.tab_in_indent_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = 'abc'
    after = 'abc'
    now = gfws.tab_in_indent_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = ' abc'
    after = ' abc'
    now = gfws.tab_in_indent_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '	abc'
    after = '        abc'
    now = gfws.tab_in_indent_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = ' 	abc'
    after = '        abc'
    now = gfws.tab_in_indent_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '	        abc'
    after = '                abc'
    now = gfws.tab_in_indent_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = '	          	abc'
    after = '                        abc'
    now = gfws.tab_in_indent_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)

    before = 'abc	efg'
    after = 'abc	efg'
    now = gfws.tab_in_indent_sanitizer(before)
    assert now == after, \
           'before: "%s", after: "%s", now: "%s"' % (before, after, now)
