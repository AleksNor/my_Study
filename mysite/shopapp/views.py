"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазинаЖ по товарам, заказам и т.д.
"""

import logging
from timeit import default_timer
from csv import DictWriter

from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import (HttpResponse,
                         HttpRequest,
                         HttpResponseRedirect,
                         JsonResponse)
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .common import save_csv_products
from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer


log = logging.getLogger(__name__)

@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.

    Полный CRUD для сущностей товара
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Get one product by ID",
        description="Retrives **product**, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by id not found"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response

    @action(
        detail=False,
        methods=["post"],
        parser_classes=[MultiPartParser],
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ShopIndexView(View):

    # @method_decorator(cache_page(60))
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
            'items': 3,
        }
        log.debug('Products for shop index: %s', products)
        log.info('Rendering shop index')
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm
    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.cteate(
                product=self.object,
                image=image,
            )

        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )

class OrdersDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("shopapp:orders_list")


class OrdersUpdateView(UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

    # def form_valid(self, form):
    #     success_url = self.get_success_url()
    #     self.object.archived = True
    #     self.object.save()
    #     return HttpResponseRedirect(success_url)

class ProductDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)

        return JsonResponse({"products": products_data})