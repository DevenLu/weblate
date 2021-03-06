# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2020 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""Tests for quality checks."""

from __future__ import unicode_literals

from weblate.checks.format import (
    CFormatCheck,
    CSharpFormatCheck,
    JavaFormatCheck,
    JavaMessageFormatCheck,
    PerlFormatCheck,
    PHPFormatCheck,
    PythonBraceFormatCheck,
    PythonFormatCheck,
)
from weblate.checks.qt import QtFormatCheck, QtPluralCheck
from weblate.checks.ruby import RubyFormatCheck
from weblate.checks.tests.test_checks import CheckTestCase, MockUnit
from weblate.lang.models import Language
from weblate.trans.models import Translation, Unit
from weblate.trans.tests.test_views import FixtureTestCase


class PythonFormatCheckTest(CheckTestCase):
    check = PythonFormatCheck()

    def setUp(self):
        super(PythonFormatCheckTest, self).setUp()
        self.test_highlight = (
            'python-format',
            '%sstring%d',
            [(0, 2, u'%s'), (8, 10, u'%d')],
        )

    def test_no_format(self):
        self.assertFalse(self.check.check_format('strins', 'string', False))

    def test_format(self):
        self.assertFalse(self.check.check_format('%s string', '%s string', False))

    def test_space_format(self):
        self.assertTrue(self.check.check_format('%d % string', '%d % other', False))

    def test_percent_format(self):
        self.assertFalse(self.check.check_format('%d%% string', '%d%% string', False))
        self.assertTrue(self.check.check_format('12%% string', '12% string', False))
        self.assertTrue(self.check.check_format('Save 12%%.', 'Save 12%.', False))

    def test_named_format(self):
        self.assertFalse(
            self.check.check_format('%(name)s string', '%(name)s string', False)
        )

    def test_missing_format(self):
        self.assertTrue(self.check.check_format('%s string', 'string', False))

    def test_missing_named_format(self):
        self.assertTrue(self.check.check_format('%(name)s string', 'string', False))

    def test_missing_named_format_ignore(self):
        self.assertFalse(self.check.check_format('%(name)s string', 'string', True))

    def test_wrong_format(self):
        self.assertTrue(self.check.check_format('%s string', '%c string', False))

    def test_reordered_format(self):
        self.assertTrue(self.check.check_format('%s %d string', '%d %s string', False))

    def test_wrong_named_format(self):
        self.assertTrue(
            self.check.check_format('%(name)s string', '%(jmeno)s string', False)
        )

    def test_reordered_named_format(self):
        self.assertFalse(
            self.check.check_format(
                '%(name)s %(foo)s string', '%(foo)s %(name)s string', False
            )
        )

    def test_reordered_named_format_long(self):
        self.assertFalse(
            self.check.check_format(
                '%(count)d strings into %(languages)d languages %(percent)d%%',
                '%(languages)d dil içinde %(count)d satır %%%(percent)d',
                False,
            )
        )


class PHPFormatCheckTest(CheckTestCase):
    check = PHPFormatCheck()

    def setUp(self):
        super(PHPFormatCheckTest, self).setUp()
        self.test_highlight = (
            'php-format',
            '%sstring%d',
            [(0, 2, u'%s'), (8, 10, u'%d')],
        )

    def test_no_format(self):
        self.assertFalse(self.check.check_format('strins', 'string', False))

    def test_format(self):
        self.assertFalse(self.check.check_format('%s string', '%s string', False))

    def test_named_format(self):
        self.assertFalse(self.check.check_format('%1$s string', '%1$s string', False))

    def test_missing_format(self):
        self.assertTrue(self.check.check_format('%s string', 'string', False))

    def test_missing_named_format(self):
        self.assertTrue(self.check.check_format('%1$s string', 'string', False))

    def test_missing_named_format_ignore(self):
        self.assertFalse(self.check.check_format('%1$s string', 'string', True))

    def test_wrong_format(self):
        self.assertTrue(self.check.check_format('%s string', '%c string', False))

    def test_double_format(self):
        self.assertTrue(self.check.check_format('%s string', '%s%s string', False))

    def test_reorder_format(self):
        self.assertFalse(
            self.check.check_format('%1$s %2$s string', '%2$s %1$s string', False)
        )

    def test_wrong_named_format(self):
        self.assertTrue(self.check.check_format('%1$s string', '%s string', False))

    def test_wrong_percent_format(self):
        self.assertTrue(self.check.check_format('%s%% (0.1%%)', '%s%% (0.1%x)', False))

    def test_missing_percent_format(self):
        self.assertTrue(self.check.check_format('%s%% %%', '%s%% percent', False))

    def test_space_format(self):
        self.assertTrue(self.check.check_format('%d % string', '%d % other', False))


