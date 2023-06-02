import math
from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView

from educational_division.models import *


def contains_number(string):
    return True if set(string).intersection('0123456789') else False


@login_required
def index(request):
    if request.user.role == 0:
        user_contract = request.user.professor_data.contracts_set.all()
        acts = Acts.objects.filter(contract__in=user_contract).all()
        return render(request, "index.html", {"acts": acts})
    else:
        return render(request, "index.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect('/login')


class RegistrationView(View):

    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        username: str = request.POST['username']
        password = request.POST['password']
        password_repeat = request.POST['password2']
        fio: str = request.POST['fio']
        phone = request.POST['phone']
        email = request.POST['email']
        fio_split = fio.split(" ")
        if password != password_repeat:
            messages.add_message(request, messages.ERROR, "Пароли не совпадают!")
            return redirect("registration")
        if len(password) < 6:
            messages.add_message(request, messages.ERROR, "Пароль меньше 6 символов!")
            return redirect("registration")
        if username == password:
            messages.add_message(request, messages.ERROR, "Логин и пароль не должны совпадать!")
            return redirect("registration")
        if len(fio_split) != 3:
            messages.add_message(request, messages.ERROR, "Введите корректное ФИО!")
            return redirect("registration")
        if contains_number(fio):
            messages.add_message(request, messages.ERROR, "Введите корректное ФИО!")
            return redirect("registration")
        professor = Professors.objects.get_or_create(last_name=fio_split[0], first_name=fio_split[1],
                                                     surname=fio_split[2], email=email, phone_number=phone)
        user = User.objects.create_user(username=username, password=password, professor_data=professor[0])
        login(request, user)
        return redirect("/")


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.add_message(request, messages.INFO, 'Проверьте правильность введенных данных!')
            return redirect("login")
        login(request, user)
        return redirect('/')


class SpecialitiesView(LoginRequiredMixin, ListView):
    model = Specialities
    context_object_name = "specialities"
    template_name = "specialities.html"


class GroupsView(LoginRequiredMixin, ListView):
    model = Group
    context_object_name = "groups"
    template_name = "groups.html"


class ActsView(LoginRequiredMixin, ListView):
    model = Acts
    context_object_name = "acts"
    template_name = "acts.html"


class ProfessorsView(LoginRequiredMixin, ListView):
    model = Professors
    context_object_name = "professors"
    template_name = "professors.html"


class CoursesView(LoginRequiredMixin, ListView):
    model = Courses
    context_object_name = "courses"
    template_name = "courses.html"


class PlansView(LoginRequiredMixin, ListView):
    model = Specialities
    context_object_name = "plan"
    template_name = "plan.html"


class SpreadView(LoginRequiredMixin, ListView):
    model = Professors
    context_object_name = "professors"
    template_name = "spread.html"


class CreateActView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "generate_act.html")

    def post(self, request):
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        contract_id = request.POST['contract']
        from_date_datetime = datetime.strptime(from_date, '%Y-%m-%d')
        to_date_datetime = datetime.strptime(to_date, '%Y-%m-%d')
        if from_date_datetime > to_date_datetime:
            messages.add_message(request, messages.ERROR, "Введите корректный период!")
            return redirect("generate_act")
        min_date = datetime(2023, 2, 8)
        max_date = datetime(2023, 6, 8)
        if from_date_datetime < min_date or to_date_datetime > max_date:
            messages.add_message(request, messages.ERROR, "Укажите период в пределах текущего семестра!")
            return redirect("generate_act")
        percent = (to_date_datetime - from_date_datetime) / (max_date - min_date)
        contract = Contracts.objects.get(id=contract_id)
        worked_hours = math.floor(percent * contract.hours)
        Acts.objects.create(worked_hours=worked_hours, beginning_date=from_date, end_date=to_date,
                            creation_date=datetime.now().strftime('%Y-%m-%d'), contract_id=contract_id)
        return redirect("/")


class CompleteWorkView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "generate_completed_act.html")

    def post(self, request):
        contract_id = request.POST['contract']
        current_date = datetime.now()
        min_date = datetime(2023, 2, 8)
        max_date = datetime(2023, 6, 8)
        percent = (current_date - min_date) / (max_date - min_date)
        contract = Contracts.objects.get(id=contract_id)
        worked_hours = math.floor(percent * contract.hours)
        Acts.objects.create(worked_hours=worked_hours, beginning_date=min_date,
                            end_date=current_date.strftime('%Y-%m-%d'), creation_date=current_date.strftime('%Y-%m-%d'),
                            contract_id=contract_id)
        return redirect("/")


class RemainWorkView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "create_remain_work.html")


class ShowRemainWorkView(LoginRequiredMixin, View):
    def get(self, request):
        contract_id = request.GET['contract']
        contract = Contracts.objects.get(id=contract_id)
        min_date = datetime(2023, 2, 8)
        max_date = datetime(2023, 6, 8)
        current_date = datetime.now()
        percent = (current_date - min_date) / (max_date - min_date)
        remain_hours = contract.hours - math.floor(percent * contract.hours)
        return render(request, "show_remain_work.html", {"contract": contract, "remain_hours": remain_hours})


class CreateAgreementView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "create_agreement.html")


class ShowAgreementView(LoginRequiredMixin, View):

    def get(self, request):
        contract_id = request.GET['contract']
        print(contract_id)
        contract = Contracts.objects.get(id=contract_id)
        print(contract)
        print(request.user.professor_data.contracts_set.all())
        if contract in request.user.professor_data.contracts_set.all():
            return render(request, "show_agreement.html", {"contract": contract})
        return HttpResponseNotFound("")


class ProfessorDetailView(LoginRequiredMixin, View):
    model = Professors
    context_object_name = "professor"
    template_name = "professor.html"

    def get(self, request, pk):
        try:
            professor = Professors.objects.get(id=pk)
            contracts = Contracts.objects.filter(professor_id=professor.id)
            return render(request, self.template_name, {"professor": professor, "contracts": contracts})
        except:
            return HttpResponseNotFound("")


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contracts
        fields = ['professor', 'course', 'group', 'type', 'hours']
        widgets = {
            'type': forms.Select(choices=[('Лекции', 'Лекции'), ('Практические занятия', 'Практические занятия'),
                                          ('Экзамены', 'Экзамены')])
        }


class ContractView(LoginRequiredMixin, CreateView):
    model = Contracts
    template_name = 'admin/create_contract.html'
    form_class = ContractForm

    def get(self, request):
        professors = Professors.objects.all()
        courses = Courses.objects.all()
        return render(request, 'admin/create_contract.html',
                      {"professors": professors, "courses": courses})

    def get_success_url(self):
        return '/'


class SpecialityCourseSpreadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SpecialityCourses
    fields = '__all__'
    template_name = 'admin/create_speciality_course.html'
    success_url = "/create_speciality_course"
    success_message = 'Учебный план изменен'
