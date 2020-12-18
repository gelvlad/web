from django import forms
from . import models


class TestForm(forms.ModelForm):
    class Meta:
        model = models.Test
        fields = ['name']


QuestionsCreateFormset = forms.modelformset_factory(
    model=models.Question,
    fields=['text', 'answer', 'points'],
    extra=1,
    can_delete=True
)

QuestionsUpdateFormset = forms.modelformset_factory(
    model=models.Question,
    fields=['text', 'answer', 'points'],
    extra=0,
    can_delete=True
)


class QuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = models.QuestionAnswer
        fields = ['question_text', 'given_answer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question_text'].disabled = True


# class BaseQuestionAnswerFormset(forms.BaseFormSet):
#     def __init__(self, *args, **kwargs):
#         self.question_ids = kwargs.pop('question_ids')
#         super().__init__(*args, **kwargs)
#
#     def clean(self):
#         if any(self.errors):
#             return
#
#         for form, question_id in zip(self.forms, self.question_ids):
#             if self.can_delete and self._should_delete_form(form):
#                 continue
#             if form.instance.question__id != question_id:
#                 raise forms.ValidationError('Question id has been changed') # TODO: words


QuestionAnswerFormset = forms.modelformset_factory(
    model=models.QuestionAnswer,
    form=QuestionAnswerForm,
    extra=0
)
