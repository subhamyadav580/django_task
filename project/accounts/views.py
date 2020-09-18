from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from accounts.serializers import UserSerializer, RegistrationSerializer
from accounts.utils import generate_access_token, generate_refresh_token
from accounts.forms import AccountAuthenticationForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import User




class RegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)

        return success_url

def user_login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
        print('helllo')
    context['login_form'] = form
    return render(request, 'registration/login.html', context)


def user_logout_view(request):
    logout(request)
    return redirect('home')




def home(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        user = request.user
        logged_user = User.objects.get(email=user)
        context['profile'] = logged_user
    return render(request, 'home.html', context)



@api_view(['GET'])
def profile(request):
    user = request.user
    serialized_user = UserSerializer(user).data
    return Response({'user': serialized_user })


@api_view(['POST',])
@permission_classes([])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'User is successfully registerd'
        else:
            data = serializer.errors
        
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    User = get_user_model()
    email = request.data.get('email')
    password = request.data.get('password')
    response = Response()
    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'email and password required')

    user = User.objects.filter(email=email).first()
    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')

    serialized_user = UserSerializer(user).data

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }

    return response
