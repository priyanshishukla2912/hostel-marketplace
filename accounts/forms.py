from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    room_no = forms.CharField(max_length=10, label="Room number")
    invite_code = forms.CharField(max_length=50, label="Hostel invite code")

    field_order = ["username", "full_name", "phone", "room_no",
                   "password1", "password2", "invite_code"]

    def clean_invite_code(self):
        code = self.cleaned_data["invite_code"].strip()
        if code != settings.HOSTEL_INVITE_CODE:
            raise forms.ValidationError("Invalid invite code. Ask your hostel group admin.")
        return code

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profile.objects.create(
                user=user,
                full_name=self.cleaned_data["full_name"],
                phone=self.cleaned_data["phone"],
                room_no=self.cleaned_data["room_no"],
            )
        return user