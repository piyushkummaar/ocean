from django.urls import path

from . import views
from .views import (
    MembershipSelectView,
    PaymentView,
    updateTransactionRecords,
    profile_view,
    cancelSubscription, 
    user_signup,
    user_login
)

urlpatterns = [
    path('', views.home,name='home'),
    path('about/', views.aboutus, name='about'),
    path('contact/', views.contact,name='contact'),
    path('dashboard/', views.profile, name='dashbord'),
    path('wallet',views.wallet, name='wallet'),
    path('user-profile',views.user_profile,name='user_profile'),
    path('memeberships',views.notifications,name='notify'),
    path('maps',views.maps,name='maps'),
    path('list', MembershipSelectView.as_view(), name='select'),
    path('payment/', views.PaymentView, name='payment'),
    path('update-transactions/<subscription_id>/',
         updateTransactionRecords, name='update-transactions'),
    path('profile/', profile_view, name='profile'),
    path('cancel/', cancelSubscription, name='cancel'),

    path('exchange_fund/', views.exchange_fund, name='exchange_fund'),
    path('inr_fund/', views.inr_fund, name='inr_fund'),

    path('wallet_transfer/',views.wallet_transfer, name='wallet_transfer'),
    path('roi_buy/', views.roi_buy, name='roi_buy'),
    
    path('direct_income/', views.direct_income, name='direct_income'),
    path('level_income/', views.level_income, name='level_income'),
    path('fast_income/', views.fast_income, name='fast_income'),
    path('prime_pool/', views.prime_pool, name='prime_pool'),
    
    path('direct_team/', views.direct_team, name='direct_team'),
    path('downline_team/', views.downline_team, name='downline_team'),
    path('prime_pool_team/', views.prime_pool_team, name='prime_pool_team'),
    path('registeration',views.user_signup, name='register'),
    path('login', views.user_login, name="login")

]
