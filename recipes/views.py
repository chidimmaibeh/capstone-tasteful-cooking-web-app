from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .forms import SignUpForm
from django.views.generic import View, UpdateView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.auth import login

from .models import *

# Create your views here.


class SignUpView(View):
    """
    Sign up for user
    senting activation link for user
    """
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})

class ActivateAccount(View):
    """
    Activation account link processsing
    """

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')



def landing(request):
    """
    Home page with our user login
    """
    return render(request, 'landing.html')

def ourstory(request):
    """
    Static link
    """
    return render(request, 'ourstory.html')

def ourpatners(request):
    """
    Static link
    """
    return render(request, 'ourpatners.html')

def news(request):
    """
    Static link
    """
    return render(request, 'news.html')

def news1(request):
    """
    Static link
    """
    return render(request, 'news1.html')

def news2(request):
    """
    Static link
    """
    return render(request, 'news2.html')

def contactus(request):
    """
    Static link
    """
    return render(request, 'contactus.html')

@login_required
def home(request):
    """
    Logged in user homepage
    """
    return render(request, 'home.html')

@login_required
def homesearch(request):
    """
    Logged in user homesearch page
    get the search key and returns recipes with search key
    """
    print(request.GET['search'])
    searchkey = request.GET['search']
    recipe = Recipe.objects.filter(title__icontains=searchkey)
    return render(request, 'homesearch.html',{'recipes':recipe})

@login_required
def recipes(request):
    """
    List user's recipes
    """
    recipe = Recipe.objects.filter(user=request.user)
    return render(request, 'myrecipes.html',{'recipes':recipe})




@login_required
def planner(request):
    """
    List user's meal plan
    """
    planner = Planner.objects.filter(user=request.user)
    return render(request, 'planner.html',{'planners':planner})

@login_required
def addplanner(request):
    """
    plan add page and handling the addition to DB
    """
    if request.method == "POST":
        try:
            id = request.POST['recipe']
        except:
            return redirect('planner')
        r = Recipe.objects.get(id=id)
        p = Planner()
        p.recipe = r
        p.date = datetime.strptime(request.POST['date'], '%m/%d/%Y')
        p.user = request.user
        p.save()

        return redirect('planner')
    else:
        recipe = Recipe.objects.filter(user=request.user)
        return render(request, 'addplanner.html',{'recipes':recipe})


@login_required
def mygrocery(request):
    """
    List user's grocery
    """
    grocery = Grocery.objects.filter(user=request.user)
    return render(request, 'mygrocery.html',{'grocerys':grocery})

@login_required
def delrecipes(request,id):
    """
    Delete the selected recipes
    """
    r = Recipe.objects.get(id=id)
    r.delete()
    return redirect('myrecipes')


@login_required
def delgrocery(request,id):
    """
    Delete the selected grocery items
    """
    r = Recipe.objects.get(id=id)
    g = Grocery.objects.get(recipe=r)
    g.delete()
    return redirect('mygrocery')
@login_required
def groceryadd(request,id):
    """
    Add grocery from selected recipe
    """
    recipe = Recipe.objects.get(id=id)
    g = Grocery()
    g.user = request.user
    g.recipe = recipe
    g.save()
    return redirect('mygrocery')

@login_required
def grocerysearch(request):
    """
    Returns all recipes from grocery search
    """
    print(request.GET['search'])
    searchkey = request.GET['search']
    recipe = Recipe.objects.filter(title__icontains=searchkey)
    grocery = Grocery.objects.filter(user=request.user)
    return render(request, 'grocerysearch.html',{'recipes':recipe,'grocerys':grocery})

@login_required
def viewrecipes(request,id):
    """
    View each selected recipes
    """
    recipe = Recipe.objects.get(id=id)
    ingredients = recipe.ingredients.split(',')
    return render(request, 'viewrecipes.html',{'recipe':recipe,'ingredients':ingredients})


@login_required
def viewgrocery(request,id):
    """
    View each selected grocery 
    """
    recipe = Recipe.objects.get(id=id)
    ingredients = recipe.ingredients.split(',')
    return render(request, 'viewgrocery.html',{'recipe':recipe,'ingredients':ingredients})

@login_required
def addrecipes(request):
    """
    add recipe page and save to DB
    """
    if request.method == "POST":

        r = Recipe()
        r.title = request.POST['title']
        r.description = request.POST['desc']
        r.cusine = request.POST['cusine']
        r.ingredients = request.POST['addmore']
        r.user = request.user
        r.save()

        return redirect('myrecipes')
    else:
        return render(request, 'addrecipes.html')
