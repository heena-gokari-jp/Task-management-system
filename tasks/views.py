# # from django.shortcuts import render, redirect, get_object_or_404
# # from django.contrib.auth.decorators import login_required
# # from django.contrib import messages
# # from django.db.models import Q
# # from .models import Task, Category
# # from .forms import TaskForm, CategoryForm


# # @login_required
# # def task_list(request):
# #     """
# #     Display a list of tasks for the logged-in user with filtering, searching, and sorting.

# #     Supports filtering by status, priority, and category, as well as searching
# #     by title, description, or category name. Also allows sorting by due date or priority.

# #     Template: tasks/task_list.html
# #     """
# #     try:
# #         tasks = Task.objects.filter(user=request.user)

# #         # Filters
# #         status_filter = request.GET.get('status')
# #         if status_filter:
# #             tasks = tasks.filter(status=status_filter)

# #         priority_filter = request.GET.get('priority')
# #         if priority_filter:
# #             tasks = tasks.filter(priority=priority_filter)

# #         category_filter = request.GET.get('category')
# #         if category_filter:
# #             tasks = tasks.filter(categories__id=category_filter)

# #         # Search
# #         search_query = request.GET.get('search')
# #         if search_query:
# #             tasks = tasks.filter(
# #                 Q(title__icontains=search_query) |
# #                 Q(description__icontains=search_query) |
# #                 Q(categories__name__icontains=search_query)
# #             ).distinct()

# #         # Sort
# #         sort_by = request.GET.get('sort_by')
# #         if sort_by == 'due_date':
# #             tasks = tasks.order_by('due_date')
# #         elif sort_by == 'priority':
# #             tasks = tasks.order_by('-priority')  # Simplified sorting logic

# #         categories = Category.objects.filter(user=request.user)

# #         context = {
# #             'tasks': tasks,
# #             'categories': categories,
# #             'current_status': status_filter,
# #             'current_priority': priority_filter,
# #             'current_category': category_filter,
# #             'search_query': search_query,
# #         }
# #         return render(request, 'tasks/task_list.html', context)
# #     except Exception as e:
# #         messages.error(request, f"An error occurred: {str(e)}")
# #         return render(request, 'tasks/task_list.html', {'tasks': [], 'categories': []})


# # @login_required
# # def task_detail(request, pk):
# #     """
# #     Display the details of a single task owned by the user.

# #     Args:
# #         pk (int): Primary key of the task.

# #     Template: tasks/task_detail.html
# #     """
# #     task = get_object_or_404(Task, pk=pk, user=request.user)
# #     return render(request, 'tasks/task_detail.html', {'task': task})


# # @login_required
# # def task_create(request):
# #     """
# #     Handle creation of a new task.

# #     On POST, validates and saves the task. On GET, displays the empty task form.

# #     Template: tasks/task_form.html
# #     """
# #     if request.method == 'POST':
# #         form = TaskForm(request.POST, user=request.user)
# #         if form.is_valid():
# #             try:
# #                 task = form.save(commit=False)
# #                 task.user = request.user
# #                 task.save()
# #                 form.save_m2m()
# #                 messages.success(request, 'Task created successfully!')
# #                 return redirect('tasks:task_list')
# #             except Exception as e:
# #                 messages.error(request, f"An error occurred while creating the task: {str(e)}")
# #         else:
# #             print(form.errors)
# #     else:
# #         form = TaskForm(user=request.user)

# #     return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})


# # @login_required
# # def task_update(request, pk):
# #     """
# #     Handle editing of an existing task.

# #     Args:
# #         pk (int): Primary key of the task.

# #     On POST, saves the updated task. On GET, shows pre-filled form.

# #     Template: tasks/task_form.html
# #     """
# #     task = get_object_or_404(Task, pk=pk, user=request.user)

# #     if request.method == 'POST':
# #         form = TaskForm(request.POST, instance=task, user=request.user)
# #         if form.is_valid():
# #             try:
# #                 form.save()
# #                 messages.success(request, 'Task updated successfully!')
# #                 return redirect('tasks:task_detail', pk=task.pk)
# #             except Exception as e:
# #                 messages.error(request, f"An error occurred while updating the task: {str(e)}")
# #         else:
# #             print(form.errors)
# #     else:
# #         form = TaskForm(instance=task, user=request.user)

# #     return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Update Task'})


