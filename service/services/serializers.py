from rest_framework import serializers
from services.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('__all__')


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer() # теперь имеем доступ ко всем полям Plan через объект plan

    # client_name будет равняться client.company_name
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    price = serializers.SerializerMethodField()  # значение будет присвоено методу с префиксом get_

    def get_price(self, instance):  # instance = subscription
        return instance.price  # присвоили в annotate в запросе

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')
