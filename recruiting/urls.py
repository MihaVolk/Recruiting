from django.urls import path

from .views import (
    AuthenticationView,
    SignupView,
    MainView,
    ApplicationView,
    logout_view,
    vacancy_list,
    all_vacancies,
    vacancy_applications,
    application_detail,
    profile,
)

urlpatterns = [
    path("", MainView.as_view(), name="main_page"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", AuthenticationView.as_view(), name="login"),
    path('logout/', logout_view, name='logout'),
    path('vacancies/', vacancy_list, name='vacancies'),
    path("application/<int:pk>/", ApplicationView.as_view(), name="application"),
    path('review/', all_vacancies, name='all_vacancies'),
    path('review/<int:vacancy_id>/', vacancy_applications, name='vacancy_applications'),
    path('review/application/<int:application_id>/', application_detail, name='application_detail'),
    path('review/application/<int:application_id>/<slug:status>/', application_detail, name='application_detail_status'),
    path('profile/', profile, name='profile'),
]