from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from core.views import export_session_pdf
from rest_framework.routers import DefaultRouter
from .api import *


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'formations', FormationViewSet)
router.register(r'sessions', SessionViewSet)



app_name = 'core'



urlpatterns = [
    # Pages principales
    path('api/', include(router.urls)),
    path('api/auth/', CustomAuthToken.as_view()),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('check-user-existence/', views.check_user_existence, name='check_user_existence'),
    
    # Formations
    path('formations/', views.formation_list, name='formation_list'),
    path('formations/<int:pk>/', views.formation_detail, name='formation_detail'),
    path('formations/create/', views.formation_create, name='formation_create'),
    path('formations/<int:pk>/edit/', views.formation_edit, name='formation_edit'),
    path('formations/<int:pk>/delete/', views.formation_delete, name='formation_delete'),
    
    # Formateurs
    path('trainers/', views.trainers_list, name='trainers_list'),
    path('trainers/<int:pk>/', views.trainer_detail, name='trainer_detail'),
    path('trainers/create/', views.trainer_create, name='trainer_create'),
    path('trainers/<int:pk>/edit/', views.trainer_edit, name='trainer_edit'),
    path('trainers/<int:pk>/delete/', views.trainer_delete, name='trainer_delete'),
    
    # Souhaits de formation
    path('wishes/', views.user_wishes, name='user_wishes'),
    path('sessions/', views.admin_training_sessions, name='admin_training_sessions'),
    path('formations/<int:formation_pk>/add_wish/', views.add_training_wish, name='add_training_wish'),
    path('sessions/<int:session_id>/assign-wishes/', views.assign_wishes_to_session, name='assign_wishes_to_session'),
    path('sessions/<int:session_id>/assign-wish/<int:wish_id>/', views.assign_single_wish_to_session, name='assign_single_wish_to_session'),


    path('manage-wishes/', views.manage_training_wishes, name='manage_training_wishes'),
    path('wishes/<int:pk>/delete/', views.delete_wish, name='delete_wish'),
    
    # Gestion administrative des souhaits de formation
    path('training-wishes/', views.admin_training_wishes, name='admin_training_wishes'),
    path('training-wishes/<int:wish_id>/assign/', views.assign_wish_to_session, name='assign_wish_to_session'),
    
    # Gestion des sessions
    path('manage-session/', views.manage_session, name='manage_session'),
    path('manage-session/detail/<int:session_id>/', views.session_detail, name='session_detail'),
    path('manage-session/get/<int:session_id>/', views.get_session, name='get_session'),
    path('manage-session/<int:session_id>/update/', views.update_session, name='update_session'),
    path('manage-session/<int:session_id>/delete/', views.delete_session, name='delete_session'),
    path('session/<int:session_id>/update_status/', views.update_session_status, name='update_session_status'),
    path('session/<int:session_id>/archive/', views.archive_session, name='archive_session'),
    path('sessions/export-archives/', views.export_archived_sessions_xlsx, name='export_archived_sessions'),
    path('sessions/list/', views.session_list, name='session_list'),
    path('session/<int:session_id>/change-status/', views.change_session_status, name='change_session_status'),





   
    
    path('manage-session/create/', views.session_create, name='session_create'),# url non utilisé la creation du session se faite par l'url 'api/create-session' voir API endpoints
    path('manage-session/<int:session_id>/participants/create-and-add/', views.create_and_add_participant, name='create_and_add_participant'),
    path('sessions/calendar/', views.sessions_calendar, name='sessions_calendar'),
    path('export-session/<int:session_id>/participants/csv/', views.export_session_csv, name='export_session_csv'),
    path('export-session/<int:session_id>/participants/pdf/', views.export_session_pdf, name='export_session_pdf'),
    #API mobile
    path('api/sessions/', views.session_list_api, name='session_list_api'),
    path('api/formations/', views.formation_list_api, name='formation_list_api'),
    path('api/trainers/', views.trainer_list_api, name='trainer_list_api'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/training-rooms/', views.api_training_rooms, name='api_training_rooms'),
    path('api/training-rooms/<int:room_id>/', views.api_training_room_detail, name='api_training_room_detail'),
    path('api/me/', views.get_user_info, name='get_user_info'),
    path('api/add-wish/', views.api_add_training_wish, name='api_add_training_wish'),
    path('api/my-wishes/', views.api_user_wishes, name='api_user_wishes'),
    path('api/remove-wish/', views.api_remove_training_wish, name='api_remove_training_wish'),
    












    # API endpoints
    path('api/users/', views.get_users, name='get_users'),
    path('api/create-session/', views.create_session, name='create_session'),
    path('api/update-session-status/', views.update_session_status, name='update_session_status'),
    path('api/wishes/', views.get_training_wishes, name='get_training_wishes'),
    path('api/assign-session/', views.assign_to_session, name='assign_to_session'),
    
    # Gestion des participants
    path('manage-session/<int:session_id>/participants/add/', views.add_participant, name='add_participant'),
    path('manage-session/participants/<int:session_id>/add-from-wish/', views.add_participant_from_wish, name='add_participant_from_wish'),
    path('manage-session/participants/<int:session_id>/create-and-add/', views.create_and_add_participant, name='create_and_add_participant'),
    path('manage-session/participants/<int:participant_id>/status/', views.update_participant_status, name='update_participant_status'),
    path('manage-session/participants/<int:participant_id>/comments/', views.get_participant_comments, name='get_participant_comments'),
    path('manage-session/participants/<int:participant_id>/update-comments/', views.update_participant_comments, name='update_participant_comments'),
    path('manage-session/participants/<int:participant_id>/remove/', views.remove_participant, name='remove_participant'),
    path('manage-session/participants/<int:participant_id>/update-status/', views.update_participant_status, name='update_participant_status_view'),
    
    # Salles de formation
    path('training-rooms/', views.training_room_list, name='training_room_list'),
    path('training-rooms/<int:pk>/', views.training_room_detail, name='training_room_detail'),
    path('training-rooms/create/', views.training_room_create, name='training_room_create'),
    path('training-rooms/<int:pk>/edit/', views.training_room_edit, name='training_room_edit'),
    path('training-rooms/<int:pk>/delete/', views.training_room_delete, name='training_room_delete'),
    path('rooms/add-comment/', views.add_room_comment, name='add_room_comment'),

    


    
    # Notifications
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    
    # URLs pour la réinitialisation du mot de passe
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='core/password/password_reset.html',
             email_template_name='core/password/password_reset_email.html',
             subject_template_name='core/password/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='core/password/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='core/password/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='core/password/password_reset_complete.html'
         ),
         name='password_reset_complete'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)