class CFormatCheckTest(CheckTestCase):
    check = CFormatCheck()
    flag = 'c-format'

    def setUp(self):
        super(CFormatCheckTest, self).setUp()
        self.test_highlight = (self.flag, '%sstring%d', [(0, 2, u'%s'), (8, 10, u'%d')])

    def test_no_format(self):
        self.assertFalse(self.check.check_format('strins', 'string', False))

    def test_format(self):
        self.assertFalse(self.check.check_format('%s string', '%s string', False))

    def test_named_format(self):
        self.assertFalse(self.check.check_format('%10s string', '%10s string', False))

    def test_missing_format(self):
        self.assertTrue(self.check.check_format('%s string', 'string', False))

    def test_missing_named_format(self):
        self.assertTrue(self.check.check_format('%10s string', 'string', False))

    def test_missing_named_format_ignore(self):
        self.assertFalse(self.check.check_format('%10s string', 'string', True))

    def test_wrong_format(self):
        self.assertTrue(self.check.check_format('%s string', '%c string', False))

    def test_wrong_named_format(self):
        self.assertTrue(self.check.check_format('%10s string', '%20s string', False))

    def test_reorder_format(self):
        self.assertFalse(
            self.check.check_format('%1$s %2$s string', '%2$s %1$s string', False)
        )

    def test_locale_delimiter(self):
        self.assertFalse(
            self.check.check_format('lines: %6.3f', 'radky: %\'6.3f', False)
        )

    def test_ld_format(self):
        self.assertFalse(
            self.check.check_format(
                '%ld bytes (free %ld bytes, used %ld bytes)',
                '%l octets (%l octets libres, %l octets utilisés)',
                True,
            )
        )

    def test_parenthesis(self):
        self.assertFalse(self.check.check_format('(%.0lf%%)', '(%%%.0lf)', False))


class PerlFormatCheckTest(CFormatCheckTest):
    check = PerlFormatCheck()
    flag = 'perl-format'


class PythonBraceFormatCheckTest(CheckTestCase):
    check = PythonBraceFormatCheck()

    def setUp(self):
        super(PythonBraceFormatCheckTest, self).setUp()
        self.test_highlight = (
            'python-brace-format',
            '{0}string{1}',
            [(0, 3, u'{0}'), (9, 12, u'{1}')],
        )

    def test_no_format(self):
        self.assertFalse(self.check.check_format('strins', 'string', False))

    def test_position_format(self):
        self.assertFalse(self.check.check_format('{} string {}', '{} string {}', False))

    def test_wrong_position_format(self):
        self.assertTrue(self.check.check_format('{} string', '{} string {}', False))

    def test_named_format(self):
        self.assertFalse(
            self.check.check_format('{s1} string {s2}', '{s1} string {s2}', False)
        )

    def test_missing_format(self):
        self.assertTrue(self.check.check_format('{} string', 'string', False))

    def test_missing_named_format(self):
        self.assertTrue(self.check.check_format('{s1} string', 'string', False))

    def test_missing_named_format_ignore(self):
        self.assertFalse(self.check.check_format('{s} string', 'string', True))

    def test_wrong_format(self):
        self.assertTrue(self.check.check_format('{s} string', '{c} string', False))

    def test_escaping(self):
        self.assertFalse(self.check.check_format('{{ string }}', 'string', False))

    def test_attribute_format(self):
        self.assertFalse(
            self.check.check_format('{s.foo} string', '{s.foo} string', False)
        )

    def test_wrong_attribute_format(self):
        self.assertTrue(
            self.check.check_format('{s.foo} string', '{s.bar} string', False)
        )


