# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-12-16 03:16
from __future__ import unicode_literals

import json

from django.db import migrations


def migrate_response_type(apps, schema_editor):
    Client = apps.get_model('oidc_provider', 'Client')
    for client in Client.objects.all():
        client.response_types = json.dumps(
            list(client.old_response_types.values_list('value', flat=True))
        )
        client.save()


def migrate_response_type_back_to_model(apps, schema_editor):
    Client = apps.get_model('oidc_provider', 'Client')
    ResponseType = apps.get_model('oidc_provider', 'ResponseType')
    RESPONSE_TYPES = [
        ('code', 'code (Authorization Code Flow)'),
        ('id_token', 'id_token (Implicit Flow)'),
        ('id_token token', 'id_token token (Implicit Flow)'),
        ('code token', 'code token (Hybrid Flow)'),
        ('code id_token', 'code id_token (Hybrid Flow)'),
        ('code id_token token', 'code id_token token (Hybrid Flow)'),
    ]
    # ensure we get proper, versioned model with the deleted response_type field;
    # importing directly yields the latest without response_type
    for value, description in RESPONSE_TYPES:
        ResponseType.objects.create(value=value, description=description)
    for client in Client.objects.all():
        client.old_response_types = list(ResponseType.objects.filter(value__in=json.loads(client.response_types)))


class Migration(migrations.Migration):

    dependencies = [
        ('oidc_provider', '0028_change_response_types_field_1_of_3'),
    ]

    operations = [
        migrations.RunPython(migrate_response_type, reverse_code=migrate_response_type_back_to_model),
    ]