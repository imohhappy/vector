from .models import Category, Product, OrderItem
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .carts import Cart
from .forms import CartAddProductForm, OrderForm


class CategoryView(ListView):
    model = Category
    template_name = 'catalog/item.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()[:3]
        context['category1'] = Category.objects.all()[3:6]
        context['category2'] = Category.objects.all()[6:9]
        context['category3'] = Category.objects.all()[9:12]

        return context


class CategoryDetail(DetailView):
    model = Category
    template_name = 'catalog/detail.html'
    context_object_name = 'product_detail'


def product_detail(request, category_id, slug):
    product = get_object_or_404(Product, category_id=category_id, slug=slug, avaliable=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'catalog/cloth.html', {'product': product, 'cart_product_form': cart_product_form})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('product:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('product:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'catalog/cart.html', {'cart': cart})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
    # clear the cart
            cart.clear()
            return render(request, 'catalog/created.html', {'order': order})
    else:
        form = OrderForm()
    return render(request, 'catalog/create.html', {'cart': cart, 'form': form})
