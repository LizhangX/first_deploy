from django.shortcuts import render, redirect, reverse
from .models import User, Secret
import bcrypt
from django.db.models import Count
from datetime import datetime

# Create your views here.
def index(request):
    print "Inside the index method."
    if 'errors' not in request.session:
        request.session['errors'] = []
    context ={
        'errors': request.session['errors'],
    }
    request.session.pop('errors')
    return render(request,'dojo_secrets_app/index.html',context)

def register(request):
    print "Inside the register method."

    if request.method == "POST":
        form_data = request.POST
        check = User.objects.register(form_data)
        duplicate = User.objects.filter(email=form_data['email'])
        print 'inside check unique'
        if duplicate:
            check.append('This email has been used.')
        if check:
            request.session['errors'] = check
            return redirect(reverse('index'))
        pw = str(form_data['password'])
        hashed_pw = bcrypt.hashpw(pw, bcrypt.gensalt())
        
        user = User.objects.create(
            first_name = form_data['fname'],
            last_name = form_data['lname'],
            email = form_data['email'],
            password = hashed_pw 
        )

        request.session['user_id'] = user.id

        return redirect(reverse('success'))
    return redirect(reverse('index'))
    
def login(request):
    print "Inside the login method."

    if request.method == "POST":
        form_data = request.POST
        check = User.objects.login(form_data)
        if type(check) == type(User()):
            request.session['user_id'] = check.id
            return redirect(reverse('success'))
        request.session['errors'] = check
        return redirect(reverse('index'))
    return redirect(reverse('index'))
        
def logout(request):
    print "Inside the logout method."
    request.session.pop('user_id')
    return redirect(reverse('index'))

def success(request):
    print "Inside the success method."

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        context = {
            'secrets': Secret.objects.all().order_by('-created_at')[:5],
            'current_user': User.objects.get(id=user_id),
            'range': range(5),
        }
        return render(request, 'dojo_secrets_app/success.html', context)
    return redirect(reverse('index'))  

def postSecret(request):
    print 'inside post_secret'
    Secret.objects.create(secret=request.POST['postSecret'], user_id = request.session['user_id'])
    return redirect(reverse('success'))

def like(request, secret_id, location):
    user_id = request.session['user_id']
    current_user = User.objects.get(id=user_id)
    current_secret = Secret.objects.get(id =secret_id)
    current_secret.like.add(current_user)
    if location == '1':
        return redirect(reverse('success'))
    if location == '2':
        return redirect(reverse('popular'))

def delete(request, secret_id, location):
    secret = Secret.objects.filter(id=secret_id).first()
    if secret.user_id == request.session['user_id']:
        Secret.objects.filter(id = secret_id).first().delete()
        if location == '1':
            return redirect(reverse('success'))
        if location == '2':
            return redirect(reverse('popular'))
    else:
        return redirect(reverse('index'))
def popular(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    order = Secret.objects.all().annotate(like_count = Count('like')).order_by('-like_count')
    context = {
        'secrets': order,
        'current_user': User.objects.get(id=user_id),   
    }
    return render(request, 'dojo_secrets_app/popular.html',context)
