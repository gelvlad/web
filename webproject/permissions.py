from django.core.exceptions import PermissionDenied
from django.http import Http404
from . import models


class CourseAuthorMixin:
    def check_is_author(self):
        try:
            course = models.Course.objects.get(id=self.kwargs['course_pk'])
        except models.Course.DoesNotExist:
            raise Http404('Course does not exist')
        if not course.author == self.request.user:
            raise PermissionDenied


class TestResultPermissionMixin:
    def check_is_taken_by(self):
        if not self.object:
            self.object = self.get_object()
        if not self.object.taken_by == self.request.user:
            raise PermissionDenied

    def check_is_active(self):
        if not self.object:
            self.object = self.get_object()
        if not self.object.isActive:
            raise PermissionDenied
