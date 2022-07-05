from django.views.generic import DetailView, ListView


from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['object'] = context['object'].content
        return context
