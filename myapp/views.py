from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.views import generic
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import RegistrationForm
from .backends import authBackend
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
User = get_user_model()

users_session = {}

def validate(data):
    print(data["middle_name"], "mbnnn")
    error = {}
    error["username"] = ""
    error["phone"] = ""
    error["middle"] = ""
    error["password"] = ""
    error["status"] = ""

    if len(data["name"]) == 0:
        error["username"] = "Username can not be empty..!"
        error["status"] = "error"

    if data["middle_name"].isalpha() == False:
        error["middle"] = "Middle name should only contains letters...!"
        error["status"] = "error"


    try:
        num = int(data["phone"])
        if len(data["phone"]) < 12:
            error["phone"] = "Please provide valid phone number"
    except:
        error["phone"] = "Phone number should be completely in numeric...!"
        error["status"] = "error"


    if len(data["password1"]) < 8:
        error["password"] = "Password should be atleast 8 characters...!"
        error["status"] = "error"

    if len(data["password2"]) > 8:
        if data["password1"] != data["password2"]:
            error["password"] = "Password and Confirm Password should be same...!"
            error["status"] = "error"

    return error

@method_decorator(csrf_exempt, name="dispatch")
class RegistrationView(generic.TemplateView):
    template_name = 'myapp/register.html'

    global users_session

    def get(self, request):

        try:
            user_chk = request.COOKIES['username']
            print(user_chk, "reg")

            if user_chk in users_session:
                return HttpResponseRedirect(reverse('dash', kwargs={"name": user_chk}))
            else:
                return render_to_response(self.template_name,{'form': form}, content_type=RequestContext)

        except:
            form = RegistrationForm(request.POST)
            return render_to_response(self.template_name, {'form': form}, content_type=RequestContext)

    def post(self, request):
        form = RegistrationForm(request.POST)
        data = request.POST.dict()
        chk_error = validate(data)
        print(chk_error)
        if chk_error["status"] == "":
            reg_data = User(username=data["name"], password=data["password2"], phone=data["phone"], middle_name=data["middle_name"])
            reg_data.save()
            u = User.objects.get(username=data["name"])
            u.set_password(data["password2"])
            u.save()
            print("Saved....!")

        else:
            return render_to_response(self.template_name, {'form': form, 'error': chk_error}, content_type=RequestContext)

        return HttpResponseRedirect(reverse('login'))


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(generic.TemplateView):
    template_name = 'myapp/login.html'
    msg = ""
    global users_session
    def get(self, request):
        try:
            user_chk = request.COOKIES["username"]
            print(user_chk, "log")
            print(users_session)
            if user_chk in users_session:
                return HttpResponseRedirect(reverse('dash', kwargs={"name": user_chk}))
            else:
                return render_to_response(self.template_name, content_type=RequestContext)


        except:
            return render_to_response(self.template_name, content_type=RequestContext)

    def post(self, request):

        data = request.POST.dict()
        username = data["name"]
        password = data["passw"]

        ab = authBackend()

        user = ab.authenticate(username=username, password=password)
        if user is not None:
            users_session[user.username] = {}
            users_session[user.username]["middle_name"] = user.middle_name
            users_session[user.username]["phone"] = user.phone
            return HttpResponseRedirect(reverse('dash', kwargs={"name": user.username}))
        else:
            msg = "Credentials are wrong....!Please try again with correct Credentials...!"

        return render_to_response(self.template_name, {'msg':msg}, content_type=RequestContext)


@method_decorator(csrf_exempt, name="dispatch")
class DashView(generic.TemplateView):

    template_name = 'myapp/dashboard.html'
    global users_session

    def get(self, request, name):

        try:
            info = users_session[name]
            response = render_to_response(self.template_name, {'name': name, 'middle_name': info['middle_name'], 'phone': info['phone']}, content_type=RequestContext)
            response.set_cookie('username', name)
            print("cookie Set")
            return response

        except Exception as er:
            print(str(er))
            return HttpResponseRedirect(reverse('login'))

    def post(self, request, name):
        del users_session[name]
        print("Successfully Logout....!")
        return HttpResponseRedirect(reverse('login'))

@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'myapp/password_reset.html'
    global users_session

    msg = ""
    def get(self, request):
        msg = ""
        try:
            user_chk = request.COOKIES["username"]
            if user_chk in users_session:
                return HttpResponseRedirect(reverse('dash', kwargs={"name": user_chk}))
            else:
                return render_to_response(self.template_name, {'msg': msg}, content_type=RequestContext)
        except:
            return render_to_response(self.template_name, {'msg': msg}, content_type=RequestContext)

    def post(self, request):
        data = request.POST.dict()
        print(data)
        username = data["name"]
        password = data["passw"]
        newPassword = data["new_passw"]

        ab = authBackend()
        user = ab.authenticate(username=username, password=password)
        if user is not None:
            u = User.objects.get(username=username)
            u.set_password(newPassword)
            u.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            msg = "Old Credentials are wrong....!Please try again with correct Credentials...!"

        print(msg)
        return render_to_response(self.template_name, {'msg': msg},  content_type=RequestContext)