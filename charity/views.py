from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, View
from .models import Article, Tag, Category
from typing import Any
from django.db.models.query import QuerySet
import stripe
from .forms import VolunteerForm, ContactForm
from django.conf import settings


def SearchNews(request):
    if request.method == 'POST':
        input = request.POST.get('search')
        result = Article.objects.filter(title__contains=input)
        context = {"articles": result}
        return render(request, 'news.html', context)


class BaseContextMixin(View):
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()[:5]
        context['categories'] = Category.objects.all()
        return context


class ShowArticle(BaseContextMixin, DetailView):
    model = Article
    template_name = 'news-detail.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()[:3]
        return context


class ArticleList(BaseContextMixin, ListView):
    model = Article
    template_name = 'news.html'
    context_object_name = 'articles'


def HomeList(request):
    volunteer_form = VolunteerForm
    if request.method == 'POST':
        volunteer_form = VolunteerForm(request.POST, request.FILES)
        if volunteer_form.is_valid():
            volunteer_form.save()
            redirect('home')

    context = {
        "tags": Tag.objects.all()[:5],
        "categories": Category.objects.all(),
        "volunteer_form": volunteer_form,
        "contact_form": ContactForm(request.POST),
        "articles": Article.objects.all()[:3]
    }

    return render(request, 'index.html', context=context)



class TagArticleList(BaseContextMixin, ListView):
    model = Article
    template_name = 'news.html'
    context_object_name = 'articles'

    def get_queryset(self) -> QuerySet[Any]:
        return Article.objects.filter(tags__slug=self.kwargs['tag_slug'])


class CategoryArticleList(BaseContextMixin, ListView):
    model = Article
    template_name = 'news.html'
    context_object_name = 'articles'

    def get_queryset(self) -> QuerySet[Any]:
        return Article.objects.filter(categories__slug=self.kwargs['category_slug'])


def SuccessfulPurchase(request):
    context = {
        "status": "Our regards for your contribution!"
    }
    return render(request, "donate.html", context=context)


def ScrewedupPurchase(request):
    context = {
        "status": "Unfortunately, your payment has failed! :("
    }
    return render(request, "donate.html", context=context)


def DonateView(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        try:
            amount = int(request.POST.get('amount')) * 100
        except:
            amount = int(request.POST.get('flexRadioDefault')) * 100
        mode = request.POST.get('DonationFrequency')

        checkout = stripe.checkout.Session.create(
            line_items=[{
                'quantity': 1,
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Donation',
                    },
                    'unit_amount': amount
                }
            }],
            mode=mode,
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('cancel'))
        )
        return redirect(checkout.url, code=303)

    return render(request, 'donate.html')
