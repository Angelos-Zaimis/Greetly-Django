import json
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from custom_user.serializer import UserSerializer
import jwt
from datetime import datetime, timedelta

User = get_user_model()





# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('email')
        user = User.objects.get(email=username)
        is_first_login = user.first_login

        if is_first_login:
            # Update the user's first_login field in the database
            user.first_login = False
            user.save()


        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(minutes=60)  # token expires in 60 minutes
        }
        token = jwt.encode(payload, 'SECRET_KEY')

        data = {
            'message': 'Successful login.',
            'username': user.email,
            'token': token,
            'first_login': is_first_login
        }

        return HttpResponse(json.dumps(data), content_type='application/json', status=200)
