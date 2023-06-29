from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import home

urlpatterns = [
                  path('', home, name='home'),

                  path('accounts/logout/', LogoutView.as_view(next_page="/"), name='logout'),
                  path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
                  path('accounts/register/', views.register_view, name='register'),
                  path('accounts/profile/', views.profile_view, name='profile'),
                  path('accounts/profile/edit', views.profile_edit, name='profile_edit'),
                  path('accounts/delete/', views.delete_profile_view, name='delete'),

                  path('dashboard/', views.dashboard, name='dashboard'),
                  path('data/edit/<int:data_id>/', views.edit_data, name='edit_data'),
                  path('data/delete/<int:data_id>/', views.delete_data, name='delete_data'),
                  path('data/view/<int:data_id>/', views.view_data, name='view_data'),

                  path('data_updated/', views.data_updated, name='data_updated'),
                  path('access_denied/', views.access_denied, name='access_denied'),

                  path('users/<int:user_id>/', views.user_detail, name='user_detail'),
                  path('users/create/', views.user_create, name='user_create'),

                  path('data/<int:data_id>/', views.confidential_data_detail, name='data_detail'),
                  path('data/create/', views.confidential_data_create, name='data_create'),

                  path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
                  path('messages/', views.message_list, name='message_list'),
                  path('messages/create/', views.message_create, name='message_create'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
