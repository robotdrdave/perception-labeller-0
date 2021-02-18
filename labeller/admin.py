from django.contrib import admin

from .models import Snippet, Evaluated_Snippet

admin.site.register(Snippet)
admin.site.register(Evaluated_Snippet)
