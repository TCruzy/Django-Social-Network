from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnDiscPlaceholderImage
from djangoProject import settings
import os


class CustomVersatileImageField(VersatileImageField):
    def __init__(self, *args, **kwargs):
        if 'placeholder_image' not in kwargs:
            kwargs['placeholder_image'] = OnDiscPlaceholderImage(
                path=os.path.join(settings.BASE_DIR, 'static', 'placeholders', 'placeholder.png')
            )
        super().__init__(*args, **kwargs)
