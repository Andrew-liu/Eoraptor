#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
from controllers import page


class TestPage(TestCase):

    def test_page(self):
        p = page.Page([1, 2, 3, 4, 5, 6, 7], 2)
        self.assertFalse(p.has_next())  # False
        self.assertTrue(p.has_previous())
        self.assertEqual(p.current(), [6, 7])

if __name__ == '__main__':
    unittest.main()