class CSharpFormatCheckTest(CheckTestCase):
    check = CSharpFormatCheck()

    def setUp(self):
        super(CSharpFormatCheckTest, self).setUp()
        self.test_highlight = (
            'c-sharp-format',
            '{0}string{1}',
            [(0, 3, u'{0}'), (9, 12, u'{1}')],
        )

    def test_no_format(self):
        self.assertFalse(self.check.check_format('strins', 'string', False))

    def test_escaping_no_position(self):
        self.assertFalse(self.check.check_format('{{ string }}', 'string', False))

    def test_simple_format(self):
        self.assertFalse(self.check.check_format('{0} strins', '{0} string', False))

    def test_format_with_width(self):
        self.assertFalse(self.check.check_format('{0,1} strins', '{0,1} string', False))

    def test_format_with_flag(self):
        self.assertFalse(
            self.check.check_format('{0:C2} strins', '{0:C2} string', False)
        )

    def test_full_format(self):
        self.assertFalse(
            self.check.check_format('{0,1:N0} strins', '{0,1:N0} string', False)
        )

    def test_missing_format(self):
        self.assertTrue(self.check.check_format('{0} strins', 'string', False))

    def test_missing_width_format(self):
        self.assertTrue(self.check.check_format('{0,1} strins', 'string', False))

    def test_missing_flag_format(self):
        self.assertTrue(self.check.check_format('{0:C1} strins', 'string', False))

    def test_missing_full_format(self):
        self.assertTrue(self.check.check_format('{0,1:C3} strins', 'string', False))

    def test_wrong_format(self):
        self.assertTrue(self.check.check_format('{0} string', '{1} string', False))

    def test_missing_named_format_ignore(self):
        self.assertFalse(self.check.check_format('{0} string', 'string', True))

    def test_escaping_with_position(self):
        self.assertFalse(self.check.check_format('{{ 0 }}', 'string', False))

    def test_wrong_attribute_format(self):
        self.assertTrue(self.check.check_format('{0} string', '{1} string', False))

    def test_reordered_format(self):
        self.assertFalse(
            self.check.check_format('{0} string {1}', '{1} string {0}', False)
        )


class JavaFormatCheckTest(CheckTestCase):
    check = JavaFormatCheck()

    def setUp(self):
        super(JavaFormatCheckTest, self).setUp()
        self.test_highlight = (
            'java-format',
            '%1s string %2s',
            [(0, 3, u'%1s'), (11, 14, u'%2s')],
        )

    def test_no_format(self):
        self.assertFalse(self.check.check_format('strins', 'string', False))

    def test_escaping(self):
        self.assertFalse(self.check.check_format('%% s %%', 'string', False))

    def test_format(self):
        self.assertFalse(self.check.check_format('%s string', '%s string', False))

    def test_time_format(self):
        self.assertFalse(self.check.check_format('%1$tH strins', '%1$tH string', False))

    def test_wrong_position_format(self):
        self.assertTrue(self.check.check_format('%s string', '%s string %s', False))

    def test_named_format(self):
        self.assertFalse(
            self.check.check_format('%1s string %2s', '%1s string %2s', False)
        )

    def test_missing_format(self):
        self.assertTrue(self.check.check_format('%1s string', 'string', False))

    def test_missing_named_format(self):
        self.assertTrue(self.check.check_format('%1$05d string', 'string', False))

    def test_wrong_argument_format(self):
        self.assertTrue(self.check.check_format('%1s string', '%2s string', False))

    def test_wrong_format(self):
        self.assertTrue(self.check.check_format('%s strins', '%d string', False))

    def test_missing_named_format_ignore(self):
        self.assertFalse(self.check.check_format('%1s string', 'string', True))

    def test_reordered_format(self):
        self.assertTrue(
            self.check.check_format('%1s string %2d', '%2d string %1s', False)
        )


