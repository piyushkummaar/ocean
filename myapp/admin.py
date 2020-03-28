from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Contact, Membership, UserMembership, Subscription


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'


# class CustomUserAdmin(UserAdmin):
#     inlines = (ProfileInline, )
#     list_display = ('username', 'email', 'first_name',
#                     'last_name', 'is_staff', 'get_country')
#     list_select_related = ('profile', )

#     def get_country(self, instance):
#         return instance.profile.country
#     get_country.short_description = 'Country'

#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(Profile)

admin.site.register(Membership)
admin.site.register(UserMembership)
admin.site.register(Subscription)

admin.site.site_header = 'Ocean'
admin.site.index_title = 'Admin Panel'
admin.site.site_title = 'Ocean Admin Panel'
