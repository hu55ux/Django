from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import Product, Review
from .forms import ReviewForm, UserRegisterForm, UserLoginForm

def product_list(request):
    """Product catalog list page"""
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, pk):
    """Product details page with associated reviews and review submission form"""
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.select_related('user').all()

    form = ReviewForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to write a review.")
            return redirect('login')

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted successfully!")
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(request, "Please correct the errors in the form below.")

    context = {
        'product': product,
        'reviews': reviews,
        'form': form
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def edit_review(request, pk):
    """Allow user to edit ONLY their own review"""
    review = get_object_or_404(Review, pk=pk)

    # Rule: Only review author can edit their own review
    if review.user != request.user:
        messages.error(request, "You can only edit your own review!")
        raise PermissionDenied("You can only edit your own review!")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated successfully!")
            return redirect('product_detail', pk=review.product.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'products/edit_review.html', {
        'form': form,
        'review': review
    })


@login_required
def delete_review(request, pk):
    """Allow user to delete ONLY their own review"""
    review = get_object_or_404(Review, pk=pk)
    product_pk = review.product.pk

    # Rule: Only review author can delete their own review
    if review.user != request.user:
        messages.error(request, "You can only delete your own review!")
        raise PermissionDenied("You can only delete your own review!")

    if request.method == 'POST':
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect('product_detail', pk=product_pk)

    return render(request, 'products/delete_confirm.html', {'review': review})


# --- Authentication Views ---

def register_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account was created successfully.")
            return redirect('product_list')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'product_list')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('product_list')
