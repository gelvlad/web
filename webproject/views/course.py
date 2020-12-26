from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from webproject import forms, models
from webproject.permissions import decorators


class CourseCreateView(generic.CreateView, LoginRequiredMixin):
    model = models.Course
    template_name = 'webproject/course_views/course_create.html'
    fields = ['name']

    def get_success_url(self):
        return f'/courses/{self.object.id}'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UserCourseListView(LoginRequiredMixin, generic.ListView):
    model = models.Course
    template_name = 'webproject/course_views/user_course_list.html'

    def get_queryset(self):
        return models.Course.objects.filter(author=self.request.user)


class CourseListView(generic.ListView):
    model = models.Course
    template_name = 'webproject/course_views/course_list.html'
