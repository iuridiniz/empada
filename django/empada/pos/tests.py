#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
#import unittest

from exceptions import OperationNotPermited, DuplicateOpenedTicket

from empada.pos.models import Selling, Product, SellingProduct, Unit, SellingPayment

from datetime import datetime


import json

class SalesOpenCloseTest(TestCase):
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

class SalesDuplicateTicketTest(TestCase):
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

class SalesBuyProductsTest(TestCase):
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
        self.ids.append(s.id)
        s.close()
        
        self.assertTrue(s.product.count() == 0)        
        self.assertRaises(OperationNotPermited, s.addProduct, self.p1)

        self.assertTrue(s.product.count() == 0)
        

class SalesPayTest(TestCase):
    def setUp(self):
        self.ids = []
        un1 = Unit.objects.create(name=u"Peça")
        un2 = Unit.objects.create(name="Kg", type='F')
        # create 2 simple products
        self.p1 = Product.objects.create(name="Coxinha de frango", price=float(1.00), unit=un1)
        # create 1 fractionary product
        self.p2 = Product.objects.create(name="Bolo de chocolate", price=float(12.00), unit=un2)
        
    def tearDown(self):
        self.p1.delete()
        self.p2.delete()

        for id in self.ids:
            Selling.objects.get(id=id).delete()
    
    def testPayInTotally(self):
        
        s = Selling.objects.create()
        self.ids.append(s.id)
        s.addProduct(self.p1)
        s.addProduct(self.p2)
        
        self.assertEqual(SellingPayment.objects.filter(selling=s.id).count(), 0) 
        s.pay(amount=s.amount)
        
        self.assertEqual(SellingPayment.objects.filter(selling=s.id).count(), 1) 
        
        self.assertTrue(s.is_paid == True)
        self.assertAlmostEqual(s.amount_paid, s.amount)
        
        s.close()
        
    def testPayMostPart(self):
        
        s = Selling.objects.create()
        self.ids.append(s.id)
        s.addProduct(self.p1)
        s.addProduct(self.p2)
        
        s.pay(amount=s.amount * 0.80)
        
        self.assertTrue(s.is_paid == False)
        self.assertAlmostEqual(s.amount_paid, s.amount * 0.80)
        
        s.close()
        
    def testTwoPayInTotally(self):
        
        s = Selling.objects.create()
        self.ids.append(s.id)
        s.addProduct(self.p1)
        s.addProduct(self.p2)
        
        self.assertEqual(SellingPayment.objects.filter(selling=s.id).count(), 0) 
        s.pay(amount=s.amount * 0.60)
        self.assertEqual(SellingPayment.objects.filter(selling=s.id).count(), 1) 
        self.assertAlmostEqual(s.amount_paid, s.amount * 0.60)
        self.assertTrue(s.is_paid == False)
        
        s.pay(amount=s.amount * 0.40)
        self.assertEqual(SellingPayment.objects.filter(selling=s.id).count(), 2) 
        self.assertTrue(s.is_paid == True)
        self.assertAlmostEqual(s.amount_paid, s.amount)
        
        s.close()
    
    def testTwoPayMoreThanTotally(self):
        s = Selling.objects.create()
        self.ids.append(s.id)
        s.addProduct(self.p1)
        s.addProduct(self.p2)
        
        s.pay(amount=s.amount * 0.60)
        self.assertAlmostEqual(s.amount_paid, s.amount * 0.60)
        self.assertTrue(s.is_paid == False)
        
        s.pay(amount=s.amount * 0.60)
        self.assertTrue(s.is_paid == True)
        self.assertNotAlmostEqual(s.amount_paid, s.amount)
        
        s.close()

    def testPayNegative(self):
        s = Selling.objects.create()
        self.ids.append(s.id)
        s.addProduct(self.p1)
        s.addProduct(self.p2)

        self.assertRaises(OperationNotPermited, s.pay, -30)
        s.close()
        
