from django import forms

from src.pages.models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ваше імʼя',
                'autocomplete': 'name',
            }),
            'phone': forms.TextInput(attrs={
                'type': 'tel',
                'placeholder': '+38 (0__) ___-__-__',
                'inputmode': 'tel',
                'autocomplete': 'tel',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'you@example.com',
                'inputmode': 'email',
                'autocomplete': 'email',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Коротко опишіть ваше питання',
                'rows': 3,
            }),
        }

    def __init__(self, *args, form_type=ContactSubmission.FORM_CALLBACK, **kwargs):
        self.form_type = form_type
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Імʼя'
        self.fields['message'].label = 'Повідомлення'
        if form_type == ContactSubmission.FORM_CALLBACK:
            self.fields['phone'].label = 'Телефон'
            self.fields['phone'].required = True
            del self.fields['email']
        else:
            self.fields['email'].label = 'Email'
            self.fields['email'].required = True
            del self.fields['phone']

    def clean(self):
        cleaned = super().clean()
        if self.form_type == ContactSubmission.FORM_CALLBACK:
            phone = cleaned.get('phone', '')
            digits = ''.join(ch for ch in phone if ch.isdigit())
            if len(digits) < 9:
                self.add_error('phone', 'Вкажіть коректний номер телефону')
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.form_type = self.form_type
        if commit:
            instance.save()
        return instance
