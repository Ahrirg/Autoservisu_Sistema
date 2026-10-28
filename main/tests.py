from django.test import TestCase


class BasicTests(TestCase):
    def test_example(self):
        rez = 2 + 2

        self.assertEqual(rez, 4)