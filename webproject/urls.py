from django.urls import path
from django.views.generic import RedirectView
from webproject.views import\
    course as course_views,\
    test as test_views,\
    test_result as test_result_views


app_name = 'webproject'
urlpatterns = [
    path('', RedirectView.as_view(url='courses/'), name='front'),
    path('courses/', course_views.CourseListView.as_view(), name='all_course_list'),
    path('user/courses/', course_views.UserCourseListView.as_view(), name='user_course_list'),
    path('user/courses/create/', course_views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:course_pk>/', test_views.TestListView.as_view(), name='test_list'),
    path('courses/<int:course_pk>/test/create/', test_views.TestCreateView.as_view(), name='test_create'),
    path('courses/<int:course_pk>/test/<int:test_pk>/', test_views.TestDetailView.as_view(), name='test_detail'),
    path('courses/<int:course_pk>/test/<int:test_pk>/update/', test_views.TestUpdateView.as_view(), name='test_update'),
    path('courses/<int:course_pk>/test/<int:test_pk>/test_results/', test_result_views.TestTestResultListView.as_view(), name='test_test_result_list'),
    path('test_results/', test_result_views.UserTestResultListView.as_view(), name='user_test_result_list'),
    path('test_results/<int:test_result_pk>/', test_result_views.TestResultDetailView.as_view(), name='test_result_detail'),
    path('take_test/<int:test_result_pk>/', test_result_views.TakeTestView.as_view(), name='take_test'),
]
