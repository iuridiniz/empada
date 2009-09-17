from django.db import models
from django.core.exceptions import ValidationError

from datetime import datetime

from django.utils.translation import ugettext_lazy as _L
from django.utils.translation import ugettext as _

# Create your models here.

#####################################################################

class Client(models.Model):
    DEFAULT_CREDIT=float(25.00)
    name = models.CharField(
        max_length=30, 
        verbose_name=_L('name')
    )
    document_id = models.SlugField(
        max_length=30, 
        unique=True,
        verbose_name=_L('document ID')
        )
    address = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_L('address')
    )
    city = models.CharField(
        max_length=60, 
        blank=True,
        verbose_name = _L('city')
    )
    state = models.CharField(
        max_length=30, 
        blank=True,
        verbose_name = _L('state')
    )
    email = models.EmailField(
        max_length=40,
        blank=True,
        verbose_name = _L('email')
    )
    telephone = models.SlugField(
        max_length=40,
        blank=True,
        verbose_name = _L('telephone')
    )
    maximum_credit = models.FloatField(
        blank=True,
        default=DEFAULT_CREDIT,
        verbose_name=_L('maximum credit')
    )

    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = _L('client')
        verbose_name_plural = _L('clients')
        ordering = ['name']
        #abstract = True

   
class ClientHistory(models.Model):
    client = models.ForeignKey(
        Client, 
        verbose_name = _L('client')
    )
    description = models.CharField(
        max_length=120, 
        verbose_name = _L('description')
    )
    date = models.DateTimeField(
        default=datetime.now, 
        verbose_name = _L('date')
    )

    def __unicode__(self):
        return u'%s' % self.date

    class Meta:
        verbose_name = _L('client modification history')
        verbose_name_plural = _L('client modification histories')
        ordering = ['client', '-date']
        #abstract = True

class ClientCredit(models.Model):
    client = models.ForeignKey(
        Client, 
        verbose_name = _L('client')
    )
    amount = models.FloatField(
        verbose_name = _L('amount')
    )
    date = models.DateTimeField(
        verbose_name = _L('date')
    )
    is_payment = models.BooleanField(
        verbose_name = _L('is a payment')
    )
    selling = models.ForeignKey(
        'Selling', 
        blank=True,
        null=True,
        verbose_name = _L('selling')
    )

    def __unicode__(self):
        if self.is_payment == True:
            type = "payment"
        else:
            type = "credit"
        return u'%s done on %s by %s' % (type, self.date, self.client.name)
    
    class Meta:
        verbose_name = _L('client credit')
        verbose_name_plural = _L('client credits')
        ordering = ['client', '-date']
        #abstract = True


#####################################################################
class ProductType(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name=_L('name')
    )

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _L('product type')
        verbose_name_plural = _L('product types')
        ordering = ['name']
        #abstract = True

class Product(models.Model):
    type = models.ManyToManyField(
        ProductType,
        verbose_name = _L('type'),
        blank=True
    )
    name = models.CharField(
        max_length=30,
        verbose_name = _L('name')
    )
    price = models.FloatField(
        verbose_name = _L('price')
    )
    is_active = models.BooleanField(
        verbose_name = _L('is active'),
        default=True
    )
    
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _L('product')
        verbose_name_plural = _L('products')
        ordering = ['name', 'price', 'is_active']
        #abstract = True


class ProductHistory(models.Model):
    product = models.ForeignKey(
        Product, 
        verbose_name = _L('product')
    )
    description = models.CharField(
        max_length=30, 
        verbose_name=_L('description')
    )
    date = models.DateTimeField(
        verbose_name=_L('date')
    )

    def __unicode__(self):
        return u'%s' % self.date

    class Meta:
        verbose_name = _L('product modification history')
        verbose_name_plural = _L('product modification histories')
        ordering = ['product', 'date']
        #abstract = True


