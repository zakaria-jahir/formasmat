from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from core.views import export_session_pdf

app_name = 'core'

urlpatterns = [
    # Pages principales
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
    path('formations/<int:formation_pk>/add_wish/', views.add_training_wish, name='add_training_wish'),
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
    path('manage-session/delete/<int:session_id>/', views.delete_session, name='delete_session'),
    path('session/<int:session_id>/update_status/', views.update_session_status, name='update_session_status'),
    path('manage-session/create/', views.session_create, name='session_create'),
    path('manage-session/<int:session_id>/participants/create-and-add/', views.create_and_add_participant, name='create_and_add_participant'),
    path('sessions/calendar/', views.sessions_calendar, name='sessions_calendar'),
    path('export-session/<int:session_id>/participants/csv/', views.export_session_csv, name='export_session_csv'),
    path('export-session/<int:session_id>/participants/pdf/', views.export_session_pdf, name='export_session_pdf'),



    
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
    #sesions
    
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