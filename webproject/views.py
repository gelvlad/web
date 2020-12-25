from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import redirect
from django.views import generic
from . import forms, models
from .permissions import CourseAuthorMixin, TestResultPermissionMixin


class TestCreateView(
    generic.CreateView,
    LoginRequiredMixin,
    CourseAuthorMixin
):
    model = models.Test
    fields = ['name']
    template_name = 'webproject/test_views/test_create.html'

    def get(self, request, *args, **kwargs):
        self.check_is_author()
        return super(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question_formset = forms.QuestionsCreateFormset(
            queryset=models.Question.objects.none()
        )
        context['question_formset'] = question_formset
        return context

    def post(self, request, *args, **kwargs):
        self.check_is_author()

        question_formset = forms.QuestionsCreateFormset(data=request.POST)
        form = self.get_form()

        if form.is_valid() and question_formset.is_valid():
            test = form.save(commit=False)
            test.course_id = self.kwargs['course_pk']
            test.save()
            questions = question_formset.save(commit=False)
            for question in questions:
                question.test_id = test.id
            question_formset.save()
            return redirect(f'../{ test.id }')
        return self.render_to_response({
            'form': self.get_form(),
            'question_formset': question_formset
        })


class TestUpdateView(
    generic.UpdateView,
    LoginRequiredMixin,
    CourseAuthorMixin
):
    model = models.Test
    fields = ['name']
    pk_url_kwarg = 'test_pk'
    template_name = 'webproject/test_views/test_update.html'

    def get(self, request, *args, **kwargs):
        self.check_is_author()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_formset = forms.QuestionsUpdateFormset(
            queryset=self.object.question_set.all()
        )
        context['question_formset'] = question_formset
        return context

    def post(self, request, *args, **kwargs):
        self.check_is_author()

        self.object = self.get_object()
        form = self.get_form()
        question_formset = forms.QuestionsUpdateFormset(
            data=request.POST,
            initial=self.object.question_set.values()
        )

        if form.is_valid() and question_formset.is_valid():
            form.save()
            for question_form in question_formset.deleted_forms:
                if question_form.instance.id:
                    question_form.instance.delete()

            questions = question_formset.save(commit=False)

            for question in questions:
                if not question.test_id:
                    question.test_id = self.object.id
                question.save()

            return redirect('.')

        return self.render_to_response(self.get_context_data())


class UserCourseListView(generic.ListView, LoginRequiredMixin):
    model = models.Course
    template_name = 'webproject/course_views/user_course_list.html'

    def get_queryset(self):
        return models.Course.objects.filter(author=self.request.user)


class CourseCreateView(generic.CreateView, LoginRequiredMixin):
    model = models.Course
    template_name = 'webproject/course_views/course_create.html'
    fields = ['name']

    def get_success_url(self):
        return f'/courses/{self.object.id}'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TestListView(generic.ListView, LoginRequiredMixin):
    model = models.Test
    template_name = 'webproject/test_views/test_list.html'

    def get_queryset(self):
        return models.Test.objects.filter(course_id=self.kwargs['course_pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        try:
            context['course'] = models.Course.objects.get(
                id=self.kwargs['course_pk']
            )
        except models.Course.DoesNotExist:
            raise Http404('Course does not exist')
        return context


class TakeTestView(
    generic.DetailView,
    LoginRequiredMixin,
    TestResultPermissionMixin
):
    model = models.TestResult
    pk_url_kwarg = 'test_result_pk'
    template_name = 'webproject/test_result_views/take_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.check_is_taken_by()
        self.check_is_active()

        question_answer_formset = forms.QuestionAnswerFormset(
            queryset=self.object.questionanswer_set.all()
        )
        context['question_answer_formset'] = question_answer_formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.check_is_taken_by()
        self.check_is_active()

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


class CourseListView(generic.ListView):
    model = models.Course
    template_name = 'webproject/course_views/course_list.html'


class TestDetailView(generic.DetailView, LoginRequiredMixin):
    model = models.Test
    pk_url_kwarg = 'test_pk'
    template_name = 'webproject/test_views/test_detail.html'

    def get_context_data(self, **kwargs):
        try:
            models.Course.objects.get(id=self.kwargs['course_pk'])
        except models.Course.DoesNotExist:
            raise Http404("Course does not exist")

        context = super().get_context_data(**kwargs)
        question_set = self.object.question_set.all()
        context['question_set'] = question_set
        context['total_points'] = question_set.aggregate(
            Sum('points')
        )['points__sum']
        context['author'] = self.object.course.author
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        test_result = models.TestResult(
            taken_by=request.user,
            test=self.object
        )
        test_result.save()
        for question in self.object.question_set.all():
            question_answer = models.QuestionAnswer(
                question_text=question.text,
                correct_answer=question.answer,
                total_points=question.points,
                testResult=test_result
            )
            question_answer.save()
        return redirect(f'/take_test/{test_result.id}/')


class TestTestResultListView(
    generic.ListView,
    LoginRequiredMixin,
    CourseAuthorMixin
):
    model = models.TestResult
    template_name = 'webproject/test_result_views/test_test_result_list.html'

    def get(self, request, *args, **kwargs):
        self.check_is_author()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return models.TestResult.objects\
            .filter(test_id=self.kwargs['test_pk'])\
            .order_by('-date_time_created')

    def get_context_data(self, *, object_list=None, **kwargs):
        try:
            models.Course.objects.get(id=self.kwargs['course_id'])
            test = models.Test.objects.get(id=self.kwargs['test_pk'])
        except models.Course.DoesNotExist:
            raise Http404('Course does not exist')
        except models.Test.DoesNotExist:
            raise Http404('Test does not exist')

        context = super().get_context_data(object_list=object_list, **kwargs)
        context['test'] = test
        return context


class UserTestResultListView(generic.ListView, LoginRequiredMixin):
    model = models.TestResult
    template_name = 'webproject/test_result_views/user_test_result_list.html'

    def get_queryset(self):
        return models.TestResult.objects.filter(taken_by=self.request.user)


class TestResultDetailView(
    generic.DetailView,
    LoginRequiredMixin,
    TestResultPermissionMixin
):
    model = models.TestResult
    pk_url_kwarg = 'test_result_pk'
    template_name = 'webproject/test_result_views/test_result_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.check_is_taken_by()

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
