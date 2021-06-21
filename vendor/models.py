import shortuuid
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.


class DateMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Account(models.Model):
    class Meta:
        db_table = 'account'
        verbose_name_plural = 'accounts'

    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)


class Vendor(DateMixin):
    class Meta:
        db_table = 'vendor'
        verbose_name_plural = 'vendors'
        ordering = ['-created_at']

    name = models.CharField(max_length=30, null=False, blank=False)
    phone = models.CharField(max_length=15, unique=True,
                             validators=[RegexValidator(regex=r"^(\+?[\d]{2,3}\-?)?[\d]{8,10}$")])
    address = models.CharField(max_length=30, null=False, blank=False)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(DateMixin):
    class Meta:
        db_table = 'product'
        verbose_name_plural = 'products'
        ordering = ['-created_at']

    CURRENCY = [
        ('RS', 'RS'),
        ('INR', 'INR'),
        ('USD', 'USD'),
    ]

    name = models.CharField(max_length=30, null=False, blank=False)
    currency = models.CharField(
        max_length=3, choices=CURRENCY, blank=False, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.PositiveBigIntegerField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_img/', null=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.vendor.name)


class Transaction(DateMixin):
    class Meta:
        db_table = 'transaction'
        verbose_name_plural = 'transactions'
        ordering = ['-created_at']

    name = models.CharField(max_length=30, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    invoice_number = models.CharField(max_length=8, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=5, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        ''' On save, create invoice number '''
        if not self.invoice_number:
            self.invoice_number = shortuuid.ShortUUID().random(length=8)
        if not self.total_amount:
            self.total_amount = self.product.price * self.quantity
        return super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number
