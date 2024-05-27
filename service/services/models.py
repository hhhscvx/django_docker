from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client


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

    def __str__(self):
        return f"Plan type: {self.plan_type}"


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
    
    def __str__(self):
        return f"{self.client.company_name} subsc on {self.service.name} by {self.plan.plan_type}"