# # @login_required
# # def task_delete(request, pk):
# #     """
# #     Handle deletion of a task.

# #     Args:
# #         pk (int): Primary key of the task.

# #     Template: tasks/task_confirm_delete.html
# #     """
# #     task = get_object_or_404(Task, pk=pk, user=request.user)

# #     if request.method == 'POST':
# #         try:
# #             task.delete()
# #             messages.success(request, 'Task deleted successfully!')
# #             return redirect('tasks:task_list')
# #         except Exception as e:
# #             messages.error(request, f"An error occurred while deleting the task: {str(e)}")

# #     return render(request, 'tasks/task_confirm_delete.html', {'task': task})


# # @login_required
# # def category_list(request):
# #     """
# #     Display a list of categories owned by the user.

# #     Template: tasks/category_list.html
# #     """
# #     categories = Category.objects.filter(user=request.user)
# #     return render(request, 'tasks/category_list.html', {'categories': categories})


# # @login_required
# # def category_create(request):
# #     """
# #     Handle creation of a new category.

# #     On POST, validates and saves the category. On GET, shows a blank form.

# #     Template: tasks/category_form.html
# #     """
# #     if request.method == 'POST':
# #         form = CategoryForm(request.POST)
# #         if form.is_valid():
# #             try:
# #                 category = form.save(commit=False)
# #                 category.user = request.user
# #                 category.save()
# #                 messages.success(request, 'Category created successfully!')
# #                 return redirect('tasks:category_list')
# #             except Exception as e:
# #                 messages.error(request, f"An error occurred while creating the category: {str(e)}")
# #     else:
# #         form = CategoryForm()

# #     return render(request, 'tasks/category_form.html', {'form': form})


# # @login_required
# # def category_delete(request, pk):
# #     """
# #     Handle deletion of a category.

# #     Args:
# #         pk (int): Primary key of the category.

# #     Template: tasks/category_confirm_delete.html
# #     """
# #     category = get_object_or_404(Category, pk=pk, user=request.user)

# #     if request.method == 'POST':
# #         try:
# #             category.delete()
# #             messages.success(request, 'Category deleted successfully!')
# #             return redirect('tasks:category_list')
# #         except Exception as e:
# #             messages.error(request, f"An error occurred while deleting the category: {str(e)}")

# #     return render(request, 'tasks/category_confirm_delete.html', {'category': category})


# from django.core.serializers.json import DjangoJSONEncoder
# from django.forms import model_to_dict
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db.models import Q
# from .models import Task, Category
# from .forms import TaskForm, CategoryForm
# import json
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import JsonResponse
# from datetime import datetime, timedelta

# from django.core.serializers.json import DjangoJSONEncoder
# from django.forms import model_to_dict
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db.models import Q
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import JsonResponse
# from django.utils import timezone
# from datetime import datetime, timedelta
# from .models import Task, Category
# from .forms import TaskForm, CategoryForm
# import json


# @login_required
# def task_list(request):
#     """
#     Enhanced task list with pagination, filtering, and search.
#     """
#     try:
#         tasks = Task.objects.filter(user=request.user).prefetch_related('categories')

#         # Filters
#         status_filter = request.GET.get('status')
#         if status_filter:
#             tasks = tasks.filter(status=status_filter)

#         priority_filter = request.GET.get('priority')
#         if priority_filter:
#             tasks = tasks.filter(priority=priority_filter)

#         category_filter = request.GET.get('category')
#         if category_filter:
#             tasks = tasks.filter(categories__id=category_filter)

#         # Search
#         search_query = request.GET.get('search')
#         if search_query:
#             tasks = tasks.filter(
#                 Q(title__icontains=search_query) |
#                 Q(description__icontains=search_query) |
#                 Q(categories__name__icontains=search_query)
#             ).distinct()

#         # Sort
#         sort_by = request.GET.get('sort_by')
#         if sort_by == 'due_date':
#             tasks = tasks.order_by('due_date')
#         elif sort_by == 'priority':
#             tasks = tasks.extra(
#                 select={'priority_order': "CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END"},
#                 order_by=['priority_order']
#             )
#         else:
#             tasks = tasks.order_by('-created_at')

#         # Pagination - 10 tasks per page
#         paginator = Paginator(tasks, 10)
#         page = request.GET.get('page')