class JavaMessageFormatCheckTest(CheckTestCase):
    check = JavaMessageFormatCheck()

    def setUp(self):
        super(JavaMessageFormatCheckTest, self).setUp()
        self.test_highlight = (
            'java-messageformat',
            '{0}string{1}',
            [(0, 3, u'{0}'), (9, 12, u'{1}')],
        )

    def test_no_format(self):
        self.assertFalse(self.check.check_format('strins', 'string', False))

    def test_escaping_no_position(self):
        self.assertFalse(self.check.check_format('{{ string }}', 'string', False))

    def test_simple_format(self):
        self.assertFalse(self.check.check_format('{0} strins', '{0} string', False))

    def test_format_with_width(self):
        self.assertFalse(self.check.check_format('{0,1} strins', '{0,1} string', False))

    def test_format_with_flag(self):
        self.assertFalse(
            self.check.check_format('{0:C2} strins', '{0:C2} string', False)
        )

    def test_full_format(self):
        self.assertFalse(
            self.check.check_format('{0,1:N0} strins', '{0,1:N0} string', False)
        )

    def test_missing_format(self):
        self.assertTrue(self.check.check_format('{0} strins', 'string', False))

    def test_missing_type_format(self):
        self.assertTrue(self.check.check_format('{0,number} strins', 'string', False))

    def test_missing_flag_format(self):
        self.assertTrue(self.check.check_format('{0} strins', 'string', False))

    def test_missing_full_format(self):
        self.assertTrue(
            self.check.check_format('{0,number,integer} strins', 'string', False)
        )

    def test_wrong_format(self):
        self.assertTrue(self.check.check_format('{0} string', '{1} string', False))

    def test_missing_named_format_ignore(self):
        self.assertFalse(self.check.check_format('{0} string', 'string', True))

    def test_escaping_with_position(self):
        self.assertFalse(self.check.check_format('{{ 0 }}', 'string', False))

    def test_wrong_attribute_format(self):
        self.assertTrue(self.check.check_format('{0} string', '{1} string', False))

    def test_reordered_format(self):
        self.assertFalse(
            self.check.check_format('{0} string {1}', '{1} string {0}', False)
        )

    def test_skip(self):
        unit = MockUnit(source='source')
        self.assertTrue(self.check.should_skip(unit))
        unit = MockUnit(source='source', flags='java-messageformat')
        self.assertFalse(self.check.should_skip(unit))
        unit = MockUnit(source='source', flags='auto-java-messageformat')
        self.assertTrue(self.check.should_skip(unit))
        unit = MockUnit(source='{0}', flags='auto-java-messageformat')
        self.assertFalse(self.check.should_skip(unit))

    def test_quotes(self):
        self.assertFalse(
            self.check.check_format('{0} string {1}', "'{1}' strin''g '{0}'", False)
        )
        self.assertTrue(
            self.check.check_format('{0} string {1}', "'{1}' strin''g '{0}", False)
        )
        self.assertTrue(
            self.check.check_format('{0} string {1}', "'{1}' strin'g '{0}'", False)
        )


class QtFormatCheckTest(CheckTestCase):
    check = QtFormatCheck()
    flag = 'qt-format'

    def setUp(self):
        super(QtFormatCheckTest, self).setUp()
        self.test_highlight = (self.flag, '%1string%2', [(0, 2, u'%1'), (8, 10, u'%2')])

    def test_no_format(self):
        self.assertFalse(self.check.check_format('strins', 'string', False))

    def test_simple_format(self):
        self.assertFalse(self.check.check_format('%1 strins', '%1 string', False))

    def test_missing_format(self):
        self.assertTrue(self.check.check_format('%1 strins', 'string', False))

    def test_wrong_format(self):
        self.assertTrue(self.check.check_format('%1 string', '%2 string', False))

    def test_reordered_format(self):
        self.assertFalse(self.check.check_format('%1 string %2', '%2 string %1', False))

    def test_reused_format(self):
        self.assertFalse(self.check.check_format('%1 string %1', '%1 string %1', False))


class QtPluralCheckTest(CheckTestCase):
    check = QtPluralCheck()
    flag = 'qt-plural-format'

    def setUp(self):
        super(QtPluralCheckTest, self).setUp()
        self.test_highlight = (self.flag, '%Lnstring', [(0, 3, u'%Ln')])

    def test_no_format(self):
        self.assertFalse(self.check.check_format('strins', 'string', False))

    def test_plural_format(self):
        self.assertFalse(self.check.check_format('%n string(s)', '%n string', False))

    def test_plural_localized_format(self):
        self.assertFalse(self.check.check_format('%Ln string(s)', '%Ln string', False))

    def test_missing_format(self):
        self.assertTrue(self.check.check_format('%n string(s)', 'string', False))


