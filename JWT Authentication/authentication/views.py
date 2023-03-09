
from django.contrib.auth  import get_user_model


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.permissions import AllowAny, IsAuthenticated



from .serializers import  UserSerializer, RegisterUserSerializer, ChangePasswordSerializer, UserProfileSerializer

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
                "msg": "New user was Created successfully",
                "user": UserSerializer(user,context=self.get_serializer_context()).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_401_BAD_REQUEST)

    



class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args,  **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data, context = {"user": self.request.user})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                "status": status.HTTP_201_CREATED,
                "msg": "Password was changed successfully"
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.data, status=status.HTTP_401_BAD_REQUEST)


class AuthTest(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"msg":"auth confirmed"})
    

# class ProfileView(generics.ListAPIView):
#     serializer_class = UserProfileSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return User.objects.filter(user_id=self.request.user.id)
