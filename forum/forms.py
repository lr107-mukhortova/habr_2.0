from .models import Post
from django.forms import ModelForm, Textarea, TextInput


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['model_name', 'short_description',
                  'full_description', 'ref_on_git']
        widgets = {
            'model_name': TextInput(attrs={'class': 'form-control'}),
            'short_description': Textarea(attrs={'cols': 80, 'rows': 5, 'class': 'form-control'}),
            'full_description': Textarea(attrs={'cols': 80, 'rows': 5, 'class': 'form-control'}),
            'ref_on_git': TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'model_name': 'Название',
            'short_description': 'Описание',
            'full_description': 'Текст',
            'ref_on_git': 'Ссылка на гит',

        }

    def is_valid(self) -> bool:
        per = super().is_valid()
        per_2 = 'https://github.com' in self.cleaned_data['ref_on_git']
        self.add_error(None, 'неправильная ссылка на гит')
        return per and per_2
