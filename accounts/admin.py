from django.contrib import admin, auth
from django import forms

from accounts.models import User


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification."
    )

    class Meta:
        model = User
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(auth.admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': ('email', )
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', )}),
        ('Important dates', {'fields': ('date_joined', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    form = auth.forms.UserChangeForm
    add_form = UserCreationForm
    change_password_form = auth.forms.AdminPasswordChangeForm
    list_display = ('username', 'email', 'is_staff', 'date_joined', )
    list_filter = ('is_staff', 'is_active', )
    search_fields = ('username', 'email', )
    ordering = ('-date_joined',)
    filter_horizontal = []
