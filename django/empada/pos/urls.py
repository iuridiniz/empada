#!/usr/bin/env python
from django.conf.urls.defaults import *

from restapi import product_list, selling_list, selling_product_list

urlpatterns = patterns('',

###############################################################################
    (r'^json/Product/$', product_list),
    (r'^json/Product/(\d+)/$', product_list),
    (r'^json/Product/count/$', product_list, {'to_count':True, 'is_entry':False}),
###############################################################################
    (r'^json/Selling/$', selling_list),
    (r'^json/Selling/(\d+)/$', selling_list),

###############################################################################
    (r'^json/Selling/(?P<selling_id>\d+)/Product/$', selling_product_list, {'is_entry':False}),
    (r'^json/Selling/(?P<selling_id>\d+)/Product/(?P<product_id>\d+)/$', selling_product_list, {'is_entry':True}),

###############################################################################
    (r'^json/Selling/is_opened/$', selling_list, {'is_opened':True, 'is_entry':False}),
    (r'^json/Selling/is_opened/(\d+)/$', selling_list, {'is_entry':True}),
    (r'^json/Selling/is_opened/count/$', selling_list, {'is_opened': True, 'is_entry':False, 'to_count':True}),
)

