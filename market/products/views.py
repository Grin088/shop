from django.shortcuts import render, redirect # noqa F401
from django.views.generic import TemplateView, CreateView
from rest_framework.views import APIView
from django.http import JsonResponse
from products.models import Review, Product
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .forms import ReviewFrom


class ReviewsAPI(APIView):

    def get(self, request):
        product_id = request.GET.get("product_id")
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 3))
        reviews = Review.objects.exclude(customer=request.user.id).filter(product_id=product_id)[offset:offset + limit]
        data = [{"user": r.customer.email, "product": r.product.name, "rating": r.rating, "text": r.review_text} for r in reviews]
        return JsonResponse({"data": data})


class ProductReviewsView(TemplateView):
    template_name = 'reviews.jinja2'
    form_class = ReviewFrom

    def get_context_data(self, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(id=product_id)
        reviews = product.count_reviews()
        can_add_review = Review.objects.select_related('customer').select_related('product').filter(customer=self.request.user.id, product_id=product_id).first()
        context = super().get_context_data(**kwargs)
        context['product_id'] = product_id
        context['form'] = self.form_class()
        context['can_add_review'] = can_add_review
        context['reviews'] = reviews
        context['user'] = self.request.user
        return context

    def post(self, request, product_id):
        form = self.form_class(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.customer_id = request.user.id
            review.product_id = product_id
            review.save()
            return redirect('/')
        else:
            context = self.get_context_data(product_id=product_id)
            context['form'] = form
            return self.render_to_response(context)
