from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'status', 'categories']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}), 
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        
                # Add Bootstrap classes directly
        for field_name, field in self.fields.items():
            if field_name != 'categories':
                field.widget.attrs['class'] = 'form-control'

        
        if user:
            self.fields['categories'].queryset = Category.objects.filter(user=user)
            # self.fields['categories'].required = False  # Make it optional
            # self.fields['categories'].label = "Categories (Hold Ctrl/Cmd to select multiple)"
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
