"""
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def glossary_home(request):
    template = loader.get_template('finedu_pedia/pages/index.html')
    return HttpResponse(template.render())


def members(request):
    return HttpResponse("Hello world!")
"""


from typing import Any, Dict

from finedu_pedia.models import GlossaryPage, GlossaryItem
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

PER_PAGE = 12


class GlossaryItemListView(ListView):
    template_name = 'finedu_pedia/pages/glossary_index.html'
    context_object_name = 'glossary_items'
    paginate_by = PER_PAGE
    queryset = GlossaryItem.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })

        return context


class CreatedByListView(GlossaryItemListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name + ' - '

        ctx.update({
            'page_title': page_title,
        })

        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


class SearchListView(GlossaryItemListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_value = self._search_value
        ctx.update({
            'page_title': f'{search_value[:30]} - Search - ',
            'search_value': search_value,
        })
        return ctx

    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('finedu_pedia:index')
        return super().get(request, *args, **kwargs)


class GlossaryPageDetailView(DetailView):
    model = GlossaryPage
    template_name = 'finedu_pedia/pages/glossary_page.html'
    slug_field = 'slug'
    context_object_name = 'glossary_page'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        glossary_page = self.get_object()
        page_title = f'{glossary_page.title} - Página - '  # type: ignore
        ctx.update({
            'page_title': page_title,
        })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)


class GlossaryItemDetailView(DetailView):
    model = GlossaryItem
    template_name = 'finedu_pedia/pages/glossary_item.html'
    context_object_name = 'glossary_item'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        glossary_item = self.get_object()
        page_title = f'{glossary_item.title} - Post - '  # type: ignore
        ctx.update({
            'page_title': page_title,
        })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)
