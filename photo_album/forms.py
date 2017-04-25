from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.core.files.images import get_image_dimensions

from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
# Next two lines are only used for generating the upload preset sample name
from cloudinary.compat import to_bytes
import cloudinary, hashlib

from .models import Photo


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'

    # Validation for image field size during upload
    def clean_image(self):
        image = self.cleaned_data.get('image')
        width = get_image_dimensions(image)[0]
        height = get_image_dimensions(image)[1]
        if width > 500 or height > 500:
            raise ValidationError("Photo is too large to upload. Please only upload images up to 500 x 500 pixels")
        return image


class PhotoDirectForm(PhotoForm):
    image = CloudinaryJsFileField()


class PhotoUnsignedDirectForm(PhotoForm):
    upload_preset_name = "sample_" + hashlib.sha1(to_bytes(cloudinary.config().api_key + cloudinary.config().api_secret)).hexdigest()[0:10]
    image = CloudinaryUnsignedJsFileField(upload_preset_name)



