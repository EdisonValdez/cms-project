# lscms/lscms/serializers.py

from rest_framework import serializers
from .models import (HeaderBlock, FooterBlock, 
AdBlock, SEOSettings, MenuItem, 
MarketingCampaign, NotificationMessage, LayoutSettings, AnalyticsSettings
)
class HeaderBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderBlock
        fields = '__all__'  # Include all fields in the serialization

class FooterBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterBlock
        fields = '__all__'

class AdBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdBlock
        fields = '__all__'

class SEOSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOSettings
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class MarketingCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingCampaign
        fields = '__all__'
    
class NotificationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationMessage
        fields = '__all__'

class LayoutSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayoutSettings
        fields = '__all__'

class AnalyticsSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsSettings
        fields = '__all__'

