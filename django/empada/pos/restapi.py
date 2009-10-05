from empada.pos.models import Product, Selling, SellingProduct, SellingPayment

from django.http import Http404, HttpResponse

from django_restapi.model_resource import Collection, Entry, reverse
from django_restapi.responder import JSONResponder
from django_restapi.authentication import HttpBasicAuthentication

import json

def json_http_response(request, url, data=None):
    data_content = {'url': url, 'result': data}
    content = json.dumps(data_content) + "\n"
    return HttpResponse(content, mimetype='application/json')
    

class ProductCollection(Collection):
    #TODO: refactoring this to avoid duplicate code for count, maybe extending the class
    #FIXME: count must be on __call__ not on read, READ is only for CRUD
    def read(self, request, product_id = "0", to_count=False):
        if to_count:
            count = self.queryset.count()
            #print "count:", count
            return json_http_response(request, self.get_url(), count)
        else:
            return super(ProductCollection, self).read(request)

product_list = ProductCollection(
    queryset = Product.objects.all(), 
    responder = JSONResponder(paginate_by=10),
    #authentication = HttpBasicAuthentication()
)

class SellingCollection(Collection):
    #TODO: refactoring this to avoid duplicate code for count, maybe extending the class
    #FIXME: count must be on __call__ not on read, READ is only for CRUD
    def read(self, request, selling_id = "0", to_count=False, is_opened=False):
        filtered_set = self.queryset._clone()
        if is_opened:
            filtered_set = self.queryset.filter(is_opened=True)
        
        if to_count:
            count = filtered_set.count()
            #print "is_opened", is_opened
            return json_http_response(request, self.get_url(), count)

        selling_id = int(selling_id)
        #print "Selling id: %d" % (selling_id,)
        return self.responder.list(request, filtered_set)
       
selling_list = SellingCollection(
    queryset = Selling.objects.all(),
    responder = JSONResponder(paginate_by=10),
)


class SellingProductCollection(Collection):
    def read(self, request, selling_id = "0"):
        selling_id = int(selling_id)
        if selling_id > 0:
            filtered_set = self.queryset._clone()
            filtered_set = filtered_set.filter(selling__id=selling_id)
            return self.responder.list(request, filtered_set)
        else:
            return self.responder.list(request, self.queryset)

    def create(self, request, selling_id = "0"):
        #print "Selling id %s" %(selling_id,)
        selling_id = int(selling_id)
        if selling_id > 0:
            #selling
            s = Selling.objects.get(id=selling_id)
            data = self.receiver.get_post_data(request)
            #product
            p = Product.objects.get(id=int(data['id']))
            #print "OK: %s| %s" % (data['id'], p)
            id = s.addProduct(p)
            #print "OK: %d" % (id,) 
            entry = self.get_entry(0, id)
            response = entry.read(request)
            response.status_code = 201
            response['Location'] = entry.get_url()
            return response
        else:
            response = self.responder.error(request, 405)
            return response

        return self.responder.error(request, 400)

    def get_entry(self, selling_id, product_id):
        return super(SellingProductCollection, self).get_entry(product_id)

    def get_url(self):
        return reverse(self, (), {'selling_id': self.model.id})

class SellingProductEntry(Entry):
    def get_url(self):
        return reverse(self.collection, (), {'selling_id': self.model.selling.id, 'product_id':self.model.id})

selling_product_list = SellingProductCollection(
    queryset = SellingProduct.objects.all(),
    responder = JSONResponder(paginate_by=10),
    #permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    permitted_methods = ('GET', 'POST'),
    entry_class = SellingProductEntry,
)

class SellingPaymentCollection(Collection):
    def read(self, request, selling_id = "0"):
        selling_id = int(selling_id)
        if selling_id > 0:
            filtered_set = self.queryset._clone()
            filtered_set = filtered_set.filter(selling__id=selling_id)
            return self.responder.list(request, filtered_set)
        else:
            return self.responder.list(request, self.queryset)

    def create(self, request, selling_id = "0"):
        selling_id = int(selling_id)
        #print "Selling_id: ", selling_id
        if selling_id > 0:
            #selling
            s = Selling.objects.get(id=selling_id)
            data = self.receiver.get_post_data(request)
            #amount
            amount = float(data['amount'])
            id = s.pay(amount=amount)

            entry = self.get_entry(0, id)
            response = entry.read(request)
            response.status_code = 201
            response['Location'] = entry.get_url()
            return response
        else:
            response = self.responder.error(request, 405)
            return response

        return self.responder.error(request, 400)

    def get_entry(self, selling_id, payment_id):
        return super(SellingPaymentCollection, self).get_entry(payment_id)

    def get_url(self):
        return reverse(self, (), {'selling_id': self.model.id})

class SellingPaymentEntry(Entry):
    def get_url(self):
        return reverse(self.collection, (), {'selling_id': self.model.selling.id, 'payment_id':self.model.id})

selling_payment_list = SellingPaymentCollection(
    queryset = SellingPayment.objects.all(),
    responder = JSONResponder(paginate_by=10),
    #permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    permitted_methods = ('GET', 'POST'),
    entry_class = SellingPaymentEntry,
)

#product_xml_resource = Collection(
#    queryset = Product.objects.all(), 
#    responder = XMLResponder(paginate_by=10)
#)
#

