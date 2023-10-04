from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from api.renderers import UserRenderer
from api.serializers import *
from projectone.models import Company
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from core.email_temp import send_password_reset_email, send_welcome_email


class UserProfileUpdate(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserProfileUpdate(data=request.data)
        fname = serializer.data.get('first_name')
        lname = serializer.data.get('last_name')
        
        user = User.objects.get(email=request.user.email)
        user.first_name = fname
        user.last_name = lname
        user.save()
        return Response({'message':'Profile Updated.'},status=status.HTTP_200_OK)
        
class UserResetPasswordView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        serializer = UserResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            try:
                User.objects.get(email=email)
                send_password_reset_email(email)
                return Response({'message':'Reset email sent.'},status=status.HTTP_200_OK)
            except:
                return Response({'email':'Email not found.'},status=status.HTTP_404_NOT_FOUND)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message':'User password changed!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = generate_user_token(user)
            email = serializer.validated_data.get('email')
            send_welcome_email(email)
            return Response({'message':'User created', 'token':token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            try:
                # check user email if exist or not
                user = User.objects.get(email=email)
                if user.check_password(password):
                    # if the user email is exist, check if the email and password match and if it does we login the user 
                    token = generate_user_token(user)
                    return Response({'message':'Login success', 'token':token},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':{'password':['Invalid Password']}},status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({'errors':{'email':['Email not found.']}},status=status.HTTP_404_NOT_FOUND)
            
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TopCompaniesView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, company_type):
        if company_type == "public":
            company = Company.objects.all()
            serializer = TopCompaniesSerializer(company,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif company_type == "private":
            company = Company.objects.filter(user=request.user)
            serializer = TopCompaniesSerializer(company,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class AddCompanyView(APIView):
    def post(self,request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            about = serializer.validated_data.get('name')
            Company.objects.create(name=name, about=about, user=request.user)
            return Response({"message":"Company Added"})
class DeleteCompanyView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def delete(self, request,slug):
        # serializer = TopCompanySerializer(data=request.data)
        # if serializer.is_valid():
            # slug = serializer.data.get('slug')
            print('slug-=---', slug)
            try:
                c = Company.objects.get(slug=slug,user=request.user)
                c.delete()
                # return Response({'message':'Comapny Deleted.'},status=status.HTTP_200_OK)
                return Response({'message':'Comapny Deleted'}, status=status.HTTP_200_OK)
            except Company.DoesNotExist:
                return Response({'message': 'Invalid request.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# generate token mannually
def generate_user_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }