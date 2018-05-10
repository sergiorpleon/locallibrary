# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
        migrations.AddField(
            model_name='author',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'imagens/photos/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='cuver',
            field=models.ImageField(null=True, upload_to=b'imagenes/covers/', blank=True),
            preserve_default=True,
        ),
    ]
