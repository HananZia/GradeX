from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from gradex_app.models import CustomUser
from django.contrib import messages
# class EmailBackEnd(ModelBackend):
#     def authenticate(self,username=None, password=None, **kwargs):
#         UserModel=get_user_model()
#         try:
#             user = CustomUser.objects.filter(email=username).first()
            
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None
    
#     from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model
# from django.conf import settings

class EmailBackEnd(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        # Try to find the user by email
        user = CustomUser.objects.filter(email=username).first()
        
        if user is None:
            # If user is not found, set a message to be displayed
            if request:
                messages.error(request, "User with this email does not exist.")
            return None
        
        # Check if the password is correct
        if user.check_password(password):
            return user
        
        # If password is incorrect
        if request:
            messages.error(request, "Incorrect password.")
        return None