#         try:
#             tasks_page = paginator.page(page)
#         except PageNotAnInteger:
#             tasks_page = paginator.page(1)
#         except EmptyPage:
#             tasks_page = paginator.page(paginator.num_pages)

#         categories = Category.objects.filter(user=request.user)

#         context = {
#             'tasks': tasks_page,
#             'categories': categories,
#             'current_status': status_filter,
#             'current_priority': priority_filter,
#             'current_category': category_filter,
#             'search_query': search_query,
#             'page_obj': tasks_page,
#             'now': timezone.now(),
#         }
#         return render(request, 'tasks/task_list_enhanced.html', context)
#     except Exception as e:
#         messages.error(request, f"An error occurred: {str(e)}")
#         return render(request, 'tasks/task_list_enhanced.html', {'tasks': [], 'categories': []})


# @login_required
# def task_detail(request, pk):
#     """
#     Display the details of a single task owned by the user.

#     Args:
#         pk (int): Primary key of the task.

#     Template: tasks/task_detail.html
#     """
#     task = get_object_or_404(Task, pk=pk, user=request.user)
#     return render(request, 'tasks/task_detail.html', {'task': task})


# @login_required
# def task_create(request):
#     """
#     Handle creation of a new task.

#     On POST, validates and saves the task. On GET, displays the empty task form.

#     Template: tasks/task_form.html
#     """
#     if request.method == 'POST':
#         form = TaskForm(request.POST, user=request.user)
#         if form.is_valid():
#             try:
#                 task = form.save(commit=False)
#                 task.user = request.user
#                 task.save()
#                 form.save_m2m()
#                 messages.success(request, 'Task created successfully!')
#                 return redirect('tasks:task_list')
#             except Exception as e:
#                 messages.error(request, f"An error occurred while creating the task: {str(e)}")
#         else:
#             print(form.errors)
#     else:
#         form = TaskForm(user=request.user)

#     return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})


# @login_required
# def task_update(request, pk):
#     """
#     Handle editing of an existing task.

#     Args:
#         pk (int): Primary key of the task.

#     On POST, saves the updated task. On GET, shows pre-filled form.

#     Template: tasks/task_form.html
#     """
#     task = get_object_or_404(Task, pk=pk, user=request.user)

#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task, user=request.user)
#         if form.is_valid():
#             try:
#                 form.save()
#                 messages.success(request, 'Task updated successfully!')
#                 return redirect('tasks:task_detail', pk=task.pk)
#             except Exception as e:
#                 messages.error(request, f"An error occurred while updating the task: {str(e)}")
#         else:
#             print(form.errors)
#     else:
#         form = TaskForm(instance=task, user=request.user)

#     return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Update Task'})


# @login_required
# def task_delete(request, pk):
#     """
#     Handle deletion of a task.

#     Args:
#         pk (int): Primary key of the task.

#     Template: tasks/task_confirm_delete.html
#     """
#     task = get_object_or_404(Task, pk=pk, user=request.user)

#     if request.method == 'POST':
#         try:
#             task.delete()
#             messages.success(request, 'Task deleted successfully!')
#             return redirect('tasks:task_list')
#         except Exception as e:
#             messages.error(request, f"An error occurred while deleting the task: {str(e)}")

#     return render(request, 'tasks/task_confirm_delete.html', {'task': task})


# @login_required
# def category_list(request):
#     """
#     Display a list of categories owned by the user.

#     Template: tasks/category_list.html
#     """
#     categories = Category.objects.filter(user=request.user)
#     return render(request, 'tasks/category_list.html', {'categories': categories})


# @login_required
# def category_create(request):
#     """
#     Handle creation of a new category.

#     On POST, validates and saves the category. On GET, shows a blank form.

#     Template: tasks/category_form.html
#     """
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             try:
#                 category = form.save(commit=False)
#                 category.user = request.user
#                 category.save()
#                 messages.success(request, 'Category created successfully!')
#                 return redirect('tasks:category_list')
#             except Exception as e:
#                 messages.error(request, f"An error occurred while creating the category: {str(e)}")
#     else:
#         form = CategoryForm()

#     return render(request, 'tasks/category_form.html', {'form': form})


# @login_required
# def category_delete(request, pk):
#     """
#     Handle deletion of a category.

#     Args:
#         pk (int): Primary key of the category.

#     Template: tasks/category_confirm_delete.html
#     """
#     category = get_object_or_404(Category, pk=pk, user=request.user)

