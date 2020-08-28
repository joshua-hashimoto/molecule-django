from django.http import JsonResponse
from django.views.generic import View

from .models import Tag


class TagAjaxCreateView(View):

    def post(self, request):
        name = request.POST.get('tag_name')
        tag = Tag.objects.create(name=name)
        context = {
            'id': tag.pk,
            'name': tag.name,
        }
        return JsonResponse(context)
