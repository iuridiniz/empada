from empada.pos.models import Product, Selling

from django_restapi.model_resource import Collection
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


#product_xml_resource = Collection(
#    queryset = Product.objects.all(), 
#    responder = XMLResponder(paginate_by=10)
#)
#

