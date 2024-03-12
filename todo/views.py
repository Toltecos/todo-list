from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from todo.models import Task, Tag
from todo.forms import TaskForm, SearchForm


class TagListView(generic.ListView):
    model = Tag
    paginate_by = 5

    def get_context_data(self, **kwargs):
        search = self.request.GET.get("name")
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(
            search_field="name",
            search_query=search
        )
        return context

    def get_queryset(self):
        queryset = Tag.objects.order_by("id")
        search = self.request.GET.get("name")
        if search:
            return queryset.filter(name__icontains=search)
        return queryset


class TagCreateView(generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("todo:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("todo:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("todo:tag-list")


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, **kwargs):
        search = self.request.GET.get("content")
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(
            search_field="content",
            search_query=search
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.order_by('is_done', '-created_datetime')
        search = self.request.GET.get("content")
        if search:
            return queryset.filter(content__icontains=search)
        return queryset


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("todo:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("todo:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("todo:task-list")


def toggle_complete_to_task(request, pk):
    task = Task.objects.get(id=pk)
    if task.is_done:
        task.is_done = False
    else:
        task.is_done = True
    task.save()
    return HttpResponseRedirect(reverse_lazy("todo:task-list"))
