from django.urls import path , include , re_path
from dj_rest_auth.registration.views import RegisterView , ConfirmEmailView , VerifyEmailView
from dj_rest_auth.views import UserDetailsView, LoginView, LogoutView , PasswordResetView , PasswordResetConfirmView , PasswordChangeView
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from baladiya.views import *

schema_view = get_schema_view(

   openapi.Info(

      title="Baladiyatuna",
      default_version='v1',
      description="Baladiya management",
      contact=openapi.Contact(email="soon@gmail.com"),
      license=openapi.License(name="BSD License"),

   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register('wilayas', WilayaView, basename='wilaya')
router.register('communes', CommuneView, basename='commune')
router.register('manage_users', ManageUsersView, basename='manage_users')
router.register('formations', FormationView, basename='formation')
router.register('accompagnements', AccompagnementView, basename='accompagnement')
router.register('topics', TopicView, basename='topic')
router.register('activities', ActivityView, basename='activity')
router.register('comments', CommentView, basename='comment')
router.register('ecological_infos', EcologicalInformationView, basename='ecological_info')
router.register('products', ProductView, basename='product')




urlpatterns = [
   path('', include(router.urls)),
   path('password-reset-confirm/', ResetPasswordView.as_view(), name='password_reset_confirm'),
   path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
   path('register/', CustomRegisterView.as_view(), name='register'),
   path('login/', CustomLoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view()),
   path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
   path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
   re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',VerifyEmailView.as_view(), name='account_confirm_email'),
   path('password-reset/', ResetRequestView.as_view()),
   path('password-change/', PasswordChangeView.as_view(), name='password_change'),
   path('user/', CustomUserDetailsView.as_view()),
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
urlpatterns += router.urls