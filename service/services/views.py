from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch, Sum
from django.core.cache import cache
from django.conf import settings

from services.models import Subscription
from services.serializers import SubscriptionSerializer
from clients.models import Client


class SubscriptionView(ReadOnlyModelViewSet):
    # подписанные клиенты (и план) сразу будут получены вместе с запросом подписки, не придется обращаться дважды
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        # select_related join`ит юзера и получаем примерно это: SELECT company_name, user.email FROM Client JOIN user
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
                                                                                     'user__email')))

    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        response = super().list(request, *args, **kwargs)  # super = ReadOnlyModelViewSet

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60 * 60)

        response_data = {'result': response.data}
        response_data['total_amount'] = price_cache
        response.data = response_data
        return response
