# lscms/lscms/views.py

from rest_framework import viewsets
from .models import HeaderBlock, FooterBlock, AdBlock, SEOSettings, MenuItem, MarketingCampaign, NotificationMessage, LayoutSettings, AnalyticsSettings
from .serializers import HeaderBlockSerializer, FooterBlockSerializer, AdBlockSerializer, SEOSettingsSerializer, MenuItemSerializer, MarketingCampaignSerializer, NotificationMessageSerializer, LayoutSettingsSerializer, AnalyticsSettingsSerializer
from rest_framework.permissions import IsAuthenticated  # Modify with other permission class
from .permissions import IsAdminOrReadOnly

# HeaderBlock ViewSet
class HeaderBlockViewSet(viewsets.ModelViewSet):
    queryset = HeaderBlock.objects.all()
    serializer_class = HeaderBlockSerializer
    permission_classes = [IsAdminOrReadOnly]

# FooterBlock ViewSet
class FooterBlockViewSet(viewsets.ModelViewSet):
    queryset = FooterBlock.objects.all()
    serializer_class = FooterBlockSerializer
    permission_classes = [IsAdminOrReadOnly]

# AdBlock ViewSet
class AdBlockViewSet(viewsets.ModelViewSet):
    queryset = AdBlock.objects.all()
    serializer_class = AdBlockSerializer
    permission_classes = [IsAdminOrReadOnly]

# SEOSettings ViewSet
class SEOSettingsViewSet(viewsets.ModelViewSet):
    queryset = SEOSettings.objects.all()
    serializer_class = SEOSettingsSerializer
    permission_classes = [IsAdminOrReadOnly]

# MenuItem ViewSet
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

# MarketingCampaign ViewSet
class MarketingCampaignViewSet(viewsets.ModelViewSet):
    queryset = MarketingCampaign.objects.all()
    serializer_class = MarketingCampaignSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = MarketingCampaign.objects.filter(is_active=True)
        platform = self.request.query_params.get('platform', None)
        location = self.request.query_params.get('location', None)

        if platform:
            queryset = queryset.filter(target_platforms__contains=[platform])
        if location:
            queryset = queryset.filter(target_locations__contains=[location])
        
        return queryset.order_by('-priority')

# NotificationMessage ViewSet
class NotificationMessageViewSet(viewsets.ModelViewSet):
    queryset = NotificationMessage.objects.all()
    serializer_class = NotificationMessageSerializer
    permission_classes = [IsAdminOrReadOnly]

# LayoutSettings ViewSet
class LayoutSettingsViewSet(viewsets.ModelViewSet):
    queryset = LayoutSettings.objects.all()
    serializer_class = LayoutSettingsSerializer
    permission_classes = [IsAdminOrReadOnly]

# AnalyticsSettings ViewSet
class AnalyticsSettingsViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsSettings.objects.all()
    serializer_class = AnalyticsSettingsSerializer
    permission_classes = [IsAdminOrReadOnly]