#     if request.method == 'POST':
#         try:
#             category.delete()
#             messages.success(request, 'Category deleted successfully!')
#             return redirect('tasks:category_list')
#         except Exception as e:
#             messages.error(request, f"An error occurred while deleting the category: {str(e)}")

#     return render(request, 'tasks/category_confirm_delete.html', {'category': category})


# @login_required
# def dashboard(request):
#     """
#     Asana-like dashboard with visual task management.
#     """
#     return render(request, 'tasks/dashboard.html')

# @login_required
# def task_notifications(request):
#     """
#     Notification center for task alerts and reminders.
#     """
#     # Get tasks due in the next 7 days
#     upcoming_due = Task.objects.filter(
#         user=request.user,
#         due_date__gte=datetime.now(),
#         due_date__lte=datetime.now() + timedelta(days=7),
#         status__in=['pending', 'in_progress']
#     ).order_by('due_date')

#     # Get overdue tasks
#     overdue_tasks = Task.objects.filter(
#         user=request.user,
#         due_date__lt=datetime.now(),
#         status__in=['pending', 'in_progress']
#     ).order_by('due_date')

#     # Get recently completed tasks (last 7 days)
#     recently_completed = Task.objects.filter(
#         user=request.user,
#         status='completed',
#         updated_at__gte=datetime.now() - timedelta(days=7)
#     ).order_by('-updated_at')

#     context = {
#         'upcoming_due': upcoming_due,
#         'overdue_tasks': overdue_tasks,
#         'recently_completed': recently_completed,
#     }

#     return render(request, 'tasks/notifications.html', context)

# @login_required
# def notifications_count(request):
#     """
#     API endpoint for real-time notification count.
#     """
#     try:
#         # Get overdue tasks count
#         overdue_count = Task.objects.filter(
#             user=request.user,
#             due_date__lt=datetime.now(),
#             status__in=['pending', 'in_progress']
#         ).count()

#         # Get tasks due in next 2 days
#         due_soon_count = Task.objects.filter(
#             user=request.user,
#             due_date__gte=datetime.now(),
#             due_date__lte=datetime.now() + timedelta(days=2),
#             status__in=['pending', 'in_progress']
#         ).count()

#         total_count = overdue_count + due_soon_count

#         return JsonResponse({
#             'count': total_count,
#             'overdue': overdue_count,
#             'due_soon': due_soon_count
#         })

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

# @login_required
# def task_dashboard_stats(request):
#     """
#     API endpoint for dashboard statistics.
#     """
#     total_tasks = Task.objects.filter(user=request.user).count()
#     pending_tasks = Task.objects.filter(user=request.user, status='pending').count()
#     in_progress_tasks = Task.objects.filter(user=request.user, status='in_progress').count()
#     completed_tasks = Task.objects.filter(user=request.user, status='completed').count()

#     high_priority_tasks = Task.objects.filter(
#         user=request.user,
#         priority='high',
#         status__in=['pending', 'in_progress']
#     ).count()

#     overdue_tasks = Task.objects.filter(
#         user=request.user,
#         due_date__lt=datetime.now(),
#         status__in=['pending', 'in_progress']
#     ).count()

#     stats = {
#         'total_tasks': total_tasks,
#         'pending_tasks': pending_tasks,
#         'in_progress_tasks': in_progress_tasks,
#         'completed_tasks': completed_tasks,
#         'high_priority_tasks': high_priority_tasks,
#         'overdue_tasks': overdue_tasks,
#         'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
#     }

#     return JsonResponse(stats)


# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db.models import Q
# from .models import Task, Category
# from .forms import TaskForm, CategoryForm


# @login_required
# def task_list(request):
#     """
#     Display a list of tasks for the logged-in user with filtering, searching, and sorting.

#     Supports filtering by status, priority, and category, as well as searching
#     by title, description, or category name. Also allows sorting by due date or priority.

#     Template: tasks/task_list.html
#     """
#     try:
#         tasks = Task.objects.filter(user=request.user)

#         # Filters
#         status_filter = request.GET.get('status')
#         if status_filter:
#             tasks = tasks.filter(status=status_filter)

#         priority_filter = request.GET.get('priority')
#         if priority_filter:
#             tasks = tasks.filter(priority=priority_filter)

#         category_filter = request.GET.get('category')
#         if category_filter:
#             tasks = tasks.filter(categories__id=category_filter)

