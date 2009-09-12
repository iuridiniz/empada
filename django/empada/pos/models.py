from django.db import models

from datetime import datetime

from django.utils.translation import ugettext_lazy as _

# Create your models here.

#####################################################################

class Client(models.Model):
    DEFAULT_CREDIT=float(25.00)
    name = models.CharField(
        max_length=30, 
        verbose_name=_('name')
    )
    document_id = models.SlugField(
        max_length=30, 
        unique=True,
        verbose_name=_('document ID')
        )
    address = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('address')
    )
    city = models.CharField(
        max_length=60, 
        blank=True,
        verbose_name = _('city')
    )
    state = models.CharField(
        max_length=30, 
        blank=True,
        verbose_name = _('state')
    )
    email = models.EmailField(
        max_length=40,
        blank=True,
        verbose_name = _('email')
    )
    telephone = models.SlugField(
        max_length=40,
        blank=True,
        verbose_name = _('telephone')
    )
    maximum_credit = models.FloatField(
        blank=True,
        default=DEFAULT_CREDIT,
        verbose_name=_('maximum credit')
    )

    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')
        ordering = ['name']
        #abstract = True

   
class ClientHistory(models.Model):
    client = models.ForeignKey(
        Client, 
        verbose_name = _('client')
    )
    description = models.CharField(
        max_length=120, 
        verbose_name = _('description')
    )
    date = models.DateTimeField(
        default=datetime.now, 
        verbose_name = _('date')
    )

    def __unicode__(self):
        return u'%s' % self.date

    class Meta:
        verbose_name = _('client modification history')
        verbose_name_plural = _('client modification histories')
        ordering = ['client', '-date']
        #abstract = True

class ClientCredit(models.Model):
    client = models.ForeignKey(
        Client, 
        verbose_name = _('client')
    )
    amount = models.FloatField(
        verbose_name = _('amount')
    )
    date = models.DateTimeField(
        verbose_name = _('date')
    )
    is_payment = models.BooleanField(
        verbose_name = _('is a payment')
    )
    selling = models.ForeignKey(
        'Selling', 
        blank=True,
        null=True,
        verbose_name = _('selling')
    )

    def __unicode__(self):
        if self.is_payment == True:
            type = "payment"
        else:
            type = "credit"
        return u'%s done on %s by %s' % (type, self.date, self.client.name)
    
    class Meta:
        verbose_name = _('client credit')
        verbose_name_plural = _('client credits')
        ordering = ['client', '-date']
        #abstract = True


#####################################################################
class ProductType(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name=_('name')
    )

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('product type')
        verbose_name_plural = _('product types')
        ordering = ['name']
        #abstract = True

class Product(models.Model):
    type = models.ManyToManyField(
        ProductType,
        verbose_name = _('type'),
        blank=True
    )
    name = models.CharField(
        max_length=30,
        verbose_name = _('name')
    )
    price = models.FloatField(
        verbose_name = _('price')
    )
    is_active = models.BooleanField(
        verbose_name = _('is active'),
        default=True
    )
    
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['name', 'price', 'is_active']
        #abstract = True


class ProductHistory(models.Model):
    product = models.ForeignKey(
        Product, 
        verbose_name = _('product')
    )
    description = models.CharField(
        max_length=30, 
        verbose_name=_('description')
    )
    date = models.DateTimeField(
        verbose_name=_('date')
    )

    def __unicode__(self):
        return u'%s' % self.date

    class Meta:
        verbose_name = _('product modification history')
        verbose_name_plural = _('product modification histories')
        ordering = ['product', 'date']
        #abstract = True


#####################################################################
class IngredientType(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name=_('name')
    )

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('ingredient type')
        verbose_name_plural = _('ingredient types')
        ordering = ['name']
        #abstract = True
   

class Ingredient(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name = _('name')
    )

    is_active = models.BooleanField(
        verbose_name = _('is active'),
        default=True
    )

    price = models.FloatField(
        verbose_name = _('price'),
        default=float(0.00)
    )

    type = models.ManyToManyField(
        IngredientType,
        verbose_name = _('type'), 
        blank=True
    )
    
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')
        ordering = ['name', 'is_active']
        #abstract = True

