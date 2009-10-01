from pos.models import *
from django.contrib import admin
from django.utils.translation import ugettext as _


# TODO: move this to setting.py
TEST_ALL=True

class IngredientProductInline(admin.TabularInline):
    model = IngredientProduct
    extra = 10

class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'document_id', 'name', 'telephone', 'email']
    list_display_links = list_display
    fieldsets = (
        (_("Basic information"),
            { 'fields': ('name', 'document_id')}),
        (_("Extra information"), 
            { 'fields': ('telephone', 'email'), 'classes': ['collapse']}),
        (_("Financial information"), 
            { 'fields': ('maximum_credit',), 'classes': ['collapse']}),
        (_("Address information"),
            { 'fields': ('address', 'city', 'state'), 'classes': ['collapse'] }),
    )
    list_filter = ['state', 'city']
    search_fields = ['id', 'document_id', 'name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_display_links = list_display
    fieldsets = (
        (_("Basic information"),
            { 'fields': ('name', 'unit', 'is_active')}),
        (_("Extra information"), 
            { 'fields': ('type',), 'classes': ['collapse']}),
        (_("Financial information"), 
            { 'fields': ('price',)}),
    )
    filter_horizontal = ['type']
    list_filter = ['type']
    search_fields = ['name', 'id']
    inlines = [IngredientProductInline]

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = list_display
    search_fields = ['name', 'id']

class UnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']
    list_display_links = list_display
    search_fields = ['name', 'id']


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_display_links = list_display
    fieldsets = (
        (_("Basic information"),
            { 'fields': ('name', 'unit', 'is_active')}),
        (_("Extra information"), 
            { 'fields': ('type',), 'classes': ['collapse']}),
        (_("Financial information"), 
            { 'fields': ('price',)}),
    )
    filter_horizontal = ['type']
    list_filter = ['type']
    search_fields = ['name', 'id']

class IngredientTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = list_display
    search_fields = ['name', 'id']


admin.site.register(Unit, UnitAdmin)

admin.site.register(Client, ClientAdmin)
if TEST_ALL:
    admin.site.register(ClientCredit)
    admin.site.register(ClientHistory)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
if TEST_ALL:
    admin.site.register(ProductHistory)

if TEST_ALL:
    admin.site.register(Selling)
    admin.site.register(SellingProduct)
    admin.site.register(SellingProductIngredient)
    admin.site.register(SellingPayment)

admin.site.register(Ingredient, IngredientAdmin)
if TEST_ALL:
    admin.site.register(IngredientProduct)
    admin.site.register(IngredientHistory)
admin.site.register(IngredientType, IngredientTypeAdmin)

