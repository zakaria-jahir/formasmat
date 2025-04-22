from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crée les groupes et permissions nécessaires'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Création des groupes
        admin_group, _ = Group.objects.get_or_create(name='Administrateurs')
        staff_group, _ = Group.objects.get_or_create(name='Staff')
        user_group, _ = Group.objects.get_or_create(name='Utilisateurs')

        self.stdout.write(self.style.SUCCESS('Groupes créés avec succès'))

        # Récupération des content types
        user_ct = ContentType.objects.get_for_model(User)
        
        # Création des permissions
        view_users_perm, _ = Permission.objects.get_or_create(
            codename='view_users',
            name='Can view users',
            content_type=user_ct,
        )
        manage_users_perm, _ = Permission.objects.get_or_create(
            codename='manage_users',
            name='Can manage users',
            content_type=user_ct,
        )

        self.stdout.write(self.style.SUCCESS('Permissions créées avec succès'))

        # Attribution des permissions aux groupes
        admin_group.permissions.add(view_users_perm, manage_users_perm)
        staff_group.permissions.add(view_users_perm)

        self.stdout.write(self.style.SUCCESS('Permissions attribuées avec succès'))
