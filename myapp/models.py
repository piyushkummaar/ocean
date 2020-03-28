from django.conf import settings
import stripe
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
from django_countries.fields import CountryField

random_id = random.randint(0, 10000000000)
user_id = random.randint(0,100000000)
stripe.api_key = settings.STRIPE_SECRET_KEY


MEMBERSHIP_CHOICES = (
    ('USER', 'User'),
    ('ACTIVE', 'Active'),
    ('STAR', 'Star'),
    ('SILVER', 'Silver'),
    ('GOLD', 'Gold'),
    ('PLATINUM', 'Platinum'),
    ('DIAMOND', 'Diamond'),
)


class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES,
        default='USER',
        max_length=30)
    price = models.IntegerField(default=15)
    img = models.ImageField(upload_to='membership_img',null=True,blank=True)
    level = models.IntegerField(default=0)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(
        Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


# def post_save_usermembership_create(sender, instance, created, *args, **kwargs):
#     user_membership, created = UserMembership.objects.get_or_create(
#         user=instance)

#     if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
#         new_customer_id = stripe.Customer.create(email=instance.email)
#         free_membership = Membership.objects.get(membership_type='USER')
#         user_membership.stripe_customer_id = new_customer_id['id']
#         user_membership.membership = free_membership
#         user_membership.save()


# post_save.connect(post_save_usermembership_create,
#                   sender=settings.AUTH_USER_MODEL)


class Subscription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username

    # @property
    # def get_created_date(self):
    #     subscription = stripe.Subscription.retrieve(
    #         self.stripe_subscription_id)
    #     return datetime.fromtimestamp(subscription.created)

    # @property
    # def get_next_billing_date(self):
    #     subscription = stripe.Subscription.retrieve(
    #         self.stripe_subscription_id)
    #     return datetime.fromtimestamp(subscription.current_period_end)


class Profile(models.Model):
    USER = 1
    ACTIVE = 2
    STAR = 3
    SILVER = 4
    GOLD = 5
    PLATINUM = 6
    DIAMOND = 7
    ROLE_CHOICES = (
        (USER, 'User'),
        (ACTIVE, 'Active'),
        (STAR, 'Star'),
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
        (PLATINUM, 'Platinum'),
        (DIAMOND, 'Diamond'),
        
    )
    name = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.IntegerField(null=True,blank=True)
    password = models.IntegerField(null=True,blank=True)
    refer_account_id = models.CharField(default=random_id, max_length=120, blank=True)
    refer_account_name = models.CharField(max_length=30, blank=True) 
    user_id = models.CharField(
        max_length=120,
        default=user_id)
    country = CountryField(blank_label='(select country)')
    role = models.PositiveSmallIntegerField(default=USER,
        choices=ROLE_CHOICES, null=True, blank=True)
    def __str__(self):
        return self.name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70, default='')
    phone = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=500, default='')

    class Meta:
        verbose_name = 'Contact Details'
        verbose_name_plural = 'Contact Details'
        db_table = 'tbl_contact'
        managed = True
        
    def __str__(self):
        return self.name
