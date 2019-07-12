import os
import re
import base64
from django import forms
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django_ace import AceWidget
from .models import Feedback, Question, Answer, QuestionAnswer


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        exclude = ['date_summitted']

    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your message...'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'username@mail.com'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('message', css_class='col-12'),
                css_class='form-row mb-4'
            ),
            Row(
                Column('email', css_class='col-12'),
                css_class='form-row mb-4'
            ),
            Row(
                Submit('submit', 'SEND FEEDBACK', css_class='btn btn-primary btn-block'),
                css_class='form-row px-1'
            )
        )


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['code', 'question_text', 'questioner']

    code = forms.CharField(widget=AceWidget(
        mode='python',
        theme='monokai',
        width='100%',
        tabsize=4,
        minlines=12,
        maxlines=12,
        wordwrap=True
    ))
    question_text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Your question...',
        'rows': 3
    }))
    questioner = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'username@mail.com'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('code', css_class='col-12'),
                css_class='form-row mb-3'
            ),
            Row(
                Column('question_text', css_class='col-12'),
                css_class='form-row mb-2'
            ),
            Row(
                Column('questioner', css_class='col-12'),
                css_class='form-row mb-2'
            ),
            Row(
                Submit('submit', 'SUBMIT QUESTION', css_class='btn btn-success btn-block'),
                css_class='form-row mb-2 px-1'
            )
        )

    def clean_code(self):
        code = self.cleaned_data.get("code", None)

        if len(code.split('\n')) > 1000:
            raise forms.ValidationError('You cannot submit more than 1000 lines!', code='invalid')

        return code


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['code', 'explanation']

    code = forms.CharField(widget=AceWidget(
        mode='python',
        theme='monokai',
        width='100%',
        tabsize=4,
        minlines=12,
        maxlines=12,
        wordwrap=True
    ))
    explanation = forms.CharField(widget=AceWidget(
        mode='markdown',
        width='100%',
        minlines=5,
        maxlines=5
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('code', css_class='col-12'),
                css_class='form-row mb-3'
            ),
            Row(
                Column('explanation', css_class='col-12'),
                css_class='form-row mb-2'
            ),
            Row(
                Submit('submit', 'CREATE ANSWER', css_class='btn btn-info btn-block'),
                css_class='form-row mb-2 px-1'
            )
        )


class AnswerOutputForm(forms.Form):

    image_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'answer_output_form'
        self.helper.form_method = 'post'

    def save_screenshot(self, filename):
        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        image_data = self.cleaned_data['image_data']
        image_data = dataUrlPattern.match(image_data).group(2)
        image_data = image_data.encode()
        image_data = base64.b64decode(image_data)

        with open(os.path.join(settings.BASE_DIR, 'answers', filename), 'wb') as f:
            f.write(image_data)