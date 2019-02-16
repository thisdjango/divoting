import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from vote.models import Voting, Variant, Vote
from vote.forms import VoteForm, VariantForm, AddUserForm


def get_base_context(request):
    if request.user.is_authenticated:
        context = {
            'menu': [
                {'link': '/', 'text': 'Главная'},
                {'link': '/votings', 'text': 'Голосования'},
                {'link': '/monly', 'text': 'Создать голосование'},
                {'link': '/logout', 'text': 'Выход'}
            ],
            'current_time': datetime.datetime.now(),
        }
    else:
        context = {
            'menu': [
                {'link': '/', 'text': 'Главная'},
                {'link': 'login', 'text': 'Вход'},
                {'link': 'singup', 'text': 'Регистрация'}
            ],
            'current_time': datetime.datetime.now(),
        }
    return context


def index_page(request):
    context = get_base_context(request)
    context['title'] = 'Главная страница'
    context['main_header'] = 'Simple votings'
    context['user'] = request.user
    return render(request, 'index.html', context)


@login_required()
def voting_page(request):
    context = get_base_context(request)
    context['title'] = 'Голосования'
    context['main_header'] = 'Simple votings'
    context['votings'] = Voting.objects.all()
    return render(request, 'base.html', context)


@login_required()
def monly_page(request):
    context = get_base_context(request)
    context['title'] = 'Создать голосование'
    context['main_header'] = 'Simple votings'
    context['user'] = current_user = request.user
    if request.method == 'POST':
        f = VoteForm(request.POST)
        if f.is_valid():

            name = f.data['name']
            descr = f.data['descr']

            # сохранение данных
            item = Voting(from_date=datetime.datetime.now(),
                          till_date=datetime.datetime.now(),
                          name=name, descr=descr,
                          author=current_user)
            item.save()

            context['name'] = name
            context['descr'] = descr
            context['form'] = f
        else:
            context['form'] = f
    else:
        context['nothing_entered'] = True
        context['form'] = VoteForm()

    return render(request, 'monly.html', context)


def profile(request, name):
    try:
        user = User.objects.get(username=name)
        return 'User {} exists'.format(user.username)
    except User.DoesNotExist:
        raise Http404

@login_required()
def variant_page(request, id):
    context = get_base_context(request)
    context['title'] = 'Варианты голосования'
    context['main_header'] = 'Simple votings'
    context['user'] = current_user = request.user
    context['voting_id'] = id
    context['variants'] = Variant.objects.filter(voting=id)
    context['areu'] = False
    if Voting.objects.get(id=id).author == current_user:
        context['areu'] = True

    if request.method == 'POST':
        f = VariantForm(request.POST)
        if f.is_valid():

            f.data['voting'] = vot = id
            text = f.data['text']

            # сохранение данных

            varu = Variant(voting=Voting.objects.get(id=id).id, text=text)
            varu.save()

            context['form'] = f
            context['text'] = text
            context['id'] = vot
        else:
            context['form'] = f
    else:
        context['nothing_entered'] = True
        context['form'] = VariantForm()

    return render(request, 'voting.html', context)

def create_user(request):
    context = get_base_context(request)
    if request.method == 'POST':
        f = AddUserForm(request.POST)
        if f.is_valid():

            name = f.data['name']
            email = f.data['email']
            passw = f.data['passw']

            # сохранение данных

            user = User.objects.create_user(username=name, email=email, password=passw)
            user.save()
            context['passw'] = passw
            context['name'] = name
            context['email'] = email
            context['form'] = f
        else:
            context['form'] = f
    else:
        context['nothing_entered'] = True
        context['form'] = AddUserForm()
    return render(request, 'singup.html', context)