#         # Search
#         search_query = request.GET.get('search')
#         if search_query:
#             tasks = tasks.filter(
#                 Q(title__icontains=search_query) |
#                 Q(description__icontains=search_query) |
#                 Q(categories__name__icontains=search_query)
#             ).distinct()

#         # Sort
#         sort_by = request.GET.get('sort_by')
#         if sort_by == 'due_date':
#             tasks = tasks.order_by('due_date')
#         elif sort_by == 'priority':
#             tasks = tasks.order_by('-priority')  # Simplified sorting logic

#         categories = Category.objects.filter(user=request.user)

#         context = {
#             'tasks': tasks,
#             'categories': categories,
#             'current_status': status_filter,
#             'current_priority': priority_filter,
#             'current_category': category_filter,
#             'search_query': search_query,
#         }
#         return render(request, 'tasks/task_list.html', context)
#     except Exception as e:
#         messages.error(request, f"An error occurred: {str(e)}")
#         return render(request, 'tasks/task_list.html', {'tasks': [], 'categories': []})


# @login_required
# def task_detail(request, pk):
#     """
#     Display the details of a single task owned by the user.

#     Args:
#         pk (int): Primary key of the task.

#     Template: tasks/task_detail.html
#     """
#     task = get_object_or_404(Task, pk=pk, user=request.user)
#     return render(request, 'tasks/task_detail.html', {'task': task})


# @login_required
# def task_create(request):
#     """
#     Handle creation of a new task.

#     On POST, validates and saves the task. On GET, displays the empty task form.

#     Template: tasks/task_form.html
#     """
#     if request.method == 'POST':
#         form = TaskForm(request.POST, user=request.user)
#         if form.is_valid():
#             try:
#                 task = form.save(commit=False)
#                 task.user = request.user
#                 task.save()
#                 form.save_m2m()
#                 messages.success(request, 'Task created successfully!')
#                 return redirect('tasks:task_list')
#             except Exception as e:
#                 messages.error(request, f"An error occurred while creating the task: {str(e)}")
#         else:
#             print(form.errors)
#     else:
#         form = TaskForm(user=request.user)

#     return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})


# @login_required
# def task_update(request, pk):
#     """
#     Handle editing of an existing task.

#     Args:
#         pk (int): Primary key of the task.

#     On POST, saves the updated task. On GET, shows pre-filled form.

#     Template: tasks/task_form.html
#     """
#     task = get_object_or_404(Task, pk=pk, user=request.user)

#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task, user=request.user)
#         if form.is_valid():
#             try:
#                 form.save()
#                 messages.success(request, 'Task updated successfully!')
#                 return redirect('tasks:task_detail', pk=task.pk)
#             except Exception as e:
#                 messages.error(request, f"An error occurred while updating the task: {str(e)}")
#         else:
#             print(form.errors)
#     else:
#         form = TaskForm(instance=task, user=request.user)

#     return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Update Task'})


# @login_required
# def task_delete(request, pk):
#     """
#     Handle deletion of a task.

#     Args:
#         pk (int): Primary key of the task.

#     Template: tasks/task_confirm_delete.html
#     """
#     task = get_object_or_404(Task, pk=pk, user=request.user)

#     if request.method == 'POST':
#         try:
#             task.delete()
#             messages.success(request, 'Task deleted successfully!')
#             return redirect('tasks:task_list')
#         except Exception as e:
#             messages.error(request, f"An error occurred while deleting the task: {str(e)}")

#     return render(request, 'tasks/task_confirm_delete.html', {'task': task})


# @login_required
# def category_list(request):
#     """
#     Display a list of categories owned by the user.

#     Template: tasks/category_list.html
#     """
#     categories = Category.objects.filter(user=request.user)
#     return render(request, 'tasks/category_list.html', {'categories': categories})


# @login_required
# def category_create(request):
#     """
#     Handle creation of a new category.

#     On POST, validates and saves the category. On GET, shows a blank form.

#     Template: tasks/category_form.html
#     """
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             try:
#                 category = form.save(commit=False)
#                 category.user = request.user
#                 category.save()
#                 messages.success(request, 'Category created successfully!')
#                 return redirect('tasks:category_list')
#             except Exception as e:
#                 messages.error(request, f"An error occurred while creating the category: {str(e)}")
#     else:
#         form = CategoryForm()

