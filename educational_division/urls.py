from django.urls import path

from educational_division import views

urlpatterns = [
    path('', views.index, name='me'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('registration', views.RegistrationView.as_view(), name='registration'),
    path('specialities', views.SpecialitiesView.as_view(), name='specialities'),
    path('courses', views.CoursesView.as_view(), name='courses'),
    path('groups', views.GroupsView.as_view(), name='groups'),
    path('acts', views.ActsView.as_view(), name='acts'),
    path('professors', views.ProfessorsView.as_view(), name='professors'),
    path('plans', views.PlansView.as_view(), name='plans'),
    path('spread', views.SpreadView.as_view(), name='spread'),
    path('professor/<int:pk>/', views.ProfessorDetailView.as_view(), name='professor-detail'),
    path('genereate_act/', views.CreateActView.as_view(), name='generate_act'),
    path('completed_work/', views.CompleteWorkView.as_view(), name='completed_work'),
    path('remain_work/', views.RemainWorkView.as_view(), name='remain_work'),
    path('create_agreement/', views.CreateAgreementView.as_view(), name='create_agreement'),
    path('show_agreement', views.ShowAgreementView.as_view(), name='show_agreement'),
    path('show_remain_work', views.ShowRemainWorkView.as_view(), name='remain_work_shower'),
    path('create_contact', views.ContractView.as_view(), name='create_contact'),
    path('create_speciality_course', views.SpecialityCourseSpreadView.as_view(), name='create_speciality_course')
]
