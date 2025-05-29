from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    """
    Form for creating and updating Task instances.

    Dynamically filters the category queryset based on the logged-in user 
    and applies Bootstrap styling to all fields.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'status', 'categories']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}), 
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, customizing category queryset based on the user,
        and applying Bootstrap classes to widgets.
        """
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        
        # Apply Bootstrap classes to non-multiselect fields
        for field_name, field in self.fields.items():
            if field_name != 'categories':
                field.widget.attrs['class'] = 'form-control'
        
        # Limit category choices to those belonging to the user
        if user:
            self.fields['categories'].queryset = Category.objects.filter(user=user)

class CategoryForm(forms.ModelForm):
    """
    Form for creating and updating Category instances.
    """
    class Meta:
        model = Category
        fields = ['name']
