from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .serializer import RegisterSerializer
from .models import Customer, OTP
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
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

        return Response({
            "message": "Login success"
        })