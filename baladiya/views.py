from django.shortcuts import render
from rest_framework import viewsets , status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, UserDetailsView
from rest_framework import generics
import random
from django.core.mail import send_mail
from rest_framework.response import Response
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter




class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailSerializer


class WilayaView(viewsets.ModelViewSet):
    queryset = Wilaya.objects.all()
    serializer_class = WilayaSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['name']
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']


class CommuneView(viewsets.ModelViewSet):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_fields = ['name','wilaya']
    filterset_fields = ['name','wilaya']
    search_fields = ['name','wilaya__id']
    ordering_fields = ['name','wilaya']

class ResetRequestView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordResetSerializer
    def post(self, request, *args, **kwargs):
        # return super().post(request, *args, **kwargs)
        data = request.data
        email = data['email']
        user = User.objects.get(email=email)
        if User.objects.filter(email=email).exists():
            user.otp = random.randint(1000, 9999)
            user.save()
            # send email with otp
            send_mail(
            'Réinisialiser Votre mot de passe',
            f'utilisez ce code :  {user.otp} pour réinitialiser votre mot de passe.',
            'from@baladiyatuna.com',
            [user.email],
            fail_silently=False,
            )
            message = {
                'detail': 'email de réinitialisation est envoyé'}
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {
                'detail': 'utilisateur avec cet email n existe pas'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.UpdateAPIView):
    serializer_class = PasswordResetConfirmSerializer
    queryset = User.objects.all()
    def update(self, request, *args, **kwargs):
        """reset_password with email, OTP and new password"""
        data = request.data
        user = User.objects.get(email=data['email'])
        new_password = data['new_password'] 
        new_password2 = data['new_password2'] 
        if user.is_active:
            # Check if otp is valid
            if data['otp'] == user.otp:
                if len(new_password) > 7:
                    if new_password == new_password2 :
                        # Change Password
                        user.set_password(data['new_password'])
                        user.otp = random.randint(1000, 9999)
                        user.save()
                        return Response(' vous avez réinitialisé votre mot de passe  ')
                    else :
                        return Response('les deux mot de passe ne sont pas identiques')  
                else:
                    message = {
                        'detail': 'Votre mot de passe est trop court'}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = {
                    'detail': 'OTP n est pas correcte'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {
                'detail': 'votre compte est désactivé'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class ManageUsersView(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('pk')
    serializer_class = ManagerUserSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['first_name','last_name','email','document','commune','phone','role','is_superuser', 'is_active','social_number','social_approved']
    filterset_fields = ['first_name','last_name','email','document','commune','phone','role','is_superuser', 'is_active','social_number','social_approved']
    search_fields = ['first_name','last_name','email','document','commune__id','phone','role','is_superuser', 'is_active','social_number','social_approved']
    ordering_fields = ['first_name','last_name','email','document','commune','phone','role','is_superuser', 'is_active','social_number','social_approved']

class FormationView(viewsets.ModelViewSet):
    serializer_class = FormationSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['date','localisation','owner','state']
    filterset_fields = ['date','localisation','owner','state']
    search_fields = ['owner__id','localisation','description','date','owner__id','title', 'created_at','state']
    ordering_fields = ['owner','date','title', 'created_at','state']
    def get_queryset(self):

        commune= self.request.user.commune
        return Formation.objects.filter(owner__commune = commune)

class AccompagnementView(viewsets.ModelViewSet):
    serializer_class = AccompagnementSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','type','state']
    filterset_fields = ['owner','type','state']
    search_fields = ['owner__id','title','description','created_at','type','state']
    ordering_fields = ['owner','title','created_at','state']
    def get_queryset(self):

        commune= self.request.user.commune
        return Accompagnement.objects.filter(owner__commune = commune)

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','topic__title']
    filterset_fields = ['owner','topic__title']
    search_fields = ['owner__id', 'content','created_at','topic__id']
    ordering_fields = ['owner','created_at']

class TopicView(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner', 'type', 'state']
    filter_fields = ['owner','type'] 
    search_fields = ['owner__id', 'title', 'description', 'created_at', 'type', 'state']
    ordering_fields = ['created_at', 'state']

    def get_queryset(self):
        commune= self.request.user.commune
        return Topic.objects.filter(owner__commune = commune)

class ActivityView(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','directed_by','state','type']
    filterset_fields = ['owner','directed_by','state','type']
    search_fields = ['owner__id','title','description','directed_by','date','created_at','state','type']
    ordering_fields = ['created_at','date','state','type']
    
    def get_queryset(self):

        commune= self.request.user.commune
        return Activity.objects.filter(owner__commune = commune)

class EcologicalInformationView(viewsets.ModelViewSet):
    serializer_class = EcologicalInformationSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','type','state']
    filterset_fields = ['owner','type','state']
    search_fields = ['owner__id','title','description','created_at','type','state']
    ordering_fields = ['created_at','date','state']
    
    def get_queryset(self):

        commune= self.request.user.commune
        return EcologicalInformation.objects.filter(owner__commune = commune)

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','action_type']
    filterset_fields = ['owner','action_type']
    search_fields = ['owner__id','name','description','created_at','action_type']
    ordering_fields = ['created_at','price']
    
    def get_queryset(self):

        commune= self.request.user.commune
        return Product.objects.filter(owner__commune = commune)

class ProductView(viewsets.ModelViewSet):
    serializer_class = AudianceDemandSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['owner','state']
    filterset_fields = ['owner','state']
    search_fields = ['owner__id','title','description','created_at','state','date']
    ordering_fields = ['created_at','date']
    
    def get_queryset(self):

        commune= self.request.user.commune
        return AudianceDemand.objects.filter(owner__commune = commune)