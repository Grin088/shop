from django.shortcuts import render  # noqa F401
from django.views.generic import TemplateView, DetailView, View
from products.services.review import ReviewHandler
# Create your views here.


class ReviewView(View):

    def get(self, request, pk: int):
        rev = ReviewHandler(product_id=pk)
        a = rev.get_review()
        first_part = next(a)
        self.request.session['asd'] = rev
        return render(request, 'product_review.jinja2', context={"reviews": first_part})

    def post(self, request, pk: int):
        rev = self.request.session.get('asd')
        next_p = rev.get_review()
        next_part = next(next_p)
        return render(request, 'product_review.jinja2', context={"reviews": next_part})


from django.http import JsonResponse
from products.models import Review


def reviews_api(request):
    product_id = request.GET.get("product_id")
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 3))

    reviews = Review.objects.filter(product_id=product_id)[offset:offset + limit]
    data = [{"user": r.customer.email, "product": r.product.name, "rating": r.rating, "text": r.review_text} for r in reviews]

    return JsonResponse({"data": data})




# class ReviewTemplate(TemplateView):
#     template_name = "reviews.jinja2"


def product_reviews(request, product_id):
    return render(request, 'reviews.jinja2', {'product_id': product_id})
