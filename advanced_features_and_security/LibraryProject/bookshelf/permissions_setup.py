# Run this script after migrations:
# python manage.py shell < bookshelf/permissions_setup.py

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


content_type = ContentType.objects.get_for_model(Book)

# Permissions
perm_view = Permission.objects.get(codename='can_view', content_type=content_type)
perm_create = Permission.objects.get(codename='can_create', content_type=content_type)
perm_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
perm_delete = Permission.objects.get(codename='can_delete', content_type=content_type)

# Groups
viewers, _ = Group.objects.get_or_create(name="Viewers")
editors, _ = Group.objects.get_or_create(name="Editors")
admins, _ = Group.objects.get_or_create(name="Admins")

# Assign permissions
viewers.permissions.add(perm_view)

editors.permissions.add(perm_view, perm_edit, perm_create)

admins.permissions.add(perm_view, perm_edit, perm_create, perm_delete)

print("Groups and permissions created successfully!")
