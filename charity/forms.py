from django import forms
from django.forms import ModelForm, Textarea
from .models import Volunteer


class VolunteerForm(ModelForm):
    class Meta:
        model = Volunteer
        fields = '__all__'
        widgets = {
            "fullname": forms.TextInput(attrs={"placeholder": "Jack Doe"}),
            "email": forms.TextInput(attrs={'placeholder': 'Jackdoe@gmail.com'}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "cv": forms.FileInput(),
            "comment": Textarea(attrs={"placeholder": "Comment (Optional)", "rows": "5"}),
        }
        labels = {
            "cv": "Upload your CV"
        }

    def __init__(self, *args, **kwargs):
        super(VolunteerForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = False
        self.fields['cv'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ContactForm(forms.Form):
    firstname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Jack"}) )
    lastname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Doe"}) )
    email = forms.EmailField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Jackdoe@gmail.com", "pattern": "[^ @]*@[^ @]*"}))
    comment = forms.CharField(max_length=1000, required=False, widget=forms.Textarea(attrs={"placeholder": "What can we help you with?"}))

    def __init__(self, args, **kwargs):
        super(ContactForm, self).__init__(args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
