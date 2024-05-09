from django_filters import FilterSet, ModelChoiceFilter
from .models import Vacancy, Office, WorkDirection

class VacancyFilter(FilterSet):
    office = ModelChoiceFilter(queryset=Office.objects.all(), label="Офис")
    direction = ModelChoiceFilter(queryset=WorkDirection.objects.all(), label="Направление работы")

    class Meta:
        model = Vacancy
        fields = ['office', 'direction']