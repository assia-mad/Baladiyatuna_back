from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.social_number = data.get('social_number')
        user.wilaya = data.get('wilaya')
        user.commune = data.get('commune')
        user.phone= data.get('phone')
        user.birth_date = data.get('birth_date')
        user.role = data.get('role')
        user.is_active = data.get('is_active')
        user.save()
        return user