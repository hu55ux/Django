from django import forms


class TicketBookingForm(forms.Form):
    customer_name = forms.CharField(
        label="Müştərinin Adı və Soyadı",
        max_length=100,
        min_length=2,
        required=True,
        error_messages={
            'required': 'Müştərinin adı boş ola bilməz.',
            'min_length': 'Müştərinin adı ən azı 2 simvol olmalıdır.',
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Məs: Əli Əliyev',
            'id': 'customer_name'
        })
    )
    ticket_count = forms.IntegerField(
        label="Biletlərin Sayı",
        min_value=1,
        initial=1,
        required=True,
        error_messages={
            'required': 'Bilet sayı daxil edilməlidir.',
            'invalid': 'Bilet sayı düzgün ədəd olmalıdır.',
            'min_value': 'Biletlərin sayı sıfırdan böyük olmalıdır.',
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'id': 'ticket_count'
        })
    )

    def __init__(self, *args, movie=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.movie = movie
        if movie and 'available_seats' in movie:
            self.fields['ticket_count'].widget.attrs['max'] = movie['available_seats']

    def clean_customer_name(self):
        customer_name = self.cleaned_data.get('customer_name', '').strip()
        if not customer_name:
            raise forms.ValidationError("Müştərinin adı boş ola bilməz.")
        if len(customer_name) < 2:
            raise forms.ValidationError("Müştərinin adı ən azı 2 simvol olmalıdır.")
        return customer_name

    def clean_ticket_count(self):
        ticket_count = self.cleaned_data.get('ticket_count')
        if ticket_count is None:
            raise forms.ValidationError("Bilet sayı düzgün ədəd olmalıdır.")
        if ticket_count <= 0:
            raise forms.ValidationError("Biletlərin sayı sıfırdan böyük olmalıdır.")
        return ticket_count

    def clean(self):
        cleaned_data = super().clean()
        ticket_count = cleaned_data.get('ticket_count')
        
        if self.movie and ticket_count is not None:
            available_seats = self.movie.get('available_seats', 0)
            if available_seats <= 0:
                raise forms.ValidationError("Bu film üçün biletlər bitmişdir (SOLD OUT). Bron etmək mümkün deyil.")
            if ticket_count > available_seats:
                raise forms.ValidationError(f"Mövcud boş yerlərin sayından ({available_seats}) çox bilet bron etmək olmaz.")
                
        return cleaned_data


class MovieFilterForm(forms.Form):
    genre = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'genreInput'})
    )
    available_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'id': 'availableToggle',
            'onchange': "document.getElementById('filterForm').submit()"
        })
    )