#     return render(request, 'tasks/category_form.html', {'form': form})


# @login_required
# def category_delete(request, pk):
#     """
#     Handle deletion of a category.

#     Args:
#         pk (int): Primary key of the category.

#     Template: tasks/category_confirm_delete.html
#     """
#     category = get_object_or_404(Category, pk=pk, user=request.user)

#     if request.method == 'POST':
#         try:
#             category.delete()
#             messages.success(request, 'Category deleted successfully!')
#             return redirect('tasks:category_list')
#         except Exception as e:
#             messages.error(request, f"An error occurred while deleting the category: {str(e)}")

#     return render(request, 'tasks/category_confirm_delete.html', {'category': category})


from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CategoryForm, TaskForm
from .models import Category, Task


@login_required
def task_list(request):
    """
    Enhanced task list with pagination, filtering, and search.
    """
    try:
        tasks = Task.objects.filter(user=request.user).prefetch_related("categories")

        # Filters
        status_filter = request.GET.get("status")
        if status_filter:
            tasks = tasks.filter(status=status_filter)

        priority_filter = request.GET.get("priority")
        if priority_filter:
            tasks = tasks.filter(priority=priority_filter)

        category_filter = request.GET.get("category")
        if category_filter:
            tasks = tasks.filter(categories__id=category_filter)

        # Search
        search_query = request.GET.get("search")
        if search_query:
            tasks = tasks.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(categories__name__icontains=search_query)
            ).distinct()

        # Sort
        sort_by = request.GET.get("sort_by")
        if sort_by == "due_date":
            tasks = tasks.order_by("due_date")
        elif sort_by == "priority":
            tasks = tasks.extra(
                select={
                    "priority_order": "CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END"
                },
                order_by=["priority_order"],
            )
        else:
            tasks = tasks.order_by("-created_at")

        # Pagination - 10 tasks per page
        paginator = Paginator(tasks, 10)
        page = request.GET.get("page")

        try:
            tasks_page = paginator.page(page)
        except PageNotAnInteger:
            tasks_page = paginator.page(1)
        except EmptyPage:
            tasks_page = paginator.page(paginator.num_pages)

        categories = Category.objects.filter(user=request.user)

        context = {
            "tasks": tasks_page,
            "categories": categories,
            "current_status": status_filter,
            "current_priority": priority_filter,
            "current_category": category_filter,
            "search_query": search_query,
            "page_obj": tasks_page,
            "now": timezone.now(),
        }
        return render(request, "tasks/task_list_enhanced.html", context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(
            request, "tasks/task_list_enhanced.html", {"tasks": [], "categories": []}
        )


@login_required
def task_detail(request, pk):
    """
    Display the details of a single task owned by the user.

    Args:
        pk (int): Primary key of the task.

    Template: tasks/task_detail.html
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, "tasks/task_detail.html", {"task": task})


@login_required
def task_create(request):
    """
    Handle creation of a new task.

    On POST, validates and saves the task. On GET, displays the empty task form.

    Template: tasks/task_form.html
    """
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                form.save_m2m()
                messages.success(request, "Task created successfully!")
                return redirect("tasks:task_list")
            except Exception as e:
                messages.error(
                    request, f"An error occurred while creating the task: {str(e)}"
                )
        else:
            print(form.errors)
    else:
        form = TaskForm(user=request.user)

    return render(
        request, "tasks/task_form.html", {"form": form, "title": "Create Task"}
    )


@login_required
def task_update(request, pk):
    """
    Handle editing of an existing task.

    Args:
        pk (int): Primary key of the task.

    On POST, saves the updated task. On GET, shows pre-filled form.

    Template: tasks/task_form.html
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Task updated successfully!")
                return redirect("tasks:task_detail", pk=task.pk)
            except Exception as e:
                messages.error(
                    request, f"An error occurred while updating the task: {str(e)}"
                )
        else:
            print(form.errors)
    else:
        form = TaskForm(instance=task, user=request.user)

    return render(
        request, "tasks/task_form.html", {"form": form, "title": "Update Task"}
    )


@login_required
def task_delete(request, pk):
    """
    Handle deletion of a task.

    Args:
        pk (int): Primary key of the task.

    Template: tasks/task_confirm_delete.html
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "POST":
        try:
            task.delete()
            messages.success(request, "Task deleted successfully!")
            return redirect("tasks:task_list")
        except Exception as e:
            messages.error(
                request, f"An error occurred while deleting the task: {str(e)}"
            )

    return render(request, "tasks/task_confirm_delete.html", {"task": task})


@login_required
def category_list(request):
    """
    Display a list of categories owned by the user.

    Template: tasks/category_list.html
    """
    categories = Category.objects.filter(user=request.user)
    return render(request, "tasks/category_list.html", {"categories": categories})


@login_required
def category_create(request):
    """
    Handle creation of a new category.

    On POST, validates and saves the category. On GET, shows a blank form.

    Template: tasks/category_form.html
    """
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                messages.success(request, "Category created successfully!")
                return redirect("tasks:category_list")
            except Exception as e:
                messages.error(
                    request, f"An error occurred while creating the category: {str(e)}"
                )
    else:
        form = CategoryForm()

    return render(request, "tasks/category_form.html", {"form": form})


@login_required
def category_delete(request, pk):
    """
    Handle deletion of a category.

    Args:
        pk (int): Primary key of the category.

    Template: tasks/category_confirm_delete.html
    """
    category = get_object_or_404(Category, pk=pk, user=request.user)

    if request.method == "POST":
        try:
            category.delete()
            messages.success(request, "Category deleted successfully!")
            return redirect("tasks:category_list")
        except Exception as e:
            messages.error(
                request, f"An error occurred while deleting the category: {str(e)}"
            )

    return render(request, "tasks/category_confirm_delete.html", {"category": category})


@login_required
def dashboard(request):
    """
    Asana-like dashboard with visual task management.
    """
    return render(request, "tasks/dashboard.html")


@login_required
def task_notifications(request):
    """
    Notification center for task alerts and reminders.
    """
    # Get tasks due in the next 7 days
    upcoming_due = Task.objects.filter(
        user=request.user,
        due_date__gte=datetime.now(),
        due_date__lte=timezone.now() + timedelta(days=7),
        status__in=["pending", "in_progress"],
    ).order_by("due_date")

    # Get overdue tasks
    overdue_tasks = Task.objects.filter(
        user=request.user,
        due_date__lt=datetime.now(),
        status__in=["pending", "in_progress"],
    ).order_by("due_date")

    # Get recently completed tasks (last 7 days)
    recently_completed = Task.objects.filter(
        user=request.user,
        status="completed",
        updated_at__gte=datetime.now() - timedelta(days=7),
    ).order_by("-updated_at")

    context = {
        "upcoming_due": upcoming_due,
        "overdue_tasks": overdue_tasks,
        "recently_completed": recently_completed,
    }

    return render(request, "tasks/notifications.html", context)


@login_required
def notifications_count(request):
    """
    API endpoint for real-time notification count.
    """
    try:
        # Get overdue tasks count
        overdue_count = Task.objects.filter(
            user=request.user,
            due_date__lt=datetime.now(),
            status__in=["pending", "in_progress"],
        ).count()

        # Get tasks due in next 2 days
        due_soon_count = Task.objects.filter(
            user=request.user,
            due_date__gte=datetime.now(),
            due_date__lte=datetime.now() + timedelta(days=2),
            status__in=["pending", "in_progress"],
        ).count()

        total_count = overdue_count + due_soon_count

        return JsonResponse(
            {"count": total_count, "overdue": overdue_count, "due_soon": due_soon_count}
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def task_dashboard_stats(request):
    """
    API endpoint for dashboard statistics.
    """
    total_tasks = Task.objects.filter(user=request.user).count()
    pending_tasks = Task.objects.filter(user=request.user, status="pending").count()
    in_progress_tasks = Task.objects.filter(
        user=request.user, status="in_progress"
    ).count()
    completed_tasks = Task.objects.filter(user=request.user, status="completed").count()

    high_priority_tasks = Task.objects.filter(
        user=request.user, priority="high", status__in=["pending", "in_progress"]
    ).count()

    overdue_tasks = Task.objects.filter(
        user=request.user,
        due_date__lt=datetime.now(),
        status__in=["pending", "in_progress"],
    ).count()

    stats = {
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completed_tasks": completed_tasks,
        "high_priority_tasks": high_priority_tasks,
        "overdue_tasks": overdue_tasks,
        "completion_rate": round(
            (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1
        ),
    }

    return JsonResponse(stats)
