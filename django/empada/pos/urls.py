#!/usr/bin/env python
from django.conf.urls.defaults import *

from restapi import product_list, selling_list, selling_product_list, selling_payment_list

urlpatterns = patterns('',

###############################################################################
    (r'^json/Product/$', product_list),
    (r'^json/Product/(\d+)/$', product_list),
    (r'^json/Product/count/$', product_list, {'call':'count'}),
###############################################################################
    (r'^json/Selling/$', selling_list),
    (r'^json/Selling/(\d+)/$', selling_list),
    (r'^json/Selling/count/$', selling_list, {'call':'count'}),

    (r'^json/Selling/is_opened/$', selling_list, {'is_opened':True, 'is_entry':False}),
    (r'^json/Selling/is_opened/(\d+)/$', selling_list, {'is_entry':True}),
    (r'^json/Selling/is_opened/count/$', selling_list, {'is_opened': True, 'call':'count'}),
    (r'^json/Selling/is_opened/(?P<selling_id>\d+)/close/$', selling_list, {'call':'close'}),

    (r'^json/Selling/is_closed/$', selling_list, {'is_opened':False, 'is_entry':False}),
    (r'^json/Selling/is_closed/(\d+)/$', selling_list, {'is_entry':False}),
    (r'^json/Selling/is_closed/count/$', selling_list, {'is_opened': False, 'call':'count'}),
    (r'^json/Selling/is_closed/(?P<selling_id>\d+)/reopen/$', selling_list, {'call':'reopen'}),

###############################################################################
    (r'^json/Selling/(?P<selling_id>\d+)/Product/$', selling_product_list, {'is_entry':False}),
    (r'^json/Selling/(?P<selling_id>\d+)/Product/(?P<product_id>\d+)/$', selling_product_list, {'is_entry':True}),

###############################################################################
    (r'^json/Selling/(?P<selling_id>\d+)/Payment/$', selling_payment_list, {'is_entry':False}),
    (r'^json/Selling/(?P<selling_id>\d+)/Payment/(?P<payment_id>\d+)/$', selling_payment_list, {'is_entry':True}),
    (r'^json/Selling/(?P<selling_id>\d+)/Payment/(?P<call>count)/$', selling_payment_list),
    (r'^json/SellingPayment/(?P<payment_id>\d+)/$', selling_payment_list),
    (r'^json/SellingPayment/$', selling_payment_list),
    (r'^json/SellingPayment/count/$', selling_payment_list, {'call':'count'}),


###############################################################################


)

