
from django.contrib.auth  import get_user_model


from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import AllowAny, IsAuthenticated



from .serializers import  UserSerializer, RegisterUserSerializer, ChangePasswordSerializer

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

    def put(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data, context = {"user": self.request.user})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                "msg": "Password was changed successfully"
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.data, status=status.HTTP_401_BAD_REQUEST)
