# Generated by Django 5.1.4 on 2024-12-18 20:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_content_created_at"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="vote",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="content",
            name="average_vote",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddIndex(
            model_name="vote",
            index=models.Index(fields=["content"], name="api_vote_content_0a4b0d_idx"),
        ),
        migrations.AddIndex(
            model_name="vote",
            index=models.Index(fields=["user"], name="api_vote_user_id_43f53e_idx"),
        ),
        migrations.AddIndex(
            model_name="vote",
            index=models.Index(
                fields=["content", "user"], name="api_vote_content_3a38c1_idx"
            ),
        ),
    ]
