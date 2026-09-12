from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from .models import Movie

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'İstifadəçi adı'}),
        label='İstifadəçi adı'
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ad (İstəyə bağlı)'}),
        label='Ad'
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyad (İstəyə bağlı)'}),
        label='Soyad'
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-poçt ünvanı (İstəyə bağlı)'}),
        label='E-poçt'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs['class'] = 'form-control'


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'release_year', 'status', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Məsələn: Inception, Interstellar...'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-select'
            }),
            'release_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Məsələn: 2010',
                'min': 1888,
                'max': datetime.now().year + 5
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1-10 arası qiymət',
                'min': 1,
                'max': 10
            }),
        }
        labels = {
            'title': 'Filmin adı',
            'genre': 'Janr',
            'release_year': 'Buraxılış ili',
            'status': 'Status',
            'rating': 'Şəxsi qiymətləndirmə (1-10)',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Filmin adı boş ola bilməz.")
        return title

    def clean_release_year(self):
        year = self.cleaned_data.get('release_year')
        current_year = datetime.now().year
        if year is not None:
            if year < 1888:
                raise forms.ValidationError("Dünyada ilk film 1888-ci ildə çəkilib.")
            if year > current_year + 5:
                raise forms.ValidationError(f"Buraxılış ili çox uzaq gələcək ola bilməz (Maksimum: {current_year + 5}).")
        return year

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 10):
            raise forms.ValidationError("Qiymətləndirmə 1 ilə 10 arasında olmalıdır.")
        return rating
