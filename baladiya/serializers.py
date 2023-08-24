from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer, PasswordChangeSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from .models import *

class WilayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilaya
        fields = '__all__'

class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = '__all__'

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    document = serializers.ImageField(max_length=None, use_url=True, required=False)
    commune = serializers.IntegerField(min_value=0)
    phone = serializers.CharField(max_length=10, validators=[num_only], required=False)
    birth_date = serializers.DateField(required=False)
    role = serializers.ChoiceField(choices=role_choices)
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    is_active = serializers.BooleanField(default=True)
    social_approved = serializers.BooleanField(default=False)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        data_dict['document'] = self.validated_data.get('document', '')
        data_dict['commune'] = self.validated_data.get('commune', '')
        data_dict['phone'] = self.validated_data.get('phone', '')
        data_dict['birth_date'] = self.validated_data.get('birth_date', '')
        data_dict['role'] = self.validated_data.get('role', '')
        data_dict['is_active'] = self.validated_data.get('is_active', '')
        data_dict['social_approved'] = self.validated_data.get('social_approved', '')
        return data_dict

class CustomLoginSerializer(LoginSerializer): 
    username = None

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password', })
    new_password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password', })
    class Meta:
        model = User
        fields = ['otp','email','new_password','new_password2']

class CustomUserDetailSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'document', 'commune', 'role', 'birth_date', 'social_approved', 'is_active','phone', 'image']

class ManagerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BaseSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(queryset=Commune.objects.all())
    # title = serializers.CharField(max_length=50)
    # description = serializers.CharField(max_length=500)
    # created_at = serializers.DateTimeField()
    class Meta:
        model = BaseModel
        fields = '__all__'

class FormationSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Formation
        fields = '__all__'

class AccompagnementSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Accompagnement
        fields = '__all__'

class TopicSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Topic
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ActivitySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Activity
        fields = '__all__'

class EcologicalInformationSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = EcologicalInformation
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class AudianceDemandSerializer(BaseSerializer):
    class Meta:
        model = AudianceDemand
        fields = '__all__'

class AgendaSerializer(BaseSerializer):
    class Meta:
        model = Agenda
        fields = '__all__'

class DiscussionSerializer(BaseSerializer):
    class Meta:
        model = Discussion
        fields = '__all__'

class SocialInformationSerializer(BaseSerializer):
    class Meta:
        model=SocialInformation
        fields= '__all__'

class DangerInformationSerializer(BaseSerializer):
    class Meta:
        model = DangerInformation
        fields = '__all__'

class VisiteSerializer(BaseSerializer):
    class Meta:
        model = Visite
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class HistoriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historique
        fields = '__all__'

class EmergencyFunctionsSerializer(BaseSerializer):
    class Meta:
        model = EmergencyFunctions
        fields = '__all__'