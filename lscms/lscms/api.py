# lscms/api.py

from rest_framework.routers import DefaultRouter
from .views import (
    HeaderBlockViewSet,
    FooterBlockViewSet,
    AdBlockViewSet,
    SEOSettingsViewSet,
    MenuItemViewSet,
    MarketingCampaignViewSet,
    NotificationMessageViewSet,
    LayoutSettingsViewSet,
    AnalyticsSettingsViewSet
)

# Create the API router
api_router = DefaultRouter()

# Register all endpoints
api_router.register(r'header-blocks', HeaderBlockViewSet, basename='header-block')
api_router.register(r'footer-blocks', FooterBlockViewSet, basename='footer-block')
api_router.register(r'ad-blocks', AdBlockViewSet, basename='ad-block')
api_router.register(r'seo-settings', SEOSettingsViewSet, basename='seo-setting')
api_router.register(r'menu-items', MenuItemViewSet, basename='menu-item')
api_router.register(r'marketing-campaigns', MarketingCampaignViewSet, basename='marketing-campaign')
api_router.register(r'notifications', NotificationMessageViewSet, basename='notification')
api_router.register(r'layout-settings', LayoutSettingsViewSet, basename='layout-setting')
api_router.register(r'analytics-settings', AnalyticsSettingsViewSet, basename='analytics-setting')
