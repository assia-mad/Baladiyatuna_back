from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, UserDetailsView, PasswordChangeView
from rest_framework import generics
import random
from django.core.mail import send_mail
from rest_framework.response import Response
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend,BaseInFilter, CharFilter
from rest_framework.filters import SearchFilter, OrderingFilter, BaseFilterBackend 
from django.db.models.functions import TruncDate
import datetime
from rest_framework.exceptions import ParseError
from django.utils.dateparse import parse_date
import django_filters
from rest_framework.views import APIView



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
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filter_fields = ["name"]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]


class CommuneView(viewsets.ModelViewSet):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filter_fields = ["name", "wilaya"]
    filterset_fields = ["name", "wilaya"]
    search_fields = ["name", "wilaya__id"]
    ordering_fields = ["name", "wilaya"]


class ResetRequestView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        # return super().post(request, *args, **kwargs)
        data = request.data
        email = data["email"]
        user = User.objects.get(email=email)
        if User.objects.filter(email=email).exists():
            user.otp = random.randint(1000, 9999)
            user.save()
            # send email with otp
            send_mail(
                "Réinisialiser Votre mot de passe",
                f"utilisez ce code :  {user.otp} pour réinitialiser votre mot de passe.",
                "from@baladiyatuna.com",
                [user.email],
                fail_silently=False,
            )
            message = {"detail": "email de réinitialisation est envoyé"}
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {"detail": "utilisateur avec cet email n existe pas"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.UpdateAPIView):
    serializer_class = PasswordResetConfirmSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        """reset_password with email, OTP and new password"""
        data = request.data
        user = User.objects.get(email=data["email"])
        new_password = data["new_password"]
        new_password2 = data["new_password2"]
        if user.is_active:
            if data["otp"] == user.otp:
                if len(new_password) > 7:
                    if new_password == new_password2:
                        # Change Password
                        user.set_password(data["new_password"])
                        user.otp = random.randint(1000, 9999)
                        user.save()
                        return Response(" vous avez réinitialisé votre mot de passe  ")
                    else:
                        return Response("les deux mot de passe ne sont pas identiques")
                else:
                    message = {"detail": "Votre mot de passe est trop court"}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = {"detail": "OTP n est pas correcte"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {"detail": "votre compte est désactivé"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ManageUsersView(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("pk")
    serializer_class = ManagerUserSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = [
        "first_name",
        "last_name",
        "email",
        "commune",
        "phone",
        "role",
        "is_superuser",
        "is_active",
        "social_approved",
    ]
    filterset_fields = [
        "first_name",
        "last_name",
        "email",
        "commune",
        "phone",
        "role",
        "is_superuser",
        "is_active",
        "social_approved",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "email",
        "commune__id",
        "phone",
        "role",
        "is_superuser",
        "is_active",
        "social_approved",
    ]
    ordering_fields = [
        "first_name",
        "last_name",
        "email",
        "commune",
        "phone",
        "role",
        "is_superuser",
        "is_active",
        "social_approved",
    ]

class FormationView(viewsets.ModelViewSet):
    serializer_class = FormationSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter ]
    filter_fields = ["state","type","owner__role"]
    filterset_fields = [ "state","type","owner__role"]
    search_fields = [
        "owner__id",
        "localisation",
        "description",
        "date",
        "owner__id",
        "title",
        "created_at",
        "state",
    ]
    ordering_fields = ["owner", "date", "title", "created_at", "state"]

    def get_queryset(self):
        commune = self.request.user.commune
        return Formation.objects.filter(owner__commune=commune)


class AccompagnementView(viewsets.ModelViewSet):
    serializer_class = AccompagnementSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["owner__role", "type"]
    filterset_fields = ["owner__role", "type"]
    search_fields = ["owner__id", "title", "description", "created_at", "type"]
    ordering_fields = ["owner", "title", "created_at"]

    def get_queryset(self):
        commune = self.request.user.commune
        return Accompagnement.objects.filter(owner__commune=commune)


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["owner", "discussion"]
    filterset_fields = ["owner", "discussion"]
    search_fields = ["owner__id", "content", "created_at", "discussion__id"]
    ordering_fields = ["owner", "created_at"]


class TopicView(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner__role", "type", "state"]
    filter_fields = ["owner__role", "type"]
    search_fields = ["owner__id", "title", "description", "created_at", "type", "state"]
    ordering_fields = ["created_at", "state"]

    def get_queryset(self):
        commune = self.request.user.commune
        return Topic.objects.filter(owner__commune=commune)


class ActivityView(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["owner__role", "directed_by", "type"]
    filterset_fields = ["owner__role", "directed_by", "type"]
    search_fields = [
        "owner__id",
        "title",
        "description",
        "directed_by",
        "date",
        "created_at",
        "type",
    ]
    ordering_fields = ["created_at", "date", "type"]

    def get_queryset(self):
        commune = self.request.user.commune
        return Activity.objects.filter(owner__commune=commune)


class EcologicalInformationView(viewsets.ModelViewSet):
    serializer_class = EcologicalInformationSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["owner__role", "type"]
    filterset_fields = ["owner__role", "type"]
    search_fields = ["owner__id", "title", "description", "created_at", "type"]
    ordering_fields = ["created_at", "date"]

    def get_queryset(self):
        commune = self.request.user.commune
        return EcologicalInformation.objects.filter(owner__commune=commune)


class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["owner", "action_type"]
    filterset_fields = ["owner", "action_type"]
    search_fields = ["owner__id", "name", "description", "created_at", "action_type"]
    ordering_fields = ["created_at", "price"]

    def get_queryset(self):
        commune = self.request.user.commune
        return Product.objects.filter(owner__commune=commune)


class AudianceDemandView(viewsets.ModelViewSet):
    serializer_class = AudianceDemandSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["owner__role", "state"]
    filterset_fields = ["owner__role", "state"]
    search_fields = ["owner__id", "title", "description", "created_at", "state", "date"]
    ordering_fields = ["created_at", "date"]

    def get_queryset(self):
        commune = self.request.user.commune
        return AudianceDemand.objects.filter(owner__commune=commune)

class AgendaView(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ["owner__role","date__date"]
    filterset_fields = ["owner__role","date__date"]
    search_fields = ["owner__id", "title", "description", "created_at", "date","localisation"]
    ordering_fields = ["created_at", "date"]

class DiscussionView(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner", "type", "state"]
    filter_fields = ["owner", "type"]
    search_fields = ["owner__id", "title", "description", "created_at", "type", "state"]
    ordering_fields = ["created_at", "state"]

class SocialinformationView(viewsets.ModelViewSet):
    queryset = SocialInformation.objects.all()
    serializer_class = SocialInformationSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner__role","title"]
    filter_fields = ["owner__role"]
    search_fields = ["owner__id", "title", "description", "created_at"]
    ordering_fields = ["created_at"]

class DangerInformationView(viewsets.ModelViewSet):
    queryset= DangerInformation.objects.all()
    serializer_class = DangerInformationSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner__role","state","type"]
    filter_fields = ["owner__role","state","type"]
    search_fields = ["owner__id", "title", "description", "created_at","type"]
    ordering_fields = ["created_at"]

class VisiteView(viewsets.ModelViewSet):
    queryset= Visite.objects.all()
    serializer_class = VisiteSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner__role","state","liked_by","commune"]
    filter_fields = ["owner__role","state","liked_by","commune"]
    search_fields = ["owner__id", "title", "description", "created_at","liked_by","localisation","commune"]
    ordering_fields = ["created_at"]

class HistoriqueFilter(django_filters.FilterSet):
    commune = django_filters.NumberFilter(field_name='commune')

    class Meta:
        model = Historique
        fields = ['commune','state']

class HistoriqueListCreateView(generics.ListCreateAPIView):
    queryset = Historique.objects.all()
    serializer_class = HistoriqueSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = HistoriqueFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["state"]
    filter_fields = ["state"]
    ordering_fields = ["date", "commune"]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class HistoriqueRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Historique.objects.all()
    serializer_class = HistoriqueSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = HistoriqueFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ["date", "commune"]
    filterset_fields = ["state"]
    filter_fields = ["state"]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EmergencyFunctionsView(viewsets.ModelViewSet):
    queryset= EmergencyFunctions.objects.all()
    serializer_class = EmergencyFunctionsSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner__role","state","type"]
    filter_fields = ["owner__role","state","type"]
    search_fields = ["owner__id", "title", "description", "created_at","type"]
    ordering_fields = ["created_at"]



class AlbumView(viewsets.ModelViewSet):
    queryset= Album.objects.all()
    serializer_class = AlbumSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner__role","state","commune"]
    filter_fields = ["owner__role","state","commune"]
    search_fields = ["owner__id","name","state","commune"]
    ordering_fields = ["created_at"]

class ActualityView(viewsets.ModelViewSet):
    queryset= Actuality.objects.all()
    serializer_class = ActualitySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner__role","state","type"]
    filter_fields = ["owner__role","state","type"]
    search_fields = ["owner__id","title", "description","state","type","created_at"]
    ordering_fields = ["created_at"]

class StudyView(viewsets.ModelViewSet):
    queryset= Study.objects.all()
    serializer_class = StudySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner__role","state"]
    filter_fields = ["owner__role","state"]
    search_fields = ["owner__id","title", "description","state","date","created_at"]
    ordering_fields = ["created_at"]

class SurveyView(viewsets.ModelViewSet):
    queryset= Survey.objects.all()
    serializer_class = SurveySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner__role"]
    filter_fields = ["owner__role"]
    search_fields = ["owner__id","title", "description","created_at"]
    ordering_fields = ["created_at"]

class ChoiceView(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["survey"]
    filter_fields = ["survey"]
    search_fields = ["name"]

    def paginate_queryset(self, queryset):
        
        return None

""" class VotedChoicesByUserAndSurvey(APIView):
    def get(self, request, user_id, survey_id, format=None):
        voted_choices = Choice.objects.filter(voted_by=user_id, survey=survey_id)
        serializer = ChoiceSerializer(voted_choices, many=True)
        return Response(serializer.data)
 """

 
class VotedSurveyByUser(APIView):
    pagination_class = CustomPagination
    
    def get(self, request, user_id, format=None):
        voted_choices = Survey.objects.filter(voted_by=user_id)
        
        paginator = self.pagination_class()
        paginated_voted_choices = paginator.paginate_queryset(voted_choices, request)
        
        serializer = SurveySerializer(paginated_voted_choices, many=True)
        return paginator.get_paginated_response(serializer.data)


class NoVotedSurveyByUser(APIView):
    pagination_class = CustomPagination
    
    def get(self, request, user_id, format=None):
        voted_choices = Survey.objects.exclude(voted_by=user_id)
        
        paginator = self.pagination_class()
        paginated_voted_choices = paginator.paginate_queryset(voted_choices, request)
        
        serializer = SurveySerializer(paginated_voted_choices, many=True)
        return paginator.get_paginated_response(serializer.data)


class BedsActualityView(viewsets.ModelViewSet):
    queryset = BedsActuality.objects.all()
    serializer_class = BedsActualitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]


    def paginate_queryset(self, queryset):
        
        return None


class CompanyCreationView(viewsets.ModelViewSet):
    queryset= CompanyCreation.objects.order_by("pk")
    serializer_class = CompanyCreationSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner","title"]
    filter_fields = ["owner","title"]
    search_fields = ["owner__role","title","description","created_at"]
    ordering_fields = ["created_at"]
