from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'webproject'
urlpatterns = [
    path('', RedirectView.as_view(url='courses/'), name='front'),
    path('courses/', views.CourseListView.as_view(), name='all_course_list'),
    path('user/courses/', views.UserCourseListView.as_view(), name='user_course_list'),
    path('user/courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:course_pk>/', views.TestListView.as_view(), name='test_list'),
    path('courses/<int:course_pk>/test/create/', views.TestCreateView.as_view(), name='test_create'),
    path('courses/<int:course_pk>/test/<int:test_pk>/', views.TestDetailView.as_view(), name='test_detail'),
    path('courses/<int:course_pk>/test/<int:test_pk>/update/', views.TestUpdateView.as_view(), name='test_update'),
    path('courses/<int:course_pk>/test/<int:test_pk>/test_results/', views.TestTestResultListView.as_view(), name='test_test_result_list'),
    path('test_results/', views.UserTestResultListView.as_view(), name='user_test_result_list'),
    path('test_results/<int:test_result_pk>/', views.TestResultDetailView.as_view(), name='test_result_detail'),
    path('take_test/<int:test_result_pk>/', views.TakeTestView.as_view(), name='take_test'),
]
