from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from webproject import forms, models
from webproject.permissions import decorators


class TestCreateView(
    LoginRequiredMixin,
    generic.CreateView
):
    model = models.Test
    fields = ['name']
    template_name = 'webproject/test_views/test_create.html'

    @decorators.check_course_author
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_formset = forms.QuestionsCreateFormset(
            queryset=models.Question.objects.none()
        )
        context['question_formset'] = question_formset
        context['course'] = get_object_or_404(
            models.Course,
            id=self.kwargs['course_pk']
        )
        return context

    def post(self, request, *args, **kwargs):
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
    LoginRequiredMixin,
    generic.UpdateView
):
    model = models.Test
    fields = ['name']
    pk_url_kwarg = 'test_pk'
    template_name = 'webproject/test_views/test_update.html'

    @decorators.check_test_author
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_formset = forms.QuestionsUpdateFormset(
            queryset=self.object.question_set.all()
        )
        context['question_formset'] = question_formset
        return context

    @decorators.check_test_author
    def post(self, request, *args, **kwargs):
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


class TestListView(LoginRequiredMixin, generic.ListView):
    model = models.Test
    template_name = 'webproject/test_views/test_list.html'

    def get_queryset(self):
        return models.Test.objects.filter(course_id=self.kwargs['course_pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['course'] = get_object_or_404(
            models.Course,
            id=self.kwargs['course_pk']
        )
        return context


class TestDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Test
    pk_url_kwarg = 'test_pk'
    template_name = 'webproject/test_views/test_detail.html'

    @decorators.check_course_kwarg
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_set = self.object.question_set.all()
        context['question_set'] = question_set
        context['total_points'] = question_set.aggregate(
            Sum('points')
        )['points__sum']
        context['author'] = self.object.course.author
        return context

    @decorators.check_course_kwarg
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
