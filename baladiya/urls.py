from django.urls import path, include, re_path
from dj_rest_auth.registration.views import (
    RegisterView,
    ConfirmEmailView,
    VerifyEmailView,
)
from dj_rest_auth.views import (
    UserDetailsView,
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
)
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from baladiya.views import *
from .consumers import ChatConsumer


schema_view = get_schema_view(
    openapi.Info(
        title="Baladiyatuna",
        default_version="v1",
        description="Baladiya management",
        contact=openapi.Contact(email="soon@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register("wilayas", WilayaView, basename="wilaya")
router.register("communes", CommuneView, basename="commune")
router.register("manage_users", ManageUsersView, basename="manage_users")
router.register("formations", FormationView, basename="formation")
router.register("accompagnements", AccompagnementView, basename="accompagnement")
router.register("topics", TopicView, basename="topic")
router.register("activities", ActivityView, basename="activity")
router.register("comments", CommentView, basename="comment")
router.register(
    "ecological_informations", EcologicalInformationView, basename="ecological_info"
)
router.register("products", ProductView, basename="product")
router.register("audiance_demands", AudianceDemandView, basename="audiance_demand")
router.register("agendas", AgendaView, basename="agenda")
router.register("discussions", DiscussionView, basename="discussion")
router.register(
    "social_informations", SocialinformationView, basename="social_information"
)
router.register(
    "danger_informations", DangerInformationView, basename="danger_information"
)
router.register("visits", VisiteView, basename="visite")
router.register("emergencies", EmergencyFunctionsView, basename="emergency_function")
router.register("albums", AlbumView, basename="album")
router.register("actualities", ActualityView, basename="actuality")
router.register("admin_actualities", AdminActualityView, basename="admin_actuality")
router.register("studies", StudyView, basename="study")
router.register("surveys", SurveyView, basename="survey")
router.register("choices", ChoiceView, basename="choice")
router.register("beds_actuality", BedsActualityView, basename="beds_actuality")
router.register("companies_creation", CompanyCreationView, basename="company_creation")
router.register("chats",ChatView, basename="chat")
router.register("messages", MessageView, basename="message")
router.register("history",Historique, basename="history")
router.register("publicity_offers", PublicityOfferView, basename="publicity_offer")
router.register("publicities", PublicityView, basename="publicity")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "password-reset-confirm/",
        ResetPasswordView.as_view(),
        name="password_reset_confirm",
    ),
    path("account-confirm-email/<str:key>/", ConfirmEmailView.as_view()),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view()),
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("password-reset/", ResetRequestView.as_view()),
    path("password-change/", PasswordChangeView.as_view(), name="password_change"),
    path("user/", CustomUserDetailsView.as_view()),
    path(
        "historiques/",
        HistoriqueListCreateView.as_view(),
        name="historique-list-create",
    ),
    path(
        "historiques/<int:pk>/",
        HistoriqueRetrieveUpdateDeleteView.as_view(),
        name="historique-retrieve-update-delete",
    ),
    # path('choices/voted_by_user&survey/<int:user_id>/<int:survey_id>/', VotedChoicesByUserAndSurvey.as_view(), name='voted-choices-by-user'),
    path(
        "surveys/voted_by/<int:user_id>/",
        VotedSurveyByUser.as_view(),
        name="voted-surveys-by-user",
    ),
    path(
        "surveys/no_voted_by/<int:user_id>/",
        NoVotedSurveyByUser.as_view(),
        name="voted-surveys-by-user",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
urlpatterns += router.urls