class RubyFormatCheckTest(CheckTestCase):
    check = RubyFormatCheck()
    flag = 'ruby-format'

    def setUp(self):
        super(RubyFormatCheckTest, self).setUp()

    def test_check_highlight(self):
        self.test_highlight = (self.flag, '%dstring%s', [(0, 2, u'%d'), (8, 10, u'%s')])
        super(RubyFormatCheckTest, self).test_check_highlight()

    def test_check_highlight_named(self):
        self.test_highlight = (
            self.flag,
            '%<int>dstring%<str>s',
            [(0, 7, u'%<int>d'), (13, 20, u'%<str>s')],
        )
        super(RubyFormatCheckTest, self).test_check_highlight()

    def test_check_highlight_named_template(self):
        self.test_highlight = (
            self.flag,
            '%{int}string%{str}',
            [(0, 6, u'%{int}'), (12, 18, u'%{str}')],
        )
        super(RubyFormatCheckTest, self).test_check_highlight()

    def test_check_highlight_complex_named_template(self):
        self.test_highlight = (
            self.flag,
            '%8.8{foo}string%+08.2<float>fstring',
            [(0, 9, u'%8.8{foo}'), (15, 29, u'%+08.2<float>f')],
        )
        super(RubyFormatCheckTest, self).test_check_highlight()

    def test_no_format(self):
        self.assertFalse(self.check.check_format('strins', 'string', False))

    def test_format(self):
        self.assertFalse(self.check.check_format('%s string', '%s string', False))

    def test_space_format(self):
        self.assertTrue(self.check.check_format('%d % string', '%d % other', False))

    def test_percent_format(self):
        self.assertFalse(self.check.check_format('%d%% string', '%d%% string', False))

    def test_named_format(self):
        self.assertFalse(
            self.check.check_format('%<name>s string', '%<name>s string', False)
        )

    def test_missing_format(self):
        self.assertTrue(self.check.check_format('%s string', 'string', False))

    def test_missing_named_format(self):
        self.assertTrue(self.check.check_format('%<name>s string', 'string', False))

    def test_missing_named_format_ignore(self):
        self.assertFalse(self.check.check_format('%<name>s string', 'string', True))

    def test_wrong_format(self):
        self.assertTrue(self.check.check_format('%s string', '%c string', False))

    def test_reordered_format(self):
        self.assertTrue(self.check.check_format('%s %d string', '%d %s string', False))

    def test_wrong_named_format(self):
        self.assertTrue(
            self.check.check_format('%<name>s string', '%<jmeno>s string', False)
        )

    def test_reordered_named_format(self):
        self.assertFalse(
            self.check.check_format(
                '%<name>s %<foo>s string', '%<foo>s %<name>s string', False
            )
        )

    def test_reordered_named_format_long(self):
        self.assertFalse(
            self.check.check_format(
                '%<count>d strings into %<languages>d languages %<percent>d%%',
                '%<languages>d dil içinde %<count>d satır %%%<percent>d',
                False,
            )
        )

    def test_formatting_named_format(self):
        self.assertFalse(
            self.check.check_format('%+08.2<foo>f string', '%+08.2<foo>f string', False)
        )

    def test_missing_named_template_format(self):
        self.assertTrue(self.check.check_format('%{name} string', 'string', False))

    def test_missing_named_template_format_ignore(self):
        self.assertFalse(self.check.check_format('%{name} string', 'string', True))

    def test_wrong_named_template_format(self):
        self.assertTrue(
            self.check.check_format('%{name} string', '%{jmeno} string', False)
        )

    def test_reordered_named_template_format(self):
        self.assertFalse(
            self.check.check_format(
                '%{name} %{foo} string', '%{foo} %{name} string', False
            )
        )

    def test_formatting_named_template_format(self):
        self.assertFalse(
            self.check.check_format('%8.8{foo} string', '%8.8{foo} string', False)
        )

    def test_reordered_named_template_format_long(self):
        self.assertFalse(
            self.check.check_format(
                '%{count} strings into %{languages} languages %{percent}%%',
                '%{languages} dil içinde %{count} satır %%%{percent}',
                False,
            )
        )


class PluralTest(FixtureTestCase):
    check = PythonFormatCheck()

    def test_arabic(self):
        arabic = Language.objects.get(code='ar')
        translation = Translation(language=arabic, plural=arabic.plural)
        unit = Unit(translation=translation)
        # Singular, correct format string
        self.assertFalse(self.check.check_target_unit(['hello %s'], ['hell %s'], unit))
        # Singular, missing format string
        self.assertTrue(self.check.check_target_unit(['hello %s'], ['hell'], unit))
        # Plural, correct format string
        self.assertFalse(
            self.check.check_target_unit(['hello %s'] * 2, ['hell %s'] * 6, unit)
        )
        # Plural, missing format string
        self.assertTrue(
            self.check.check_target_unit(['hello %s'] * 2, ['hell'] * 6, unit)
        )
        # Plural, correct format string (missing on single value plurals)
        self.assertFalse(
            self.check.check_target_unit(
                ['hello %s'] * 2, ['hell'] * 3 + ['hello %s'] * 3, unit
            )
        )
        # Plural, missing format string on multi value plural
        self.assertTrue(
            self.check.check_target_unit(
                ['hello %s'] * 2, ['hell'] * 4 + ['hello %s'] * 2, unit
            )
        )
