from django.urls import path, include

urlpatterns = [
   path('users/', include('src.users.urls')),
   path('groups/', include('src.groups.urls')),
]
