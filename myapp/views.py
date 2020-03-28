from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse
from django.core import mail
from .models import Contact, Membership, UserMembership, Subscription,Profile
from myapp.forms import ProfileForm
import stripe


def home(request):
    return render(request,'index.html')

def aboutus(request):
    return render(request, 'roadmap.html')

def profile(request):
    return render(request,'d-templates/dashboard.html')

def wallet(request):
    return render(request, 'd-templates/icons.html')


def user_profile(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_membership': user_membership,
        'user_subscription': user_subscription
    }
    # return render(request, "memberships/profile.html", context)
    return render(request, 'd-templates/user.html', context)


def notifications(request):
    obj = Membership.objects.all()
    context = {'obj': obj}
    return render(request, 'd-templates/notifications.html',context)


def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None


def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


@login_required
def profile_view(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_membership': user_membership,
        'user_subscription': user_subscription
    }
    return render(request, "memberships/profile.html", context)


class MembershipSelectView(LoginRequiredMixin, ListView):
    model = Membership
    template_name = 'd-templates/notifications.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self, request, **kwargs):
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        selected_membership_type = request.POST.get('membership_type')

        selected_membership = Membership.objects.get(
            membership_type=selected_membership_type)

        if user_membership.membership == selected_membership:
            if user_subscription is not None:
                messages.info(request, """You already have this membership. Your
                        next payment is due {}""".format('get this value from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # assign to the session
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('payment'))


@login_required
def PaymentView(request):
    user_membership = get_user_membership(request)
    try:
        selected_membership = get_selected_membership(request)
    except:
        return redirect(reverse("select"))
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == "POST":
        try:
            token = request.POST['stripeToken']

            # UPDATE FOR STRIPE API CHANGE 2018-05-21

            '''
            First we need to add the source for the customer
            '''

            customer = stripe.Customer.retrieve(
                user_membership.stripe_customer_id)
            customer.source = token  # 4242424242424242
            customer.save()

            '''
            Now we can create the subscription using only the customer as we don't need to pass their
            credit card source anymore
            '''

            subscription = stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[
                    {"plan": selected_membership.stripe_plan_id},
                ]
            )

            return redirect(reverse('update-transactions',
                                    kwargs={
                                        'subscription_id': subscription.id
                                    }))

        except:
            messages.info(
                request, "An error has occurred, investigate it in the console")

    context = {
        'publishKey': publishKey,
        'selected_membership': selected_membership
    }

    return render(request, "memberships/membership_payment.html", context)


@login_required
def updateTransactionRecords(request, subscription_id):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(
        user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request, 'Successfully created {} membership'.format(
        selected_membership))
    return redirect(reverse('select'))


@login_required
def cancelSubscription(request):
    user_sub = get_user_subscription(request)

    if user_sub.active is False:
        messages.info(request, "You dont have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()

    user_sub.active = False
    user_sub.save()

    free_membership = Membership.objects.get(membership_type='Free')
    user_membership = get_user_membership(request)
    user_membership.membership = free_membership
    user_membership.save()

    messages.info(
        request, "Successfully cancelled membership. We have sent an email")
    # sending an email here

    return redirect(reverse('select'))


def maps(request):
    return render(request, 'd-templates/map.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
    return render(request, 'contact.html')

def wallet_transfer(request):
    return render(request,'d-templates/wallet-transfer.html')



def exchange_fund(request):
    return render(request,'d-templates/exchange_fund.html')



def inr_fund(request):
    return render(request,'d-templates/inr_fund.html')



def roi_buy(request):
    return render(request,'d-templates/roi_buy.html')



def direct_income(request):
    return render(request,'d-templates/direct_income.html')



def level_income(request):
    return render(request,'d-templates/level_income.html')

def fast_income(request):
    return render(request, 'd-templates/fast_income.html')


def prime_pool(request):
    return render(request,'d-templates/prime_pool.html')


def direct_team(request):
    return render(request,'d-templates/direct_team.html')


def downline_team(request):
    return render(request,'d-templates/downline_team.html')

def prime_pool_team(request):
    return render(request,'d-templates/prime_pool_team.html')


from django.core.mail import send_mail

def user_signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            email = EmailMessage(
                subject='Hello',
                body='Body goes here',
                from_email='rajat.saini@alervice.com',
                to=['pk554115@gmail.com'],
                reply_to=['rajat.saini@alervice.com'],
                headers={'Content-Type': 'text/plain'},
            )
            form.save()
            users = Profile.objects.all() #for check autofile 
            return redirect('/')
    else:
        form = ProfileForm()

    return render(request,'accounts/signup.html',{'form':form})
