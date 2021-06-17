from django.http import JsonResponse

from .models import Background

# Create your views here.
def get(request, value):
    bg = Background.objects.get(id=value)
    return JsonResponse({'value': bg.color_view()})