#####################################################################
class IngredientType(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name=_L('name')
    )

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _L('ingredient type')
        verbose_name_plural = _L('ingredient types')
        ordering = ['name']
        #abstract = True
   

class Ingredient(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name = _L('name')
    )

    is_active = models.BooleanField(
        verbose_name = _L('is active'),
        default=True
    )

    price = models.FloatField(
        verbose_name = _L('price'),
        default=float(0.00)
    )

    type = models.ManyToManyField(
        IngredientType,
        verbose_name = _L('type'), 
        blank=True
    )
    
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = _L('ingredient')
        verbose_name_plural = _L('ingredients')
        ordering = ['name', 'is_active']
        #abstract = True

class IngredientProduct(models.Model):
    TYPE_CHOICES = (
        ('F', _L('Fixed')),
        ('O', _L('Optional')),
        ('I', _L('Included')),
    )

    product = models.ForeignKey(
        Product, 
        verbose_name = _L('product')
    )

    ingredient = models.ForeignKey(
        Ingredient, 
        verbose_name = _L('ingredient')
    )

    price = models.FloatField(
        verbose_name = _L('price'),
        default=float(0.00)
    )

    quantity = models.FloatField(
        verbose_name = _L('quantity'),
        default=float(1.00)
    )

    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES, 
        verbose_name=_L('type'),
        default='F'
    )

    def __unicode__(self):
        return u'Product: %s, Ingredient: %s' % (self.product, self.ingredient,)

    class Meta:
        verbose_name = _L('ingredient of a product')
        verbose_name_plural = _L('ingredients of a product')
        ordering = ['product', 'ingredient']
        #abstract = True

class IngredientHistory(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, 
        verbose_name = _L('ingredient')
    )
    description = models.CharField(
        max_length=30, 
        verbose_name=_L('description')
    )
    date = models.DateTimeField(
        verbose_name=_L('date')
    )

    def __unicode__(self):
        return u'modification in %s on %s' % (self.ingredient, self.date,)

    class Meta:
        verbose_name = _L('ingredient modification history')
        verbose_name_plural = _L('ingredient modification histories')
        ordering = ['ingredient', 'date']
        #abstract = True


#####################################################################
class SellingHistory(models.Model):
    selling = models.ForeignKey(
        'Selling', 
        verbose_name = _L('selling')
    )
    description = models.CharField(
        max_length=30, 
        verbose_name=_L('description')
    )
    date = models.DateTimeField(
        verbose_name=_L('date'),
        default=datetime.now
    )

    def __unicode__(self):
        return u'Modification in [%s] on [%s]' % (self.selling, self.date,)

    class Meta:
        verbose_name = _L('selling modification history')
        verbose_name_plural = _L('selling modification histories')
        ordering = ['selling', 'date']
        #abstract = True

