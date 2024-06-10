from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F
import time


@shared_task(base=Singleton)  # создаем таску из любой даппки
def set_price(subscription_id):
    from service.services.models import Subscription
    time.sleep(5)

    subscription = Subscription.objects.filter(id=subscription_id).annotate(annotated_price=F('service__price_to_subscribe')
                                                                            - F('service__price_to_subscribe')
                                                                            * F('plan__discount_percent') / 100.00).first()
    subscription.price = subscription.annotated_price  # поменяли прайс и сохранили
    subscription.save()
