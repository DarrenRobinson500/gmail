from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('home/<start>', views.home, name='home'),
    path('home/<start>/<null_only>', views.home, name='home'),
    path('show_messages/<sender_id>', views.show_messages, name='show_messages'),
    path('delete_messages', views.delete_messages, name='delete_messages'),
    # path('get_senders', views.get_senders, name='get_senders'),
    path('read_messages', views.read_messages, name='read_messages'),
    path('add_type/<id>/<type>/<start>/<null_only>', views.add_type, name='add_type'),
    path('show_years', views.show_years, name='show_years'),
    path('show_messages_year/<year>', views.show_messages_year, name='show_messages_year'),
]
