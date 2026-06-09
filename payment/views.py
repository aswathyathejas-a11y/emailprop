from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from rest_framework.permissions import IsAdminUser

from sam import serializer
from .serializer import OrderSerializer,PaymentSerializer
from sam.models import Cart
from .models import Order, OrderItem,Payment
import razorpay
from django.conf import settings
import uuid


class PlaceOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        carts = Cart.objects.filter(
            customer=request.user
        )

        if not carts.exists():
            return Response({
                "message": "Cart is empty"
            })

        total = Decimal("0.00")

        for cart in carts:
            total += cart.product.price * cart.quantity

        order = Order.objects.create(
            customer=request.user,
            order_number=str(uuid.uuid4())[:8].upper(),
            total_amount=total
        )

        for cart in carts:

            OrderItem.objects.create(
                order=order,
                product=cart.product,
                quantity=cart.quantity,
                price=cart.product.price
            )

        carts.delete()

        serializer = OrderSerializer(order)
        print("Logged User:", request.user)
        print("User ID:", request.user.id)

        carts = Cart.objects.filter(customer=request.user)

        print("Cart Count:", carts.count())

        return Response({
            "message": "Order placed successfully",
            "order": serializer.data
 })
        

class PaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        order_id = request.data.get("order_id")

        order = Order.objects.get(
            id=order_id,
            customer=request.user
        )

        order.payment_status = "paid"
        order.save()

        return Response({
            "message": "Payment successful",
            "order_id": order.id,
            "payment_status": order.payment_status
        })
    


class OrderHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        orders = Order.objects.filter(
            customer=request.user
        ).order_by('-created_at')

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)
    
class TrackOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        order = Order.objects.get(
            id=pk,
            customer=request.user
        )

        serializer = OrderSerializer(order)

        return Response(serializer.data)
    
class AdminOrderView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        orders = Order.objects.all()

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)

class UpdateOrderStatusView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, pk):

        order = Order.objects.get(id=pk)

        order.status = request.data.get("status")

        order.save()

        return Response({
            "message": "Order status updated",
            "status": order.status
        })

class CreatePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        order_id = request.data.get("order_id")

        order = Order.objects.get(
            id=order_id,
            customer=request.user
        )

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        payment_data = {
            "amount": int(order.total_amount * 100),
            "currency": "INR",
            "receipt": str(order.id)
        }

        razorpay_order = client.order.create(
            payment_data
        )

        Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order["id"],
            amount=order.total_amount
        )

        return Response({
            "message": "Payment order created",
            "razorpay_order_id": razorpay_order["id"],
            "amount": order.total_amount
        })
class VerifyPaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        razorpay_order_id = request.data.get(
            "razorpay_order_id"
        )

        razorpay_payment_id = request.data.get(
            "razorpay_payment_id"
        )

        payment = Payment.objects.get(
            razorpay_order_id=razorpay_order_id
        )

        payment.razorpay_payment_id = (
            razorpay_payment_id
        )

        payment.status = "paid"

        payment.save()

        order = payment.order

        order.payment_status = "paid"

        order.status = "confirmed"

        order.save()

        return Response({
            "message": "Payment verified",
            "payment_status": payment.status
        })
class PaymentHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        payments = Payment.objects.filter(
            order__customer=request.user
        )

        data = []

        for payment in payments:

            data.append({
                "order_id": payment.order.id,
                "amount": payment.amount,
                "status": payment.status,
                "razorpay_order_id":
                payment.razorpay_order_id
            })

        return Response(data)

