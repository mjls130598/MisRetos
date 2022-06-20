from django import forms


class registro(forms.Form):
    email = forms.EmailField(label='Email:',
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': 'ejemplo@ejemplo.com',
                                 }))
    nombre = forms.CharField(label='Nombre:', max_length='100',
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control'
                                 }))
    password = forms.CharField(label='Contraseña:', max_length='16', min_length='8',
                                 widget=forms.PasswordInput(
                                     attrs={
                                         'class': 'form-control'
                                     }))
    password_again = forms.CharField(label='Repetir contraseña:', max_length='16',
                                         min_length='8', widget=forms.PasswordInput(
                                             attrs={
                                                 'class': 'form-control'
                                             }))
    foto_de_perfil = forms.ImageField(label='Foto de perfil:',
                                      widget=forms.FileInput(
                                          attrs={
                                              'class': 'form-control'
                                          }))

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password_again']

        if password != password2:
            self.add_error('repetir_contraseña', "Las constraseñas deben ser iguales")

        return password