class RestTest(TestCase):

    BASE_URL = '/pos/json/'
    fixtures = ['testdata.json']

    def setUp(self):
        self.last_product = Product.objects.order_by('-id')[0]
        self.first_product = Product.objects.order_by('id')[0]
        self.opened_selling = Selling.objects.filter(is_opened=True)[0]
        self.closed_selling = Selling.objects.filter(is_opened=False)[0]

    def tearDown(self):
        pass

    def testUrlListSellings(self):
        #FIXME: We Trust on django_restapi, so we must use json to verify
        url = RestTest.BASE_URL + 'Selling/'

        response = self.client.get(url)
        
        self.failUnlessEqual(response.status_code, 200)
        self.failIfEqual(response.content.find('"pos.selling"'), -1)
        self.failIfEqual(response.content.find('"pk": %d' % (self.opened_selling.id,)), -1)
        self.failIfEqual(response.content.find('"pk": %d' % (self.closed_selling.id,)), -1)

    def testUrlListProducts(self):
        #FIXME: We Trust on django_restapi, so we must use json to verify
        url = RestTest.BASE_URL + 'Product/'

        response = self.client.get(url)

        self.failUnlessEqual(response.status_code, 200)
        self.failIfEqual(response.content.find('"pos.product"'), -1)
        self.failIfEqual(response.content.find('"name": "%s"' % (self.first_product.name,)), -1)
        self.failIfEqual(response.content.find('"pk": %d' % (self.first_product.id,)), -1)

        self.failIfEqual(response.content.find('"name": "%s"' % (self.last_product.name,)), -1)
        self.failIfEqual(response.content.find('"pk": %d' % (self.last_product.id,)), -1)

    def testUrlGetProduct(self):
        #FIXME: We Trust on django_restapi, so we must use json to verify
        url = RestTest.BASE_URL + 'Product/%d/' % (self.first_product.id,)

        response = self.client.get(url)

        self.failUnlessEqual(response.status_code, 200)
        self.failIfEqual(response.content.find('"pos.product"'), -1)
        self.failIfEqual(response.content.find('"pk": %d' % (self.first_product.id,)), -1)
        self.failIfEqual(response.content.find('"name": "%s"' % (self.first_product.name,)), -1)
    
        # test for error
        self.failUnlessEqual(response.content.find('"pk": %d' % (self.last_product.id,)), -1)

    def testUrlListOpenedSellings(self):
        #FIXME: We Trust on django_restapi, so we must use json to verify
        url = RestTest.BASE_URL + 'Selling/is_opened/'
        response = self.client.get(url)

        self.failUnlessEqual(response.status_code, 200)
        self.failIfEqual(response.content.find('"pos.selling"'), -1)
        self.failIfEqual(response.content.find('"pk": %d' % (self.opened_selling.id,)), -1)
        self.failUnlessEqual(response.content.find('"pk": %d' % (self.closed_selling.id,)), -1)



    def testUrlGetOpenedSelling(self):
        #FIXME: We Trust on django_restapi, so we must use json to verify
        url = RestTest.BASE_URL + 'Selling/is_opened/%d/' % (self.opened_selling.id,)
        response = self.client.get(url)

        self.failUnlessEqual(response.status_code, 200)
        self.failIfEqual(response.content.find('"pos.selling"'), -1)
        self.failIfEqual(response.content.find('"pk": %d' % (self.opened_selling.id,)), -1)

        # try to get a closed (disabled: not implemented)
        #url = RestTest.BASE_URL + 'Selling/is_opened/%d' % (self.closed_selling.id,)
        #response = self.client.get(url)

        #self.failUnlessEqual(response.status_code, 404)

    def testUrlOpenedSellingCount(self):
        url = RestTest.BASE_URL + 'Selling/is_opened/count/' 
        response = self.client.get(url)

        self.failUnlessEqual(response.status_code, 200)
        count = Selling.objects.filter(is_opened=True).count()
        data = json.loads(response.content)

        self.assertEqual(data[0]['result'], count)


    def testUrlSellingCount(self):
        url = RestTest.BASE_URL + 'Selling/count/' 
        response = self.client.get(url)

        self.failUnlessEqual(response.status_code, 200)
        count = Selling.objects.all().count()
        data = json.loads(response.content)

        self.assertEqual(data[0]['result'], count)

    def testUrlProductCount(self):
        url = RestTest.BASE_URL + 'Product/count/' 
        response = self.client.get(url)

        self.failUnlessEqual(response.status_code, 200)
        count = Product.objects.all().count()
        data = json.loads(response.content)

        self.assertEqual(data[0]['result'], count)

    def testUrlSellingPaymentCount(self):
        url = RestTest.BASE_URL + "Selling/%d/Payment/count/" % (self.opened_selling.id,)
        response = self.client.get(url)

        self.failUnlessEqual(response.status_code, 200)
        count = SellingPayment.objects.filter(selling__id=self.opened_selling.id).count()
        data = json.loads(response.content)

        self.assertEqual(data[0]['result'], count)

    def testUrlSellingProducts(self):
        #FIXME: We Trust on django_restapi, so we must use json to verify
        url = RestTest.BASE_URL + 'Selling/%d/Product/' % (self.opened_selling.id,)
        response = self.client.get(url)
        
        self.failUnlessEqual(response.status_code, 200)
        self.failIfEqual(response.content.find('"pos.sellingproduct"'), -1)
        self.failIfEqual(response.content.find('"selling": %d' % (self.opened_selling.id,)), -1)


    def testUrlAddProduct(self):
        #FIXME: We Trust on django_restapi, so we must use json to verify
        url = RestTest.BASE_URL + 'Selling/%d/Product/' % (self.opened_selling.id,)
        params = {
            'id': self.first_product.id
        }
        response = self.client.post(url, params)

        self.failUnlessEqual(response.status_code, 201)

    def testUrlAddPayment(self):
        url = RestTest.BASE_URL + "Selling/%d/Payment/" % (self.opened_selling.id,)

        self.opened_selling.addProduct(self.first_product)

        params = {
           'amount': self.first_product.price
        }

        response = self.client.post(url, params)
        self.failUnlessEqual(response.status_code, 201)

        data = json.loads(response.content)

        self.assertEqual(data[0]["model"], "pos.sellingpayment")
        self.assertAlmostEqual(data[0]["fields"]["amount"], self.first_product.price)
        self.assertEqual(data[0]['fields']['selling'], self.opened_selling.id)

    def testUrlCloseReopenSelling(self):
        selling_id = self.opened_selling.id

        #close
        url = RestTest.BASE_URL + "Selling/is_opened/%d/close/" % (selling_id,)

        response = self.client.get(url)

        self.failUnlessEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data[0]['result'], True)

        s = Selling.objects.get(id=selling_id)
        self.assertTrue(s.is_closed)

        #reopen
        url = RestTest.BASE_URL + "Selling/is_closed/%d/reopen/" % (selling_id,)

        response = self.client.get(url)

        self.failUnlessEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data[0]['result'], True)

        s = Selling.objects.get(id=selling_id)
        self.assertTrue(s.is_opened)

        

