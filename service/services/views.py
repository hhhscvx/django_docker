from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch
from services.models import Subscription
from services.serializers import SubscriptionSerializer
from clients.models import Client


class SubscriptionView(ReadOnlyModelViewSet):
    # подписанные клиенты сразу будут получены вместе с запросом подписки, не придется обращаться дважды
    queryset = Subscription.objects.all().prefetch_related(
        # select_related join`ит юзера и получаем примерно это: SELECT company_name, user.email FROM Client JOIN user
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
                                                                                     'user__email')))
    serializer_class = SubscriptionSerializer
