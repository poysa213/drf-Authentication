
from django.contrib.auth  import get_user_model


from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser



from .serializers import  UserSerializer, RegisterUserSerializer

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
                "user": UserSerializer(user,context=self.get_serializer_context()).data,
            })
        return Response(serializer.data, status=status.HTTP_401_BAD_REQUEST)

    


