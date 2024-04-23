from django import forms 
from .models import Vendor




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




class VendorForm(RequiredFieldsMixin, forms.ModelForm):
    
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
        widgets = {
            'vendor_license': forms.FileInput(attrs={'class': 'form-control' }),
        }
    
    #add require attr at input field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendor_name'].required = False
        self.fields['vendor_license'].required = False
    
    def clean(self):
        cleaned_data = super(VendorForm, self).clean()
       
       

