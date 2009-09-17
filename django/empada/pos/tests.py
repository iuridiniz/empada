import unittest

from empada.pos.models import Selling

from datetime import datetime

class SalesOpenTest(unittest.TestCase):
    TICKET=31
    def setUp(self):
        s = Selling.objects.create(ticket=SalesOpenTest.TICKET)
        self.id = s.id

    def tearDown(self):
        Selling.objects.get(id=self.id).delete()

    def testOpened(self):
        s = Selling.objects.get(id=self.id)

        self.assertEqual(s.ticket, SalesOpenTest.TICKET)
        self.assertTrue(s.incoming_time <= datetime.now())
        self.assertTrue(s.outcoming_time is None)
        self.assertTrue(s.is_opened)

    def testClose(self):
        s = Selling.objects.get(id=self.id)
        s.close()
        self.assertFalse(s.is_opened)
        self.assertFalse(s.outcoming_time is None)
        self.assertTrue(s.outcoming_time <= datetime.now())

        # refresh from database
        s = Selling.objects.get(id=self.id)
    
        self.assertFalse(s.is_opened)
        self.assertFalse(s.outcoming_time is None)
        self.assertTrue(s.outcoming_time <= datetime.now())

        
