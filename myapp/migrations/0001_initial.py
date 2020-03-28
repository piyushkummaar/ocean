# Generated by Django 3.0.2 on 2020-03-28 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(default='', max_length=70)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('message', models.CharField(default='', max_length=500)),
            ],
            options={
                'verbose_name': 'Contact Details',
                'verbose_name_plural': 'Contact Details',
                'db_table': 'tbl_contact',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('membership_type', models.CharField(choices=[('USER', 'User'), ('ACTIVE', 'Active'), ('STAR', 'Star'), ('SILVER', 'Silver'), ('GOLD', 'Gold'), ('PLATINUM', 'Platinum'), ('DIAMOND', 'Diamond')], default='USER', max_length=30)),
                ('price', models.IntegerField(default=15)),
                ('img', models.ImageField(blank=True, null=True, upload_to='membership_img')),
                ('level', models.IntegerField(default=0)),
                ('stripe_plan_id', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile', models.IntegerField(blank=True, null=True)),
                ('password', models.IntegerField(blank=True, null=True)),
                ('refer_account_id', models.CharField(blank=True, default=9965368902, max_length=120)),
                ('refer_account_name', models.CharField(blank=True, max_length=30)),
                ('user_id', models.CharField(default=4441240, max_length=120)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('role', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'User'), (2, 'Active'), (3, 'Star'), (4, 'Silver'), (5, 'Gold'), (6, 'Platinum'), (7, 'Diamond')], default='USER', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(max_length=40)),
                ('membership', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.Membership')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_subscription_id', models.CharField(max_length=40)),
                ('active', models.BooleanField(default=True)),
                ('user_membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.UserMembership')),
            ],
        ),
    ]