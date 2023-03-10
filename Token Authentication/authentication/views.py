
from django.contrib.auth  import get_user_model


from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from authentication.serializers import LoginUserSerializer, UserSerializer, RegisterSerializer, RegisterAdminSerializer

User = get_user_model()
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            _, token = AuthToken.objects.create(user)
            return Response({
                "user": UserSerializer(user,context=self.get_serializer_context()).data,
                "token":  token
            })
        return Response(serializer.data, status=status.HTTP_401_BAD_REQUEST)



class LoginView(KnoxLoginView):
    serializer_class = LoginUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        }) 

    


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
class RegisterAdminView(generics.CreateAPIView):
    serializer_class = RegisterAdminSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
