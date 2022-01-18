
from authentication import views
from django.conf.urls.static import static
from django.conf import settings


from django.urls import path


from .views import Home,register_user
from django.conf.urls import url
from django.contrib.auth.views import LogoutView


from django.views.static import serve

urlpatterns = [
    path('',views.index,name='index'),
    path('signin', views.signin, name="signin"),
    path('users',views.users,name="users"),
    path('bonus',views.bonus,name="bonus"),
    path('showrole',views.showrole,name="showrole"),
    path('showrewards',views.showrewards,name="showrewards"),
    path('normallist',views.normallist,name="normallist"),
    path('showdeal',views.showdeal,name="showdeal"),
     path('saleslist',views.saleslist,name="saleslist"),
    path('edit/<int:id>',views.edit,name="edit"),
    path('useredit/<int:id>',views.useredit,name="useredit"),
    path('user/<int:id>/edit-role', views.edit_user_role, name="userEditRole"),
    path('user/<int:id>/edit_business', views.edit_business, name="userEditBusiness"),
    path('categoryedit/<int:id>',views.categoryedit,name="categoryredit"),
    path('roleedit/<int:id>',views.roledit,name="roledit"),
     path('dealedit/<int:id>',views.dealedit,name="dealedit"),
    path('update/<int:id>',views.update,name="update"),
    path('userupdate/<int:id>',views.userupdate,name="userupdate"),
    path('categoryupdate/<int:id>',views.categoryupdate,name="categoryupdate"),
    path('role/<int:id>/update',views.roleupdate,name="roleupdate"),
    path('dealupdate/<int:id>',views.dealupdate,name="dealupdate"),
    path('userdelete/<int:id>',views.userdelete,name="userdelete"),
    path('delete/<int:id>',views.delete,name="delete"),
    path('catgeories/<int:id>/delete',views.categorydelete,name="categorydelete"),
    path('roledelete/<int:id>',views.roledelete,name="roledelete"),
    path('deal/<int:id>/delete',views.dealdelete,name="dealdelete"),
    path('getbooks', views.get_books),
    path('rewardsapi',views.rewardsapi,name="rewardsapi"),
    path('rewardcreation',views.rewardcreation,name="rewardcreation"),
    path('dealapi',views.dealapi,name="dealapi"),
    path('loginApi',views.loginApi.as_view()),
     path('trans', views.trans,name='trans'),
     path('show_users',views.show_users,name="show_users"),
     path('normalcategories',views.normalcategories,name="normalcategories"),
     path('normaltransactions',views.normaltransactions,name="normaltransactions"),
     path('normalpayment',views.normalpayment,name="normalpayment"),
      path('favourites',views.favourites,name="favourites"),
    path('businesslist',views.businesslist,name="businesslist"),
    path('businessupdate/<int:id>',views.businessupdate,name="businessupdate"),
    path('addsales', views.addsales,name='addsales'),
    path('normaluser', views.normaluser,name='normaluser'),
    path('transactions', views.transactions, name="transactions"),
    path('role', views.role, name="role"),
    path('adduser',views.adduser.as_view()),
    path('createdeal', views.createdeal, name="createdeal"),
    path('wallets', views.wallets, name="wallets"),
    path('mybusiness', views.mybusiness, name="mybusiness"),
    path('business_favourite/<int:id>', views.business_favourite, name="business_favourite"),
    path('business_list', views.business_list, name="business_list"),
    path('register_user', views.register_user, name="register_user"),
    path('paysection', views.paysection.as_view()),
    path('business/<int:id>/payment', views.payment, name="payment"),
    path('walletsection', views.walletsection, name="walletsection"),
    path('paymentss', views.paymentss, name="paymentss"),
    path('show_business', views.show_business, name="show_business"),
    path('business/<int:id>/business_pay', views.business_pay, name="business_pay"),
    path('setting', views.setting, name="setting"),
    path('notification', views.notification, name="notification"),
    path("logout", views.logout, name="logout"),
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
    path('search_map', views.search_map, name="search_map"),

    path('BusinessAdd', views.BusinessAddApi.as_view()),
    


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
