from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from webproject import forms, models
from webproject.permissions import decorators


class TakeTestView(LoginRequiredMixin, generic.DetailView):
    model = models.TestResult
    pk_url_kwarg = 'test_result_pk'
    template_name = 'webproject/test_result_views/take_test.html'

    @decorators.check_taken_by_user
    @decorators.check_result_is_active
    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_answer_formset = forms.QuestionAnswerFormset(
            queryset=self.object.questionanswer_set.all()
        )
        context['question_answer_formset'] = question_answer_formset
        return context

    @decorators.check_taken_by_user
    @decorators.check_result_is_active
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        question_answer_formset = forms.QuestionAnswerFormset(
            data=request.POST,
            initial=self.object.questionanswer_set.all()
        )
        if question_answer_formset.is_valid():
            question_answer_formset.save()
            self.object.isActive = False
            self.object.save()
            return redirect(f'/test_results/{self.object.id}')
        return self.render_to_response(self.get_context_data())


class TestTestResultListView(
    LoginRequiredMixin,
    generic.ListView
):
    model = models.TestResult
    template_name = 'webproject/test_result_views/test_test_result_list.html'

    @decorators.check_course_kwarg
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        return models.TestResult.objects \
            .filter(test_id=self.kwargs['test_pk']) \
            .order_by('-date_time_created')

    def get_context_data(self, *, object_list=None, **kwargs):
        test = get_object_or_404(models.Test, id=self.kwargs['test_pk'])
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['test'] = test
        return context


class UserTestResultListView(LoginRequiredMixin, generic.ListView):
    model = models.TestResult
    template_name = 'webproject/test_result_views/user_test_result_list.html'

    def get_queryset(self):
        return models.TestResult.objects.filter(taken_by=self.request.user)


class TestResultDetailView(
    LoginRequiredMixin,
    generic.DetailView
):
    model = models.TestResult
    pk_url_kwarg = 'test_result_pk'
    template_name = 'webproject/test_result_views/test_result_detail.html'

    @decorators.check_taken_by_user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_answers = self.object.questionanswer_set.all()
        context['question_answers'] = question_answers
        total_points = 0
        scored_points = 0
        for question_answer in question_answers:
            total_points += question_answer.total_points
            scored_points += question_answer.scored_points
        context['total_points'] = total_points
        context['scored_points'] = scored_points
        return context
