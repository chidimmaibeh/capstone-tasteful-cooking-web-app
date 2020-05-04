from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .forms import SignUpForm, GroceryModelFormSet
from django.views.generic import View, UpdateView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.auth import login
from .forms import GroceryModelForm, ReceipeForm, ContactForm

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
            user.is_active = False  # Deactivate account till it is confirmed
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
    if request.method == 'POST':
        filled_form = ContactForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = ' Thank you for contact us! We will back to you soon '
            return render(request, 'contactus1.html', {'note': note})
    else:
        filled_form = ContactForm()

    return render(request, 'contactus.html', {'form': filled_form, })


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
    return render(request, 'homesearch.html', {'recipes': recipe})


@login_required
def recipes(request):
    """
    List user's recipes
    """
    recipe = Recipe.objects.filter(user=request.user)
    return render(request, 'myrecipes.html', {'recipes': recipe})


@login_required
def planner(request):
    """
    List user's meal plan
    """
    planner = Planner.objects.filter(user=request.user)
    return render(request, 'planner.html', {'planners': planner})


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
        return render(request, 'addplanner.html', {'recipes': recipe})


@login_required
def mygrocery(request):
    """
    List recipes that will be selected for reviewing the grocery.
    """
    recipes = request.user.recipe_set.all()
    return render(request, 'mygrocery1.html', {'recipes': recipes})


@login_required
def grocerylist(request):
    """
    Represent the grocery item of selected receipes
    """
    grocerys = []
    if request.method == 'POST':
        try:
            recipeIds = dict(request.POST)['recipeIds']
            print(recipeIds)
            qs_union = Grocery.objects.none()
            for recipeid in recipeIds:
                qs = Grocery.objects.filter(recipe_id=int(recipeid))
                qs_union = qs_union.union(qs)
            grocerys = qs_union.all()
        except Exception as e:
            pass
    else:
        grocerys = Grocery.objects.filter(user=request.user).all()
    return render(request, 'grocerylist.html', {'grocerys': grocerys})


@login_required
def delrecipes(request, id):
    """
    Delete the selected recipes
    """
    r = Recipe.objects.get(id=id)
    r.delete()
    return redirect('myrecipes')


@login_required
def delgrocery(request, id):
    """
    Delete the selected grocery items
    """
    r = Recipe.objects.get(id=id)
    g = Grocery.objects.get(recipe=r)
    g.delete()
    return redirect('mygrocery')


@login_required
def groceryadd(request, id):
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
    return render(request, 'grocerysearch.html', {'recipes': recipe, 'grocerys': grocery})


@login_required
def viewrecipes(request, id):
    """
    View each selected recipes
    """
    recipe = Recipe.objects.get(id=id)
    ingredients = recipe.ingredients.split(',')
    ingredients = recipe.grocery_set.all()
    return render(request, 'viewrecipes.html', {'recipe': recipe, 'ingredients': ingredients})


@login_required
def viewgrocery(request, id):
    """
    View each selected grocery 
    """
    recipe = Recipe.objects.get(id=id)
    ingredients = recipe.ingredients.split(',')
    return render(request, 'viewgrocery.html', {'recipe': recipe, 'ingredients': ingredients})


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

        formset = GroceryModelFormSet(request.POST, instance=r)
        if formset.is_valid():
            formset.save()

        return redirect('myrecipes')
    else:
        formset = GroceryModelFormSet()
        return render(request, 'addrecipes.html', {'formset': formset, 'userId': request.user.pk})


@login_required
def edit(request, pk):
    """
    add recipe page and save to DB
    """

    r = Recipe.objects.get(pk=pk)
    if request.method == "POST":

        r.title = request.POST.get('title')
        r.description = request.POST.get('desc')
        r.cusine = request.POST.get('cusine')
        r.ingredients = request.POST.get('addmore')
        r.user = request.user
        r.save()

        formset = GroceryModelFormSet(request.POST, instance=r)
        if formset.is_valid():
            formset.save()

        return redirect('myrecipes')
    else:
        formset = GroceryModelFormSet()
        return render(request, 'edit.html', {'formset': formset, 'userId': request.user.pk})


"""
def edit(request, pk):
    title = "Update Recipes"
    Groceryformset = inlineformset_factory(Grocery, form=GroceryModelForm, extra=0)
    queryset = Grocery.objects.filter(recipe__id=pk)

    formset = Groceryformset(request.POST or None, queryset=queryset)

    if formset.is_valid():
        instances = formset.save(commit=False)
        for instances in instances:
            instances.recipe.title = instances.recipe.title


            instances.save()

    context = {
        "formset": formset,
        "title" : title,
    }

    return render(request, 'edit.html', context)

    # Groceryformset = modelformset_factory(Grocery, fields=('content',))

    #  formset = Groceryformset(queryset=Grocery.objects.filter(recipe__id=pk))

"""
