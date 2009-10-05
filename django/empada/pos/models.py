from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from exceptions import DuplicateOpenedTicket, OperationNotPermited

FLOAT_PRECISION=0.0000001
# Create your models here.

#####################################################################
class Unit(models.Model):
    name = models.CharField(max_length=30,
        verbose_name=_("name")
    )
    TYPE_CHOICES = (
        ('I', _('Integer')),
        ('F', _('Fraction')),
    )

    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES, 
        verbose_name=_('type'),
        default='I'
    )

    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = _('unit')
        verbose_name_plural = _('units')
        ordering = ['type', 'name']
        #abstract = True


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
    unit = models.ForeignKey(
        Unit,
        verbose_name = _("unit")
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

    unit = models.ForeignKey(
        Unit,
        verbose_name = _("unit")
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
class SellingHistory(models.Model):
    selling = models.ForeignKey(
        'Selling', 
        verbose_name = _('selling')
    )
    description = models.CharField(
        max_length=30, 
        verbose_name=_('description')
    )
    date = models.DateTimeField(
        verbose_name=_('date'),
        default=datetime.now
    )

    def __unicode__(self):
        return u'Modification in [%s] on [%s]' % (self.selling, self.date,)

    class Meta:
        verbose_name = _('selling modification history')
        verbose_name_plural = _('selling modification histories')
        ordering = ['selling', 'date']
        #abstract = True

class Selling(models.Model):
    product = models.ManyToManyField(
        Product, 
        through='SellingProduct', 
        verbose_name=_('product')
    )

    ticket = models.IntegerField(
        verbose_name=_('ticket'),
        blank=True,
        null=True
    )

    is_paid = models.BooleanField(
        verbose_name=_('is paid'),
        default=False
    )

    amount_paid = models.FloatField(
        verbose_name=_('amount paid'), 
        default=float(0.00)
    )

    incoming_time = models.DateTimeField(
        verbose_name=_('incoming time'),
        default=datetime.now,
    )

    outcoming_time = models.DateTimeField(
        verbose_name=_('outcoming time'),
        blank=True,
        null=True,
    )

    is_opened = models.BooleanField(
        verbose_name=_('is opened'),
        default=True
    )

    def __amount__(self):
        amount = float(0.00)
        for sp in SellingProduct.objects.filter(selling=self):
            amount += sp.quantity * sp.selling_unit_price
        return amount
    
    amount = property(__amount__)

    def addProduct(self, product, quantity=1, instructions="", price=None):
        #print "On addProduct"
        if self.is_closed:
            raise OperationNotPermited, "Cannot add product to a closed selling"
        
        p = product.price
        if price:
            p = price
        # Product with integer units
        if product.unit.type == 'I':
            for i in range(0,quantity):
                #self.product.add(product, instructions=instructions, selling_unit_price=p)
                sp = SellingProduct(product=product, selling=self, instructions=instructions, selling_unit_price=p)
                sp.save()
        # product with fractional units
        else:
            sp = SellingProduct(product=product, selling=self, instructions=instructions, selling_unit_price=p, quantity=quantity)
            sp.save()

        return sp.id
            

    def save(self, force_insert=False, force_update=False):
        #verify if TICKET is already opened.
        if self.ticket:
            q = Selling.objects.filter(ticket=self.ticket, is_opened=True)
            assert q.count() <= 1, "System have tickets opened under same number: %d" % (self.ticket,) 
            if q.count() > 0 and q[0].id != self.id:
                raise DuplicateOpenedTicket, "System has a ticket already opened with ticket id %d" % (self.ticket,)
        # call the real save method
        super(Selling, self).save(force_insert, force_update)

    def __is_closed__(self):
        return not self.is_opened

    is_closed = property(__is_closed__)

    #def __verify_is_closed__(self):
    #    now = datetime.now()
    #    if self.outcoming_time is None:
    #        return False
    #    if now >= self.outcoming_time:
    #        return True
    #
    #    return False
        
    def close(self):
        if self.is_closed:
            raise OperationNotPermited, "Cannot close this selling because it is already closed"

        assert self.is_opened == True, "Selling should be opened to be closed"
        assert self.outcoming_time is None, "Outcoming time should be None on an opened selling"

        self.outcoming_time = datetime.now()
        self.is_opened = False
        self.save()
        # TODO: write user to log
        # TODO: refactor this by implement a decoration
        desc = ugettext("Someone closed this selling")
        SellingHistory.objects.create(selling=self, description=desc)
        
    close.alters_data = True

    def pay(self,amount=0.00):
        if self.is_closed:
            raise OperationNotPermited, "Cannot pay this selling because it is closed"
        if amount < 0:
            raise OperationNotPermited, "Cannot accept negative payments"

        # Programming errors
        assert amount > 0, "Amount to pay must be greater than 0"
        assert self.is_opened == True, "Selling should be opened to be paid"

        payment = SellingPayment.objects.create(selling=self, amount=amount)
        self.amount_paid += amount
        if not self.is_paid and (self.amount_paid >= self.amount or abs(self.amount_paid - self.amount) < FLOAT_PRECISION):
            self.is_paid = True
        
        self.save()

        return payment.id

    pay.alters_data = True    
    
    def reopen(self):
        if self.is_opened:
            raise OperationNotPermited, "Cannot reopen this selling because it is already opened"

        assert self.is_opened == False, "Selling should be closed to be reopened"
        assert self.outcoming_time is not None, "Outcoming time should be setted on a closed selling"

        if self.ticket:
            q = Selling.objects.filter(ticket=self.ticket, is_opened=True)
            assert q.count() <= 1, "System have tickets opened under same number: %d" % (self.ticket,) 
            if q.count() > 0:
                raise DuplicateOpenedTicket, "System has a ticket already opened with ticket id %d" % (self.ticket,)

        self.outcoming_time = None
        self.is_opened = True
        self.save()
        # TODO: write user to log
        # TODO: refactor this by implement a decoration
        desc = ugettext("Someone reopened this selling")
        SellingHistory.objects.create(selling=self, description=desc)

    reopen.alters_data = True


    def __unicode__(self):
        ticket_number = "None"
        if self.ticket:
            ticket_number = "%s" % (self.ticket,)
        return u'Selling [%d]|Ticket: [%s]' % (self.id, ticket_number)

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
        verbose_name=_('special instructions')
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
    date = models.DateTimeField(
        verbose_name=_("payment date"),
        default=datetime.now
    )
    def __unicode__(self):
        return u'Selling %s |amount %f' % (self.selling.id, self.amount)

    class Meta:
        verbose_name = _('selling payment')
        verbose_name_plural = _('selling payments')
        ordering = ['selling', 'client']
        #abstract = True


#####################################################################


