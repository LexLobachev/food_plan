from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from plan.forms import CustomAuthenticationForm, Login


def index(request):
    """
    View function for home page of site.
    """
    return render(request, "index.html")


@login_required(login_url='/login/')
def lk(request):
    user = request.user
    context = {'user': user}
    # context = {'client': Client.objects.get(id=id)}
    return render(request, 'lk.html', context=context)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "registration/login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")

        return render(request, "registration/login.html", context={
            'form': form,
            'ivalid': True,
        })


def register(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/registration.html', {'form': form})
