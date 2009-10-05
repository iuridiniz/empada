from empada.pos.models import Product, Selling, SellingProduct

from django.http import Http404

from django_restapi.model_resource import Collection, Entry, reverse
from django_restapi.responder import JSONResponder
from django_restapi.authentication import HttpBasicAuthentication

product_list = Collection(
    queryset = Product.objects.all(), 
    responder = JSONResponder(paginate_by=10),
    #authentication = HttpBasicAuthentication()
)

selling_opened_list = Collection(
    queryset = Selling.objects.filter(is_opened=True),
    responder = JSONResponder(paginate_by=10),
)

selling_list = Collection(
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

#product_xml_resource = Collection(
#    queryset = Product.objects.all(), 
#    responder = XMLResponder(paginate_by=10)
#)
#

