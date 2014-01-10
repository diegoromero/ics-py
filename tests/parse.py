import unittest

from .fixture import cal1, cal5, cal11
from ics.event import Event
from ics.icalendar import Calendar
from ics.parse import (
    ParseError,
    ContentLine,
    Container,
    string_to_container,
    lines_to_container,
)


class TestParse(unittest.TestCase):

    def test_parse(self):
        content = string_to_container(cal5)
        self.assertEqual(1, len(content))

        cal = content.pop()
        self.assertEqual('VCALENDAR', cal.name)
        self.assertTrue(isinstance(cal, Container))
        self.assertEqual('VERSION', cal[0].name)
        self.assertEqual('2.0', cal[0].value)
        self.assertEqual(cal5.strip(), str(cal).strip())

    def test_one_line(self):
        ics = 'DTSTART;TZID=Europe/Brussels:20131029T103000'
        reader = lines_to_container([ics])
        self.assertEqual(next(iter(reader)), ContentLine(
            'DTSTART',
            {'TZID': ['Europe/Brussels']},
            '20131029T103000'
        ))

    def test_many_lines(self):
        i = 0
        for line in string_to_container(cal1)[0]:
            self.assertNotEqual('', line.name)
            if isinstance(line, ContentLine):
                self.assertNotEqual('', line.value)
            if line.name == 'DESCRIPTION':
                self.assertEqual('Lorem ipsum dolor sit amet, \
                    consectetur adipiscing elit. \
                    Sed vitae facilisis enim. \
                    Morbi blandit et lectus venenatis tristique. \
                    Donec sit amet egestas lacus. \
                    Donec ullamcorper, mi vitae congue dictum, \
                    quam dolor luctus augue, id cursus purus justo vel lorem. \
                    Ut feugiat enim ipsum, quis porta nibh ultricies congue. \
                    Pellentesque nisl mi, molestie id sem vel, \
                    vehicula nullam.', line.value)
            i += 1

    def test_end_different(self):

        with self.assertRaises(ParseError):
            Calendar(cal11)

    def test_repr(self):

        e = Event(begin=0, end=10)
        c = Container("test", e)

        self.assertEqual("<Container 'test' with 1 element>", repr(c))