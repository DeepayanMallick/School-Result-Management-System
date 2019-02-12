from django.contrib import admin
from django.urls import include, path, re_path
from results.views import Homepage, RankListView
from results.api.views import UserViewSet
from django.contrib.auth import views as auth_views

from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

#router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)





#from django.contrib.auth import login
#from django.contrib.auth import authenticate, login
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Homepage.as_view(), name='home_app'),
    path('results/', include('results.urls')),
    #path('login/', auth_views.login, name='login1'),
    path('results/', include('django.contrib.auth.urls')),
    path('api/', UserViewSet.as_view(), name='api'),
    #re_path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    path('all-school-rank/',RankListView.as_view() , name='rank'),

]

handler404 = 'results.views.ErrorPage'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
school_name = 'Fulhata Secondary School'

# default: "Django Administration"
admin.site.site_header = school_name+' Admin Panel'
# default: "Site administration"
admin.site.index_title = school_name+' Administration '
admin.site.site_title = school_name+' adminsitration'



