from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
from urllib.parse import urljoin

# Custom storage path for Django CKEditor 5

class CKEditorCustomStorage(FileSystemStorage):
    location = os.path.join(settings.MEDIA_ROOT, 'images/recipes_steps_images')
    base_url = urljoin(settings.MEDIA_URL, 'images/recipes_steps_images/')