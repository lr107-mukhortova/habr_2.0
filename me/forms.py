from django import forms


class RegistrationForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='E-mail')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Никнейм')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Повторить пароль')
    remember = forms.BooleanField(label='Запомнить меня', required=False)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password', 'Пароли не совпадают')
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Пароль')
    remember = forms.BooleanField(label='Запомнить меня', required=False)