class IngredientProduct(models.Model):
    TYPE_CHOICES = (
        ('F', _('Fixed')),
        ('O', _('Optional')),
        ('I', _('Included')),
    )

    product = models.ForeignKey(
        Product, 
        verbose_name = _('product')
    )

    ingredient = models.ForeignKey(
        Ingredient, 
        verbose_name = _('ingredient')
    )

    price = models.FloatField(
        verbose_name = _('price'),
        default=float(0.00)
    )

    quantity = models.FloatField(
        verbose_name = _('quantity'),
        default=float(1.00)
    )

    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES, 
        verbose_name=_('type'),
        default='F'
    )

    def __unicode__(self):
        return u'Product: %s, Ingredient: %s' % (self.product, self.ingredient,)

    class Meta:
        verbose_name = _('ingredient of a product')
        verbose_name_plural = _('ingredients of a product')
        ordering = ['product', 'ingredient']
        #abstract = True

class IngredientHistory(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, 
        verbose_name = _('ingredient')
    )
    description = models.CharField(
        max_length=30, 
        verbose_name=_('description')
    )
    date = models.DateTimeField(
        verbose_name=_('date')
    )

    def __unicode__(self):
        return u'modification in %s on %s' % (self.ingredient, self.date,)

    class Meta:
        verbose_name = _('ingredient modification history')
        verbose_name_plural = _('ingredient modification histories')
        ordering = ['ingredient', 'date']
        #abstract = True


#####################################################################
class Selling(models.Model):
    product = models.ManyToManyField(
        Product, 
        through='SellingProduct', 
        verbose_name=_('product')
    )
    ticket = models.CharField(
        max_length=30, 
        verbose_name=_('ticket'),
        blank=True
    )
    is_paid = models.BooleanField(
        verbose_name=_('is paid'),
        default=False
    )
    amount_paid = models.FloatField(
        verbose_name=_('amount paid'), 
        default=0.00
    )
    incoming_time = models.DateTimeField(
        verbose_name=_('incoming time'),
        default=datetime.now,
    )
    outcoming_time = models.DateTimeField(
        verbose_name=_('outcoming time'),
        blank=True
    )

    def __unicode__(self):
        return u'Selling %d |ticket %s' % (self.id, self.ticket)

    class Meta:
        verbose_name = _('selling')
        verbose_name_plural = _('sellings')
        ordering = ['is_paid','incoming_time', 'ticket']
        #abstract = True

class SellingProduct(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_('product'),
    )
    selling = models.ForeignKey(
        Selling,
        verbose_name=_('selling')
    )
    instructions = models.TextField(
        max_length=256, 
        blank=True,
        verbose_name=_('special instuctions')
    )
    quantity = models.FloatField(
        verbose_name=_('quantity'),
        default=float(1.0)
    )
    selling_unit_price = models.FloatField(
        verbose_name=_('selling unit price'),
        default = float(0.00),
    )
    date = models.DateTimeField(
        verbose_name=_('selling date'),
        default = datetime.now
    )
    def __unicode__(self):
        return u'Selling id %u of product %s' % (self.selling.id, self.product.name)

    class Meta:
        verbose_name = _('selling product')
        verbose_name_plural = _('selling products')
        ordering = ['selling', 'date', 'product']
        #abstract = True

class SellingProductIngredient(models.Model):
    ingredient_product = models.ForeignKey(
        IngredientProduct,
        verbose_name=_('ingredient'),
    )

    selling_product = models.ForeignKey(
        SellingProduct,
        verbose_name=_('selling product')
    )

    selling_price = models.FloatField(
        verbose_name=_('selling unit price'),
        default = float(0.00),
    )
    
    class Meta:
        verbose_name = _('selling product ingredient')
        verbose_name_plural = _('selling product ingredients')
        ordering = ['selling_product', 'ingredient_product']
        #abstract = True


class SellingPayment(models.Model):
    selling = models.ForeignKey(
        Selling,
        verbose_name=_("selling"),
    )
    client = models.ForeignKey(
        Client, 
        blank=True,
        null=True,
        verbose_name=_("client"),
    )
    amount = models.FloatField(
        verbose_name=_("amount")
    )
    is_credit = models.BooleanField(
        verbose_name=_("is credit"),
        default=False
    )

    def __unicode__(self):
        return u'Selling %s |amount %f' % (self.selling.id, self.amount)

    class Meta:
        verbose_name = _('selling payment')
        verbose_name_plural = _('selling payments')
        ordering = ['selling', 'client']
        #abstract = True


#####################################################################


