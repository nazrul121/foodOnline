from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator


class RequiredFieldsMixin:
    def clean(self):
        cleaned_data = super().clean()
        empty_fields = []  # List to store fields with empty values
        for field_name, field_value in cleaned_data.items():
            if not field_value and field_name != 'id':
                empty_fields.append(field_name)  # Add field name to the list

        # Iterate over the list of empty fields and add errors to the form
        for field_name in empty_fields:
            field_name_display = field_name.replace('_', ' ')  # Replace underscores with spaces
            error_message = f"<b>{field_name_display.capitalize()}</b> is required."
            self.add_error(field_name, error_message)

        return cleaned_data



class registerFrom(RequiredFieldsMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
      
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'username', 'email', 'password']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control' ,'placeholder':'Type here'}),
        }

    #add require attr at input field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['phone_number'].required = False
        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False

    def clean(self):
        cleaned_data = super(registerFrom, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            #for non_field_errors
            raise forms.ValidationError( "Password does not match each other!" )

            # for field_errors
            self.add_error('password', 'Password does not match each other!')
    
        phone_number = self.cleaned_data.get('phone_number')
        # Take only the first 11 characters of the phone number
       

        if phone_number is not None:
            phone_number = phone_number[:11]
            if not phone_number.isdigit():
                self.add_error('phone_number','Phone number must contain only numeric values.')
                # raise forms.ValidationError('Phone number must contain only numeric values.')

            # Check if phone number contains exactly 11 digits
            if len(phone_number) != 11:
                # raise forms.ValidationError('Phone number should  exactly 11 digits')
                self.add_error('phone_number','Phone number should  exactly 11 digits.')



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Email or Phone')
    password = forms.CharField(widget=forms.PasswordInput, label='Enter Password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['password'].required = False

    def clean(self):
        cleaned_data = super().clean()
        
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username:
            self.add_error('username', 'Empty <b>username</b> is not allowed')

        if not password:
            self.add_error('password', 'Empty <b>password</b> is not allowed')




class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'