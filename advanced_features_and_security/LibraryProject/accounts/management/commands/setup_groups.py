from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Create groups (Editors, Viewers, Admins) and assign custom permissions for Book model. Also creates test users.'

    def handle(self, *args, **options):
        # Target model: Book in relationship_app
        try:
            from relationship_app.models import Book
        except Exception as exc:
            self.stdout.write(self.style.ERROR('Could not import Book model: %s' % exc))
            return

        content_type = ContentType.objects.get_for_model(Book)

        # Ensure permissions exist (create if missing)
        perms = {
            'can_view': Permission.objects.get_or_create(
                codename='can_view',
                name='Can view book',
                content_type=content_type,
            )[0],
            'can_create': Permission.objects.get_or_create(
                codename='can_create',
                name='Can create book',
                content_type=content_type,
            )[0],
            'can_edit': Permission.objects.get_or_create(
                codename='can_edit',
                name='Can edit book',
                content_type=content_type,
            )[0],
            'can_delete': Permission.objects.get_or_create(
                codename='can_delete',
                name='Can delete book',
                content_type=content_type,
            )[0],
        }

        # Groups and their permission assignments
        groups_spec = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }

        for group_name, perm_codenames in groups_spec.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for codename in perm_codenames:
                group.permissions.add(perms[codename])
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' ready with permissions: {perm_codenames}"))

        # Create test users and assign them to groups (if they don't exist)
        user_model = get_user_model()
        test_users = [
            ('viewer', 'viewer@example.com', 'viewerpass', 'Viewers'),
            ('editor', 'editor@example.com', 'editorpass', 'Editors'),
            ('groupadmin', 'groupadmin@example.com', 'adminpass', 'Admins'),
        ]

        for username, email, password, groupname in test_users:
            user, created = user_model.objects.get_or_create(username=username, defaults={'email': email})
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user '{username}' with password '{password}'"))
            else:
                self.stdout.write(self.style.NOTICE(f"User '{username}' already exists"))
            group = Group.objects.get(name=groupname)
            user.groups.add(group)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Assigned '{username}' to group '{groupname}'"))

        self.stdout.write(self.style.SUCCESS('Groups, permissions and test users configured.'))
