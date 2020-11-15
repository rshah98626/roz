# Generated by Django 3.0.6 on 2020-10-02 02:57

from django.db import migrations, models
import roz.custom_storage


class Migration(migrations.Migration):

    dependencies = [
        ('chatty', '0008_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='file_name',
        ),
        migrations.AddField(
            model_name='video',
            name='file',
            field=models.FileField(default=None, storage=roz.custom_storage.VideoStorage, upload_to='', verbose_name='The video file instance'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='When the video was created'),
        ),
    ]
