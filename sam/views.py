from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .serializer import RegisterSerializer,ProductSerializer,RecentSearchSerializer,CustomerSerializer,CartSerializer
from .models import Customer, OTP,Product, RecentSearch,Wishlist,Cart
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q


class RegisterView(APIView):

    def post(self, request):

        try:
            serializer = RegisterSerializer(data=request.data)

            if serializer.is_valid():

                customer = serializer.save()

                otp_record = OTP.objects.create(
                    customer=customer
                )

                otp = otp_record.generate_otp()

                
                print("EMAIL =", repr(settings.EMAIL_HOST_USER))
                print("PASSWORD =", repr(settings.EMAIL_HOST_PASSWORD))

                send_mail(
                    "OTP Verification",
                    f"Your OTP is {otp}",
                    settings.EMAIL_HOST_USER,
                    [customer.email],
                    fail_silently=False
                )
                return Response({
                    "message": "OTP sent successfully"
                })

            return Response(serializer.errors)

        except Exception as e:

            return Response({
                "error": str(e)
            })
class VerifyOTPView(APIView):

    def post(self, request):

        return Response({
            "message": "OTP verified"
        })

class LoginView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:

            return Response({
                "error": "Invalid credentials"
            })

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
    

class ResendOTPView(APIView):

    def post(self, request):

        try:
            email = request.data.get("email")

            customer = Customer.objects.get(email=email)

            otp_record, created = OTP.objects.get_or_create(
                customer=customer
            )

            otp = otp_record.generate_otp()

            send_mail(
                "Resend OTP",
                f"Your OTP is {otp}",
                settings.EMAIL_HOST_USER,
                [customer.email],
                fail_silently=False
            )

            return Response({
                "message": "OTP resent successfully"
            })

        except Customer.DoesNotExist:

            return Response({
                "error": "Customer not found"
            })

        except Exception as e:

            return Response({
                "error": str(e)
            })
class ForgotPasswordView(APIView):

    def post(self, request):

        try:
            email = request.data.get("email")

            customer = Customer.objects.get(email=email)

            otp_record, created = OTP.objects.get_or_create(
                customer=customer
            )

            otp = otp_record.generate_otp()

            send_mail(
                "Password Reset OTP",
                f"Your OTP is {otp}",
                settings.EMAIL_HOST_USER,
                [customer.email],
                fail_silently=False
            )

            return Response({
                "message": "Password reset OTP sent"
            })

        except Customer.DoesNotExist:

            return Response({
                "error": "Customer not found"
            })

        except Exception as e:

            return Response({
                "error": str(e)
            })
        
class ResetPasswordView(APIView):

    def post(self, request):

        try:

            email = request.data.get("email")
            new_password = request.data.get("password")

            customer = Customer.objects.get(email=email)

            customer.password = new_password
            customer.save()

            return Response({
                "message": "Password changed successfully"
            })

        except Customer.DoesNotExist:

            return Response({
                "error": "Customer not found"
            })

        except Exception as e:

            return Response({
                "error": str(e)
            })
  


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated] # Requires a valid Bearer token

    def get(self, request):
        content = {'message': f'Hello, {request.user.username}! You are authenticated.'}
        return Response(content) 



class AdminLoginView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:

            return Response({
                "error": "Invalid credentials"
            })

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
class AddProductView(APIView):

    permission_classes = [IsAdminUser]

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "message": "Product added successfully"
            })

        return Response(serializer.errors)
    

class ProductListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        products = Product.objects.all()

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)
    
class ProductDetailView(APIView):

    def get(self, request, pk):

        product = Product.objects.get(id=pk)

        serializer = ProductSerializer(product)

        return Response(serializer.data)
class ProductDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        product = Product.objects.get(id=pk)

        serializer = ProductSerializer(product)

        return Response(serializer.data)

class AddToCartView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        product = Product.objects.get(id=product_id)

        cart, created = Cart.objects.get_or_create(
            customer=request.user,
            product=product
        )

        if created:

            cart.quantity = quantity
            cart.save()

            return Response({
                "message": "Product added to cart",
                "quantity": cart.quantity
            })

        cart.quantity = quantity
        cart.save()

        return Response({
            "message": "Cart quantity updated",
            "quantity": cart.quantity
        })
    
class AddToWishlistView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get("product_id")

        product = Product.objects.get(id=product_id)

        wishlist, created = Wishlist.objects.get_or_create(
            customer=request.user,
            product=product
        )

        product_data = ProductSerializer(product).data

        return Response({
            "message": "Added to wishlist",
            "wishlist_id": wishlist.id,
            "product": product_data
        })

class SearchProductView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        keyword = request.GET.get("q")

        products = Product.objects.filter(
            Q(name__icontains=keyword) |
            Q(description__icontains=keyword)
        )

        serializer = ProductSerializer(
            products,
            many=True
        )
        RecentSearch.objects.create(
            customer=request.user,
            keyword=keyword
        )

        return Response(serializer.data)

class RecentSearchView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        searches = RecentSearch.objects.filter(
            customer=request.user
        ).order_by('-searched_at')[:10]

        serializer = RecentSearchSerializer(
            searches,
            many=True
        )

        return Response(serializer.data)
    
class RecommendationView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        products = Product.objects.exclude(
            id__in=Cart.objects.filter(
                customer=request.user
            ).values_list(
                'product_id',
                flat=True
            )
        )[:5]

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)
    
class AdminProductListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        products = Product.objects.all()

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)
    
class UpdateProductView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, pk):

        product = Product.objects.get(id=pk)

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response({
                "message": "Product updated successfully",
                "data": serializer.data
            })

        return Response(serializer.errors)

class DeleteProductView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        product = Product.objects.get(id=pk)

        product.delete()

        return Response({
            "message": "Product deleted successfully"
        })
    

class UserListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        users = Customer.objects.all()

        serializer = CustomerSerializer(
            users,
            many=True
        )

        return Response(serializer.data)

class UserDetailView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        user = Customer.objects.get(id=pk)

        serializer = CustomerSerializer(user)

        return Response(serializer.data)

class AdminCartView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        carts = Cart.objects.all()

        serializer = CartSerializer(
            carts,
            many=True
        )

        return Response(serializer.data)
