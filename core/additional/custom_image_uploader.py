import os
import json
import uuid

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

import cloudinary


class MarkdownImageUploader(View):
    """
    custom image uploader for martor.
    """

    def post(self, request, *args, **kwargs):
        """
        called when images are uploaded to martor's markdown field.
        validation is from martor's documentation.
        it will upload images to cloudinary.

        Note:
            when there is '?' in the to be foldername the image upload will not work.
        """
        article_title = request.POST['title']
        if not article_title:
            return HttpResponse(_('Invalid request!'))

        if not request.is_ajax():
            return HttpResponse(_('Invalid request!'))

        if 'markdown-image-upload' not in request.FILES:
            return HttpResponse(_('Invalid request!'))

        image = request.FILES['markdown-image-upload']
        image_types = [
            'image/png', 'image/jpg',
            'image/jpeg', 'image/pjpeg', 'image/gif'
        ]
        if image.content_type not in image_types:
            # return error when the image type
            # is not an expected type
            data = json.dumps({
                'status': 405,
                'error': _('Bad image format.')
            }, cls=LazyEncoder)
            return HttpResponse(
                data, content_type='application/json', status=405)

        if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
            # return error when the image size
            # is over the setted MAX_IMAGE_UPLOAD_SIZE
            to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
            data = json.dumps({
                'status': 405,
                'error': _('Maximum image file is %(size) MB.') % {'size': to_MB}
            }, cls=LazyEncoder)
            return HttpResponse(
                data, content_type='application/json', status=405)

        # when the image is valid

        # create new name for image
        img_name = f'{uuid.uuid4().hex[:10]}-{image.name.replace(" ", "-")}'
        # assign new name to the image that is being uploaded
        image.name = img_name
        # create folder path
        img_folder = os.path.join(
            settings.MEDIA_URL, f'article/{article_title}/markdown/')
        # save image to cloudinary
        cloudinary_img = cloudinary.uploader.upload(
            image, folder=img_folder, overwrite=True)
        # get the saved image url from cloudinary response
        cloudinary_img_url = cloudinary_img['secure_url']
        # name json data to return to markdown
        data = json.dumps({
            'status': 200,
            'link': cloudinary_img_url,
            'name': image.name
        })
        return HttpResponse(data, content_type='application/json')
