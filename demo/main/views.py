from demo.main.serializers import RegistrationSerializer
from rest_framework import generics, status
from rest_framework.response import Response

# Create your views here.

class RegistrationView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        
        return Response(user_data, status=status.HTTP_201_CREATED)