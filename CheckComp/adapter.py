from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        user.email = data.get('email')
        user.username = data.get('username')
        # all your custom fields
        user.date_of_birth = data.get('date_of_birth')
        user.gender = data.get('gender')
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user

class UsernameMaxAdapter(DefaultAccountAdapter):
    def clean_username(self, username):
        if len(username) > 20:
            raise ValidationError('Please enter a username value less than the current one')
        return DefaultAccountAdapter.clean_username(self,username) # For other default validations.