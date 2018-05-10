# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=36, serialize=False, primary_key=True, help_text=b'Unique ID for this particular book across whole library'),
            preserve_default=True,
        ),
    ]
