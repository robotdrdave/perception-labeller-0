from django.urls import path, include

from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

import labeller.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    #path("", labeller.views.login, name='login'),
    #path("logout", auth_views.LogoutView.as_view(), name='logout'),
    path("spam/", labeller.views.spam, name="spam"),
    path("harmful/", labeller.views.harmful, name="harmful"),
    path("opinion/", labeller.views.opinion, name="opinion"),
    path("fact/", labeller.views.fact, name="fact"),
    path("product_mention/", labeller.views.product_mention, name="product_mention"),
    path("out_of_samples/", labeller.views.out_of_samples, name="out_of_samples")
]
