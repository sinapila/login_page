from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Product
from .models import ProductCategory, ProductBrand


# Create your views here.

class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = [
        # '-price'
    ]
    paginate_by = 6

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()

        category = self.kwargs.get('cat')
        brand = self.kwargs.get('brand')
        if category is not None:
            query = query.filter(category__url_title__iexact=category)
        else:
            if brand is not None:
                query = query.filter(brand__url_title__iexact=brand)

        return query


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()

        loaded_product = self.object
        request = self.request
        favarite_product_id = request.session.get('product_favarite')
        context['is_favorite'] = favarite_product_id == str(loaded_product.id)

        return context


class AddProductFavorite(View):
    def post(self, request):
        product_id = request.POST['product_id']
        product = Product.objects.get(pk=product_id)
        request.session['product_favarite'] = product_id
        return redirect(product.get_absolute_url())


def product_categories_component(request: HttpRequest):
    product_categorys = ProductCategory.objects.filter(is_active=True, is_delete=False)
    return render(request, 'product_module/components/product_categorys_components.html',
                  {'product_categorys': product_categorys,
                   'request':request})


def product_brand_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(product_count=Count('product')).filter(is_active=True)
    return render(request, 'product_module/components/product_brand_components.html',
                  {'product_brands': product_brands,
                   'request':request})
