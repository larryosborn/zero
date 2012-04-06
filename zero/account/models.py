from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from zero.company.models import Company, Price

class Account(models.Model):
    user    = models.ForeignKey(User, unique=True)
    balance = models.FloatField(default=0)

    def buy(self, company, quantity):
        price = company.latest_price();
        cost = quantity * price
        if self.balance < cost:
            return False
        try:
            asset = Asset.objects.get(company=company, user=self.user)
            asset.quantity = asset.quantity + quantity
        except:
            asset = Asset.objects.create(company=company, user=self.user, quantity=quantity)

        asset.save()
        self.balance = self.balance - cost
        self.save()
        date = datetime.now()
        transaction = Transaction.objects.create(company=company, quantity=quantity, user=self.user, date=date, category='buy', price=price)
        return True

    def sell(self, company, quantity):
        price = company.latest_price();
        try:
            asset = Asset.objects.get(company=company, user=self.user)
        except:
            return False
        if asset.quantity < quantity:
            quantity = asset.quantity
        asset.quantity = asset.quantity - quantity
        if asset.quantity == 0:
            asset.delete()
        else:
            asset.save()
        cost = quantity * price
        self.balance = self.balance + cost
        self.save()
        date = datetime.now()
        transaction = Transaction.objects.create(company=company, quantity=quantity, user=self.user, date=date, category='sell', price=price)
        return True

    def __unicode__(self):
        return '%s %s %s' % (self.user.email, self.user.first_name, self.user.last_name)

User.account = property(lambda u: Account.objects.get_or_create(user=u)[0])

class Asset(models.Model):
    company     = models.ForeignKey(Company)
    quantity    = models.FloatField(default=0)
    user        = models.ForeignKey(User)

    def value(self):
        price = Price.objects.order_by('-date').filter(company=self.company)[:1].get()
        return self.quantity * price.closed

    def __unicode__(self):
        return '%i x %s' % (self.quantity, self.company.symbol)

class Transaction(models.Model):

    CATEGORY_CHOICES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )

    company     = models.ForeignKey(Company)
    quantity    = models.FloatField(default=0)
    user        = models.ForeignKey(User)
    date        = models.DateTimeField()
    category    = models.CharField(max_length=8, choices=CATEGORY_CHOICES)
    price       = models.FloatField(default=0)

    def value(self):
        return self.quantity * self.price

    def current_value(self):
        price = Price.objects.order_by('-date').filter(company=self.company)[:1].get()
        return self.quantity * price.closed

    def __unicode__(self):
        return '%i x %s @ %i = $%i (%s)' % (self.quantity, self.company.symbol, self.price, (self.quantity * self.price), self.date)

