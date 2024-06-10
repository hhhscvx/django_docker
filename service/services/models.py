from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client
from services.tasks import set_price, set_comment
from django.db.models.signals import post_delete
from .receivers import delete_cache_total_sum


class Service(models.Model):
    """Сервис с названием и ценой"""
    name = models.CharField(max_length=50)
    price_to_subscribe = models.PositiveIntegerField()

    def __str__(self):
        return f"Service: {self.name}"


class Plan(models.Model):
    """Тариф сервиса, который определяет скидку"""
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_type = models.CharField(choices=PLAN_TYPES,
                                 max_length=10,
                                 default='full')
    discount_percent = models.PositiveIntegerField(default=0,
                                                   validators=[
                                                       MaxValueValidator(100)
                                                   ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def __str__(self):
        return f"Plan type: {self.plan_type}"
    
    def save(self, *args, **kwargs):

        if self.discount_percent != self.__discount_percent: # если поменяли скидку - пересчитываем
            for subscription in self.subscriptions.all(): # related_name=subscriptions!
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)
        
        return super().save(*args, **kwargs)


class Subscription(models.Model):
    """Подписка. Связывает клиента, сервис, 
    на который он оформил подписку, и тарифный план"""

    client = models.ForeignKey(Client,  # client.subscriptions.all()
                               related_name='subscriptions',
                               on_delete=models.CASCADE)
    service = models.ForeignKey(Service,
                               related_name='subscriptions',
                               on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan,
                               related_name='subscriptions',
                               on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=50, default="")
    
    def __str__(self):
        return f"{self.client.company_name} subsc on {self.service.name} by {self.plan.plan_type}"
    
    def save(self, *args, **kwargs):
        creating = not bool(self.pk)
        
        result = super().save(*args, **kwargs)
        if creating:
            set_price.delay(self.id)
        
        return result

post_delete.connect(delete_cache_total_sum, sender=Subscription)
