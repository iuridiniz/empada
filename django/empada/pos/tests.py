#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from exceptions import OperationNotPermited, DuplicateOpenedTicket

from empada.pos.models import Selling, Product, SellingProduct, Unit

from datetime import datetime

class SalesOpenCloseTest(unittest.TestCase):
    TICKET=31
    def setUp(self):
        self.ids = []

    def tearDown(self):
        for id in self.ids:
            Selling.objects.get(id=id).delete()

    def createSale(self, ticket=TICKET):
        return Selling.objects.create(ticket=ticket)

    def testOpenAndClose(self):
        s = self.createSale()
        self.ids.append(s.id)

        # A new created sale must be opened
        self.assertEqual(s.ticket, SalesOpenCloseTest.TICKET)
        self.assertTrue(s.incoming_time < datetime.now())
        self.assertTrue(s.outcoming_time is None)
        self.assertTrue(s.is_opened)

        # Now close it
        s.close()

        self.assertFalse(s.is_opened)
        self.assertFalse(s.outcoming_time is None)
        self.assertTrue(s.outcoming_time < datetime.now())

        # refresh from database
        #s = Selling.objects.get(id=self.id)
    
        #self.assertFalse(s.is_opened)
        #self.assertFalse(s.outcoming_time is None)
        #self.assertTrue(s.outcoming_time < datetime.now())
        
    def testReopenAndClose(self):
        s = self.createSale(SalesOpenCloseTest.TICKET+1)
        self.ids.append(s.id)

        self.assertTrue(s.is_opened)
        s.close()
        self.assertFalse(s.is_opened)
        
        old_incoming_time = s.incoming_time
        old_outcoming_time = s.outcoming_time

        s.reopen()
        self.assertTrue(s.is_opened)
        self.assertTrue(s.incoming_time == old_incoming_time)
        self.assertTrue(s.outcoming_time is None)

        s.close()
        self.assertFalse(s.is_opened)
        self.assertTrue(s.incoming_time == old_incoming_time)
        self.assertTrue(s.outcoming_time > old_outcoming_time)
        self.assertTrue(s.outcoming_time < datetime.now())

class SalesDuplicateTicketTest(unittest.TestCase):
    TICKET=21

    def setUp(self):
        self.ids = []

    def createSale(self):
        return Selling.objects.create(ticket=SalesDuplicateTicketTest.TICKET)

    def testCreateTwo(self):
        # create the first one
        s1 = self.createSale()
        self.ids.append(s1.id)
        self.assertTrue(s1.is_opened)

        # try to create the second one
        self.assertRaises(DuplicateOpenedTicket, self.createSale)

        # now close the first one
        s1.close()
        self.assertFalse(s1.is_opened)

        # try to create the second one
        s2 = self.createSale()
        self.ids.append(s2.id)
        self.assertTrue(s2.is_opened)

        # we cannot reopen first one now, same ticket
        self.assertRaises(DuplicateOpenedTicket, s1.reopen)
        self.assertFalse(s1.is_opened)

        # but we can, after close the second one
        s2.close()
        self.assertFalse(s2.is_opened)

        s1.reopen()
        self.assertTrue(s1.is_opened)

    def tearDown(self):
        for id in self.ids:
            Selling.objects.get(id=id).delete()

class SalesBuyProductsTest(unittest.TestCase):
    def setUp(self):
        un1 = Unit.objects.create(name=u"Peça")
        un2 = Unit.objects.create(name="Kg", type='F')
        # create 3 simple products
        self.p1 = Product.objects.create(name="Coxinha de frango", price=float(1.00), unit=un1)
        self.p2 = Product.objects.create(name="Pastel de carne", price=float(2.30), unit=un1)
        self.p3 = Product.objects.create(name="Coca-Cola 350ml", price=float(1.20), unit=un1)
        # create a fractionary product
        self.p4 = Product.objects.create(name="Bolo de chocolate", price=float(12.00), unit=un2)
        
        self.ids = []
    def tearDown(self):
        self.p1.delete()
        self.p2.delete()
        self.p3.delete()
        
        for id in self.ids:
            Selling.objects.get(id=id).delete()

    def testSaleProducts(self):
        # Selling without ticket
        amount = float(0.00)
        qtd = 0
        s = Selling.objects.create()
        self.ids.append(s.id)

        # 1 x p1
        s.addProduct(self.p1)
        amount += self.p1.price
        qtd += 1
        self.assertTrue(s.product.count() == qtd)
        self.assertAlmostEqual(s.amount, amount)

        # 2 x p2
        s.addProduct(self.p2, quantity=2)
        amount += 2 * self.p2.price
        qtd += 2
        self.assertTrue(s.product.count() == qtd)
        self.assertAlmostEqual(s.amount, amount)

        # 3 x p3 with instructions
        s.addProduct(self.p3, quantity=3, instructions="with lemon")
        amount += 3 * self.p3.price
        qtd += 3
        self.assertTrue(s.product.count() == qtd)
        self.assertAlmostEqual(s.amount, amount)

        # 1 x p3 with a special price
        s.addProduct(self.p3, quantity=1, price=1.00)
        amount += 1 * 1.00
        qtd += 1
        self.assertTrue(s.product.count() == qtd)
        self.assertAlmostEqual(s.amount, amount)
        
        # 0.300 kg x p4
        s.addProduct(self.p4, quantity=0.300)
        amount += 0.300 * self.p4.price
        qtd += 1
        self.assertTrue(s.product.count() == qtd)
        self.assertAlmostEqual(s.amount, amount)
        
        # 4.500 kg x p4
        s.addProduct(self.p4, quantity=4.500)
        amount += 4.500 * self.p4.price
        qtd += 1
        self.assertTrue(s.product.count() == qtd)
        self.assertAlmostEqual(s.amount, amount)
        
    def testSaleProductOnClosedSelling(self):
        s = Selling.objects.create()
        s.close()
        
        self.assertTrue(s.product.count() == 0)        
        self.assertRaises(OperationNotPermited, s.addProduct, self.p1)

        self.assertTrue(s.product.count() == 0)
        
        
