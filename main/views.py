from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, IsAuthenticated
from rental.serializers import RegistrationSerializer, LoginSerializer
#from rental.tasks import send_email_confirmation
from rest_framework.response import Response
from django.contrib import messages


# def register(request):
#     error = ''
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account created successfully')
#         else:
#             error = 'Invalid form'
#
#     form = UserRegisterForm()
#
#     data = {
#         'form': form,
#         'error': error
#     }
#     return render(request, 'main/register.html', data)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # current_site = get_current_site(request)
        # send_email_confirmation.delay(user.id, current_site.domain)

        return Response(serializer.data, status=201)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Обратите внимание, что мы не вызываем метод save() сериализатора, как
        # делали это для регистрации. Дело в том, что в данном случае нам
        # нечего сохранять. Вместо этого, метод validate() делает все нужное.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=200)


# def login(request):
#     error = ''
#     if request.POST == 'POST':
#         form = UserRegisterForm()
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         else:
#             error = 'Incorrect form'
#
#     form = UserRegisterForm()
#     data = {
#         'form': form,
#         'error': error
#     }
#
#     return render(request, 'main/login_logout.html', data)