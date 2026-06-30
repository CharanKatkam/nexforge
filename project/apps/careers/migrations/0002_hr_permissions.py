"""Grant the HR Manager role full control of careers models. Reversible."""

from django.db import migrations

MODELS = ["jobopening", "jobapplication"]
ACTIONS = ["add", "change", "delete", "view"]


def grant(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    try:
        hr = Group.objects.get(name="HR Manager")
    except Group.DoesNotExist:
        return
    perms = Permission.objects.filter(
        content_type__app_label="careers",
        content_type__model__in=MODELS,
        codename__regex=r"^(" + "|".join(ACTIONS) + ")_",
    )
    hr.permissions.add(*perms)


def revoke(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    try:
        hr = Group.objects.get(name="HR Manager")
    except Group.DoesNotExist:
        return
    perms = Permission.objects.filter(content_type__app_label="careers")
    hr.permissions.remove(*perms)


class Migration(migrations.Migration):

    dependencies = [
        ("careers", "0001_initial"),
        ("accounts", "0001_roles"),
    ]

    operations = [migrations.RunPython(grant, revoke)]
