# Generated by Django 3.2.12 on 2023-06-06 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitch_reward_id', models.CharField(max_length=10)),
                ('image_file_name', models.ImageField(null=True, upload_to='')),
                ('valid_flag', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'image',
            },
        ),
    ]
