from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch, F, Sum
from services.models import Subscription
from services.serializers import SubscriptionSerializer
from clients.models import Client


class SubscriptionView(ReadOnlyModelViewSet):
    # подписанные клиенты (и план) сразу будут получены вместе с запросом подписки, не придется обращаться дважды
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        # select_related join`ит юзера и получаем примерно это: SELECT company_name, user.email FROM Client JOIN user
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
                                                                                     'user__email'))
    ).annotate(price=F('service__price_to_subscribe')  # вычисляем поле price
               - F('service__price_to_subscribe')  # F - ссылка на поле модели
               * F('plan__discount_percent') / 100.00)  # Получается наша хуйня в селекте в виде: `формула` AS price

    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):  # в этом методе обр. запрос и формируется ответ клиенту
        queryset = self.filter_queryset(self.get_queryset())

        response = super().list(request, *args, **kwargs)  # super = ReadOnlyModelViewSet

        response_data = {'result': response.data}  # aggregate это SELECT SUM('price') из этого же queryset`а
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')  # получаем словарь -> get
        response.data = response_data  # был обычный json словарь, стал список в ключе result
        # в aggregate мы можем строить даже подобную хуйню: aggregate(total=Sum('price'), total2=Sum('plan_id')).
        return response
