from authentication import views
from django.conf.urls.static import static
from django.conf import settings


from django.urls import path
from .views import Home, login_view, register_user
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from .views import (HomepageView, BillListView,
                    PayrollListView, ExpensesListView,
                    report_view
                    )

from django.views.static import serve

urlpatterns = [
    # path('index',views.index,name='index'),
    path('', login_view, name="login"),
    path('homepage', HomepageView.as_view(), name='homepage'),

    path('bills/', BillListView.as_view(), name='bills_view'),
    path('payroll/', PayrollListView.as_view(), name='payroll_view'),
    path('expenses/', ExpensesListView.as_view(), name='expenses_view'),
    path('reports/', report_view, name='reports_view'),
    path('register/', register_user, name="register"),
    path('getbooks', views.get_books),
     path('trans', views.trans),
    # path('profile', views.profile),
    path('transactions', views.transactions, name="transactions"),
    path('business_list', views.business_list, name="business_list"),
    path('', views.register_user, name="register_user"),
    path('payment', views.payment, name="payment"),
    path('setting', views.setting, name="setting"),
    path('notification', views.notification, name="notification"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('home', views.Home, name="home"),
    path('pay', views.pay, name="pay"),
    path('list', views.tablelist, name="list"),
    path('category', views.categories, name="category"),
    path('show_category', views.show_category, name="show_category"),
    path('categories', views.apis, name="categories"),
   
    path('api/get/', views.api, name="api"),


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
