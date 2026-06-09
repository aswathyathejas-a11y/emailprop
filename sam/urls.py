from django.urls import path
from .views import (
    RegisterView,
    VerifyOTPView,
    LoginView,
    ResendOTPView,
    ForgotPasswordView,
    ResetPasswordView,AdminLoginView,AddProductView,ProductListView,
    ProductDetailView,AddToCartView,AddToWishlistView,UserListView,AdminCartView,
    SearchProductView,RecentSearchView,RecommendationView,UserDetailView,
    AdminProductListView,UpdateProductView,DeleteProductView)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('login/', LoginView.as_view()),
    path('resend-otp/', ResendOTPView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin-login/',AdminLoginView.as_view()),
    path('add-product/',AddProductView.as_view()),
    path('products/',ProductListView.as_view()),
    path('product/<int:pk>/',ProductDetailView.as_view()),
    path('add-cart/',AddToCartView.as_view()),
    path('add-wishlist/',AddToWishlistView.as_view()),
    path('search-product/',SearchProductView.as_view()),
    path('recent-searches/',RecentSearchView.as_view()),
    path('recommendations/',RecommendationView.as_view()),
    path('admin/products/',AdminProductListView.as_view()),
    path('admin/product/update/<int:pk>/',UpdateProductView.as_view()),
    path('admin/product/delete/<int:pk>/',DeleteProductView.as_view()),
    path('admin/users/',UserListView.as_view()),
    path('admin/user/<int:pk>/',UserDetailView.as_view()),
    path('admin/carts/',AdminCartView.as_view()),


]