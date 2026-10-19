from django import forms
from .models import Listing


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_clean(d, initial) for d in data]
        return [single_clean(data, initial)]


class ListingForm(forms.ModelForm):
    images = MultipleImageField(required=False, label="Photos (1 to 4)")

    class Meta:
        model = Listing
        fields = ["title", "description", "price", "category", "condition"]

    def clean_images(self):
        files = self.cleaned_data.get("images") or []
        if len(files) == 0:
            raise forms.ValidationError("Please add at least one photo.")
        if len(files) > 4:
            raise forms.ValidationError("You can upload a maximum of 4 photos.")
        for f in files:
            if f.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Each photo must be smaller than 5 MB.")
        return files