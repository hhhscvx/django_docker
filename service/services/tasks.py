from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F
import time
import datetime
from django.db import transaction


# создаем таску из любой даппки
@shared_task(base=Singleton)  # вызываем из models при сохранении
def set_price(subscription_id):
    from services.models import Subscription

    with transaction.atomic():  # Все save`ы применятся вместе в конце, либо все не применятся

        # подписку эта таска получит, только когда отработает та, что получила его раньше. Это из-за того, что строка с select_for_update лочится
        subscription = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
            annotated_price=F('service__price_to_subscribe')
            - F('service__price_to_subscribe') * F('plan__discount_percent') / 100.00
        ).first()

        subscription.price = subscription.annotated_price  # поменяли прайс и сохранили
        subscription.save()


@shared_task(base=Singleton)
def set_comment(subscription_id):
    from services.models import Subscription

    with transaction.atomic():  # код внутри не будет работать параллельно

        subscription = Subscription.objects.select_for_update().get(id=subscription_id)

        subscription.comment = str(datetime.datetime.now())  # просто для примера
        subscription.save()
