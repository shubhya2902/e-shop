from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('master/',views.Master,name="master"),
    path('',views.Index,name="index"),

    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('accounts/',include('django.contrib.auth.urls')),


    # add to cart

    path('cart/add/<int:id>',views.cart_add,name="cart_add"),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment,name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail,name='cart_detail'),


    # contact page

    path('contact/',views.contact_page,name="contact_page"),


    # Checkout page
    path('checkout/',views.checkout,name="checkout"),

    # order page
    path('order/',views.your_order,name='order'),

    # Product page
    path('product/',views.Product_page,name='product'),

    # Product detail page
    path('product/<str:id>',views.Product_detail,name="product_detail"),

    # Search page
    path('search/',views.Search,name='search'),

    # Account Page
    path('account/',views.Account,name='account'),

    # Info Page
    path('info/',views.info,name='info')

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
