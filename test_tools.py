#!/usr/bin/python
from unittest import TestCase
from os.path import abspath

from editorconfig import get_properties
from editorconfig_tools.editorconfig_tools import EditorConfigChecker


def get_filename(test_file):
    return abspath('tests/{0}'.format(test_file))


class EditorConfigTestCase(TestCase):

    """Test case for EditorConfigChecker tests"""

    def assertFileErrors(self, filename, expected_errors):
        full_filename = get_filename(filename)
        props = get_properties(full_filename)
        checker = EditorConfigChecker()
        errors = checker.check(full_filename, props)
        self.assertEquals((filename, errors), (filename, expected_errors))


class LineEndingTests(EditorConfigTestCase):

    """Tests for EditorConfigChecker line endings"""

    def test_check_crlf(self):
        self.assertFileErrors('crlf_valid.txt', [])
        self.assertFileErrors('crlf_invalid_cr.txt', [
            "Final newline found",
            "Incorrect line ending found: cr",
        ])
        self.assertFileErrors('crlf_invalid_lf.txt', [
            "Final newline found",
            "Incorrect line ending found: lf",
        ])

    def test_check_cr(self):
        self.assertFileErrors('cr_valid.txt', [])
        self.assertFileErrors('cr_invalid_lf.txt', [
            "Incorrect line ending found: lf",
        ])
        self.assertFileErrors('cr_invalid_crlf.txt', [
            "Incorrect line ending found: crlf",
        ])

    def test_check_lf(self):
        self.assertFileErrors('lf_valid.txt', [])
        self.assertFileErrors('lf_invalid_cr.txt', [
            "Incorrect line ending found: cr",
        ])
        self.assertFileErrors('lf_invalid_crlf.txt', [
            "Incorrect line ending found: crlf",
            "No final newline found",
        ])


class CharsetTests(EditorConfigTestCase):

    """Tests for EditorConfigChecker charsets"""

    def test_utf8(self):
        self.assertFileErrors('utf-8_valid.txt', [])
        self.assertFileErrors('utf-8_valid_latin1.txt', [])
        self.assertFileErrors('utf-8_invalid_utf-8-bom.txt', [
            "Charset utf-8-bom found",
        ])
        self.assertFileErrors('utf-8_invalid_utf-16be.txt', [
            "Charset utf-16be found",
        ])
        self.assertFileErrors('utf-8_invalid_utf-16le.txt', [
            "Charset utf-16le found",
        ])

    def test_utf8_with_bom(self):
        self.assertFileErrors('utf-8-bom_valid.txt', [])
        self.assertFileErrors('utf-8-bom_invalid_latin1.txt', [
            "Charset utf-8 or latin1 found",
        ])
        self.assertFileErrors('utf-8-bom_invalid_utf-8.txt', [
            "Charset utf-8 or latin1 found",
        ])
        self.assertFileErrors('utf-8-bom_invalid_utf-16be.txt', [
            "Charset utf-16be found",
        ])
        self.assertFileErrors('utf-8-bom_invalid_utf-16le.txt', [
            "Charset utf-16le found",
        ])

    def test_latin1(self):
        self.assertFileErrors('latin1_valid.txt', [])
        self.assertFileErrors('latin1_invalid_utf-8.txt', [])
        self.assertFileErrors('latin1_invalid_utf-8-bom.txt', [])
        self.assertFileErrors('latin1_invalid_utf-16be.txt', [])
        self.assertFileErrors('latin1_invalid_utf-16le.txt', [])

    def test_utf16be(self):
        self.assertFileErrors('utf-16be_valid.txt', [])
        self.assertFileErrors('utf-16be_invalid_utf-16le.txt', [
            "Charset utf-16le found",
        ])
        self.assertFileErrors('utf-16be_invalid_utf-8.txt', [
            "Charset utf-8 or latin1 found",
        ])
        self.assertFileErrors('utf-16be_invalid_utf-8-bom.txt', [
            "Charset utf-8-bom found",
        ])
        self.assertFileErrors('utf-16be_invalid_latin1.txt', [
            "Charset utf-8 or latin1 found",
        ])

    def test_utf16le(self):
        self.assertFileErrors('utf-16le_valid.txt', [])
        self.assertFileErrors('utf-16le_invalid_utf-16be.txt', [
            "Charset utf-16be found",
        ])
        self.assertFileErrors('utf-16le_invalid_utf-8.txt', [
            "Charset utf-8 or latin1 found",
        ])
        self.assertFileErrors('utf-16le_invalid_utf-8-bom.txt', [
            "Charset utf-8-bom found",
        ])
        self.assertFileErrors('utf-16le_invalid_latin1.txt', [
            "Charset utf-8 or latin1 found",
        ])
