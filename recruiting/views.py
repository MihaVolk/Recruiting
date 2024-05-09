from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import View, ListView, FormView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Vacancy, Application, Office, WorkDirection
from .forms import SignupForm, LoginForm, ApplicationForm
from django.db.models import Q
from .filters import VacancyFilter
# Create your views here.

def admin_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return redirect('main_page')
    return wrap


class MainView(View):
    def get(self, request):
        return render(request, "recruiting/index.html")

class SignupView(FormView):
    template_name = "recruiting/signup.html"
    model = User
    form_class = SignupForm
    success_url = reverse_lazy("main_page")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AuthenticationView(FormView):
    template_name = "recruiting/signin.html"
    model = User
    form_class = LoginForm
    success_url = reverse_lazy("main_page")

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return super().form_valid(form)


class ApplicationView(FormView):
    template_name = "recruiting/application.html"
    model = Application
    form_class = ApplicationForm
    success_url = reverse_lazy("main_page")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        vacancy = Vacancy.objects.get(id=self.kwargs.get("pk"))
        context["vacancy"] = vacancy
        return context

    def get_initial(self) -> dict[str, Any]:
        return {"full_name": self.request.user.full_name, "email": self.request.user.email, "phone_number": self.request.user.phone_number}

    def form_valid(self, form):
        application = form.save(commit=False)
        application.applicant = self.request.user
        application.vacancy = Vacancy.objects.get(id=self.kwargs.get("pk"))
        application.save()
        return super().form_valid(form)

@admin_required
def all_vacancies(request):
    vacancies = VacancyFilter(request.GET, queryset=Vacancy.objects.all())
    context = {'vacancies': vacancies}
    return render(request, 'recruiting/review.html', context)

@admin_required
def vacancy_applications(request, vacancy_id):
    vacancy = Vacancy.objects.get(pk=vacancy_id)
    applications = Application.objects.filter(vacancy=vacancy).select_related('applicant')
    context = {'vacancy': vacancy, 'applications': applications}
    return render(request, 'recruiting/review_application.html', context)

@admin_required
def application_detail(request, application_id, *args, **kwargs):
    application = Application.objects.get(pk=application_id)
    print(application.accepted)
    status = kwargs.get('status')
    if status:
        if status == "accept":
            application.accepted = True
        elif status == "decline":
            application.accepted = False
        application.save()
        return redirect('application_detail', application_id=application_id)
    
    context = {'application': application}
    return render(request, 'recruiting/review_application_detail.html', context)


       
def vacancy_list(request):
    vacancies = VacancyFilter(request.GET, queryset=Vacancy.objects.all())
    context = {"vacancies": vacancies}
    return render(request, "recruiting/vacancy_list.html", context=context)

@login_required
def profile(request):
    user = request.user
    applications = user.applications.all()

    application_statuses = []
    for application in applications:
        if application.accepted:  # Check if decision was made
            if application.accepted:
                status = "Принята"
            else:
                status = "Отклонена"
        else:
            status = "Ожидает ответа"
        
        # status = "Принята" if application.accepted else "Отклонена" if application.accepted is not None else "Ожидает ответа"

        application_statuses.append({
            "vacancy_title": application.vacancy.title,
            "status": status,
        })

    context = {
        'user': user,
        'application_statuses': application_statuses,
    }
    return render(request, 'recruiting/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('main_page')