class Selling(models.Model):
    product = models.ManyToManyField(
        Product, 
        through='SellingProduct', 
        verbose_name=_L('product')
    )

    ticket = models.IntegerField(
        verbose_name=_L('ticket'),
        blank=True,
        null=True
    )

    is_paid = models.BooleanField(
        verbose_name=_L('is paid'),
        default=False
    )

    amount_paid = models.FloatField(
        verbose_name=_L('amount paid'), 
        default=0.00
    )

    incoming_time = models.DateTimeField(
        verbose_name=_L('incoming time'),
        default=datetime.now,
    )

    outcoming_time = models.DateTimeField(
        verbose_name=_L('outcoming time'),
        blank=True,
        null=True,
    )

    is_opened = models.BooleanField(
        verbose_name=_L('is opened'),
        default=True
    )


    def save(self, force_insert=False, force_update=False):
        #verify if TICKET is already opened.
        if self.ticket:
            q = Selling.objects.filter(ticket=self.ticket, is_opened=True)
            assert q.count() <= 1, "System have tickets opened under same number: %d" % (self.ticket,) 
            if q.count() > 0 and q[0].id != self.id:
                raise ValidationError, "System has ticket already opened with %d" % (self.ticket,)
        # call the real save method
        super(Selling, self).save(force_insert, force_update)

    def __is_closed__(self):
        return not self.is_opened

    is_closed = property(__is_closed__)

    def __verify_is_closed__(self):
        now = datetime.now()
        if self.outcoming_time is None:
            return False
        if now >= self.outcoming_time:
            return True
        
        return False
        
    def close(self):
        if self.is_closed:
            return

        assert self.is_opened == True, "Selling should be opened to be closed"
        assert self.outcoming_time is None, "Outcoming time should be None on an opened selling"

        self.outcoming_time = datetime.now()
        self.is_opened = False
        self.save()
        # TODO: write user to log
        # TODO: refactor this by implement a decoration
        desc = _("Someone closed this selling")
        SellingHistory.objects.create(selling=self, description=desc)
        

    def reopen(self):
        if self.is_opened:
            return

        assert self.is_opened == False, "Selling should be closed to be reopened"
        assert self.outcoming_time is not None, "Outcoming time should be setted on a closed selling"

        self.outcoming_time = None
        self.is_opened = False
        self.save()
        # TODO: write user to log
        # TODO: refactor this by implement a decoration
        desc = _("Someone reopened this selling")
        SellingHistory.objects.create(selling=self, description=desc)


    def __unicode__(self):
        ticket_number = "None"
        if self.ticket:
            ticket_number = "%s" % (self.ticket,)
        return u'Selling [%d]|Ticket: [%s]' % (self.id, ticket_number)

    class Meta:
        verbose_name = _L('selling')
        verbose_name_plural = _L('sellings')
        ordering = ['is_paid','incoming_time', 'ticket']
        #abstract = True

class SellingProduct(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_L('product'),
    )
    selling = models.ForeignKey(
        Selling,
        verbose_name=_L('selling')
    )
    instructions = models.TextField(
        max_length=256, 
        blank=True,
        verbose_name=_L('special instuctions')
    )
    quantity = models.FloatField(
        verbose_name=_L('quantity'),
        default=float(1.0)
    )
    selling_unit_price = models.FloatField(
        verbose_name=_L('selling unit price'),
        default = float(0.00),
    )
    date = models.DateTimeField(
        verbose_name=_L('selling date'),
        default = datetime.now
    )
    def __unicode__(self):
        return u'Selling id %u of product %s' % (self.selling.id, self.product.name)

    class Meta:
        verbose_name = _L('selling product')
        verbose_name_plural = _L('selling products')
        ordering = ['selling', 'date', 'product']
        #abstract = True

class SellingProductIngredient(models.Model):
    ingredient_product = models.ForeignKey(
        IngredientProduct,
        verbose_name=_L('ingredient'),
    )

    selling_product = models.ForeignKey(
        SellingProduct,
        verbose_name=_L('selling product')
    )

    selling_price = models.FloatField(
        verbose_name=_L('selling unit price'),
        default = float(0.00),
    )
    
    class Meta:
        verbose_name = _L('selling product ingredient')
        verbose_name_plural = _L('selling product ingredients')
        ordering = ['selling_product', 'ingredient_product']
        #abstract = True


class SellingPayment(models.Model):
    selling = models.ForeignKey(
        Selling,
        verbose_name=_L("selling"),
    )
    client = models.ForeignKey(
        Client, 
        blank=True,
        null=True,
        verbose_name=_L("client"),
    )
    amount = models.FloatField(
        verbose_name=_L("amount")
    )
    is_credit = models.BooleanField(
        verbose_name=_L("is credit"),
        default=False
    )

    def __unicode__(self):
        return u'Selling %s |amount %f' % (self.selling.id, self.amount)

    class Meta:
        verbose_name = _L('selling payment')
        verbose_name_plural = _L('selling payments')
        ordering = ['selling', 'client']
        #abstract = True


#####################################################################


