from django.urls import path
from .views import *

urlpatterns = [
    path('place-order/',PlaceOrderView.as_view()),
    path('payment/',PaymentView.as_view()),
    path('order-history/',OrderHistoryView.as_view()),
    path('track-order/<int:pk>/',TrackOrderView.as_view()),
    path('admin/orders/',AdminOrderView.as_view()),
    path('admin/order-status/<int:pk>/',UpdateOrderStatusView.as_view()),
    path('create-payment/',CreatePaymentView.as_view()),
    path('verify-payment/',VerifyPaymentView.as_view()),
    path('payment-history/',PaymentHistoryView.as_view()),
    path(
    'payment-history/',
    PaymentHistoryView.as_view()
),
    

]

