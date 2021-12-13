
from authentication import views
from django.conf.urls.static import static
from django.conf import settings


from django.urls import path


from .views import Home,register_user
from django.conf.urls import url
from django.contrib.auth.views import LogoutView


from django.views.static import serve

urlpatterns = [
    # path('index',views.index,name='index'),
    path('signin', views.signin, name="signin"),
    path('users',views.users,name="users"),
    path('edit/<int:id>',views.edit,name="edit"),
    path('useredit/<int:id>',views.useredit,name="useredit"),
    path('categoryedit/<int:id>',views.categoryedit,name="categoryredit"),
    path('update/<int:id>',views.update,name="update"),
    path('userupdate/<int:id>',views.userupdate,name="userupdate"),
    path('categoryupdate/<int:id>',views.categoryupdate,name="categoryupdate"),
    path('userdelete/<int:id>',views.userdelete,name="userdelete"),
    path('delete/<int:id>',views.delete,name="delete"),
    path('catgeories/<int:id>/delete',views.categorydelete,name="categorydelete"),
    path('getbooks', views.get_books),
     path('trans', views.trans,name='trans'),
  
    path('transactions', views.transactions, name="transactions"),
    path('role', views.role, name="role"),
    path('business_list', views.business_list, name="business_list"),
    path('', views.register_user, name="register_user"),
    path('paysection', views.paysection.as_view()),
    path('business/<int:id>/payment', views.payment, name="payment"),
    path('paymentss', views.paymentss, name="paymentss"),
    path('show_business', views.show_business, name="show_business"),
    path('business/<int:id>/business_pay', views.business_pay, name="business_pay"),
    path('setting', views.setting, name="setting"),
    path('notification', views.notification, name="notification"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('home', views.Home, name="home"),
    path('transact',views.transact,name="transact"),
    # path('business_lists', views.business_lists.as_view()),
    path('pay', views.pay, name="pay"),
    path('list', views.tablelist, name="list"),
    path('business', views.business, name="business"),
    path('category', views.Category, name="category"),
     path('categoryapi', views.Categoryapi, name="Categoryapi"),
    path('show_category', views.show_category, name="show_category"),
    path('categories', views.categories, name="categories"),
    path('shuffle', views.shuffle, name="shuffle"),
   
    


    # pyament checkout urls
    path('checkout-session', views.create_checkout_session, name="api"),
    path('payment-success', views.payment_success),
    path('payment-success', views.payment_cancel),
    path('payment-webhook', views.payment_webhook),
   
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
else:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
