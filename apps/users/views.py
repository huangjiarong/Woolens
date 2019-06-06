from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate

from rest_framework import views
from rest_framework import status
from rest_framework.response import Response

from .serializers import UserProfileSerializer


class LoginRequiredMixin():
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='login')


class LoginView(views.APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.data)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(views.APIView):
    def get(self, request):
        auth.logout(request)
        return redirect('login')
# def login(request):
#     if request.method == 'POST':
#         login_form = forms.LoginForm(request.POST)
#         if login_form.is_valid():
#             login_name = request.POST['username'].strip()
#             login_password = request.POST['password']
#             user = authenticate(username=login_name, password=login_password)
#             if user is not None:
#                 if user.is_active:
#                     auth.login(request, user)
#                     return redirect('/')
#     else:
#         login_form = forms.LoginForm()
#
#     template = get_template('login.html')
#     request_context = RequestContext(request)
#     request_context.push(locals())
#     html = template.render(request_context)
#     response = HttpResponse(html)
#     return response

def logout(request):
    auth.logout(request)
    return redirect('/')
