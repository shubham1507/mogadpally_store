from django.urls import path
from .views import CreateOrderView, OrderListView, OrderDetailView, CancelOrderView

urlpatterns = [
    path("", CreateOrderView.as_view(), name="order-create"),
    path("list", OrderListView.as_view(), name="order-list"),
    path("<uuid:pk>", OrderDetailView.as_view(), name="order-detail"),
    path("<uuid:pk>/cancel", CancelOrderView.as_view(), name="order-cancel"),
]
