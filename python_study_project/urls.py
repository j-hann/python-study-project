from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # jobs api 연결
    path('api/', include('jobs.urls')),

]
