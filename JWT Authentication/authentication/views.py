
from django.contrib.auth  import get_user_model
from django.core.mail import send_mail


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.permissions import AllowAny, IsAuthenticated



from .serializers import  UserSerializer, RegisterUserSerializer, ChangePasswordSerializer, UserProfileSerializer
from .models import OTP
from .utils import get_otp

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data, context = {"request": self.request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                "messge": "New user was Created successfully",
                "user": UserSerializer(user,context=self.get_serializer_context()).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_401_BAD_REQUEST)

    



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args,  **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context = {"user": self.request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save(validated_data=serializer.validated_data)
            return Response({
                "messge": "Password was changed successfully"
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.data, status=status.HTTP_401_BAD_REQUEST)


class AuthTest(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"msg":"auth confirmed"})
    

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = OTP.objects.filter(user=user).first()
            if otp:
                otp.delete()
            code = get_otp()
            OTP.objects.create(code=code, user=user)
            send_mail(
                'Reset Password OTP',
                f'Your OTP code is {code}',
                'poysa213@gmail.com',
                [email],
                fail_silently=False,
            )
            return Response({'message':'OTP code sent successfully'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error':'No such user found with this email!'}, status=status.HTTP_404_NOT_FOUND)
            