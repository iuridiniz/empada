#!/usr/bin/env python
from django.conf.urls.defaults import *

from restapi import product_list, selling_list, selling_opened_list

urlpatterns = patterns('',
    (r'^json/Product/(\d*?)/?$', product_list),
    (r'^json/Selling/(\d*?)/?$', selling_list),
    (r'^json/Selling/is_opened/(\d*?)/?$', selling_opened_list),
)

