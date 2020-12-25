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


QuestionAnswerFormset = forms.modelformset_factory(
    model=models.QuestionAnswer,
    form=QuestionAnswerForm,
    extra=0
)
