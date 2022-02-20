
from authentication import views
from django.conf.urls.static import static
from django.conf import settings




from .views import Home,register_user
from django.conf.urls import url
from django.contrib.auth.views import LogoutView


from django.views.static import serve

urlpatterns = [
    url('',views.index,name='index'),
    url('signin', views.signin, name="signin"),
    url('users',views.users,name="users"),
    url('bonus',views.bonus,name="bonus"),
    url('showrole',views.showrole,name="showrole"),
    url('showrewards',views.showrewards,name="showrewards"),
    url('normallist',views.normallist,name="normallist"),
    url('showdeal',views.showdeal,name="showdeal"),
     url('saleslist',views.saleslist,name="saleslist"),
    url('edit/<int:id>',views.edit,name="edit"),
    url('useredit/<int:id>',views.useredit,name="useredit"),
    url('user/<int:id>/edit-role', views.edit_user_role, name="userEditRole"),
    url('user/<int:id>/edit_business', views.edit_business, name="userEditBusiness"),
    url('categoryedit/<int:id>',views.categoryedit,name="categoryredit"),
    url('roleedit/<int:id>',views.roledit,name="roledit"),
     url('dealedit/<int:id>',views.dealedit,name="dealedit"),
    url('update/<int:id>',views.update,name="update"),
    url('userupdate/<int:id>',views.userupdate,name="userupdate"),
    url('categoryupdate/<int:id>',views.categoryupdate,name="categoryupdate"),
    url('role/<int:id>/update',views.roleupdate,name="roleupdate"),
    url('dealupdate/<int:id>',views.dealupdate,name="dealupdate"),
    url('userdelete/<int:id>',views.userdelete,name="userdelete"),
    url('delete/<int:id>',views.delete,name="delete"),
    url('catgeories/<int:id>/delete',views.categorydelete,name="categorydelete"),
    url('roledelete/<int:id>',views.roledelete,name="roledelete"),
    url('deal/<int:id>/delete',views.dealdelete,name="dealdelete"),
    url('getbooks', views.get_books),
    url('rewardsapi',views.rewardsapi,name="rewardsapi"),
    url('rewardcreation',views.rewardcreation,name="rewardcreation"),
    url('dealapi',views.dealapi,name="dealapi"),
    url('loginApi',views.loginApi.as_view()),
     url('trans', views.trans,name='trans'),
     url('show_users',views.show_users,name="show_users"),
     url('normalcategories',views.normalcategories,name="normalcategories"),
     url('normaltransactions',views.normaltransactions,name="normaltransactions"),
     url('normalpayment',views.normalpayment,name="normalpayment"),
      url('favourites',views.favourites,name="favourites"),
    url('businesslist',views.businesslist,name="businesslist"),
    url('businessupdate/<int:id>',views.businessupdate,name="businessupdate"),
    url('addsales', views.addsales,name='addsales'),
    url('normaluser', views.normaluser,name='normaluser'),
    url('transactions', views.transactions, name="transactions"),
    url('role', views.role, name="role"),
    url('adduser',views.adduser.as_view()),
    url('createdeal', views.createdeal, name="createdeal"),
    url('wallets', views.wallets, name="wallets"),
    url('mybusiness', views.mybusiness, name="mybusiness"),
    url('business_favourite/<int:id>', views.business_favourite, name="business_favourite"),
    url('business_list', views.business_list, name="business_list"),
    url('register_user', views.register_user, name="register_user"),
    url('paysection', views.paysection.as_view()),
    url('business/<int:id>/payment', views.payment, name="payment"),
    url('walletsection', views.walletsection, name="walletsection"),
    url('paymentss', views.paymentss, name="paymentss"),
    url('show_business', views.show_business, name="show_business"),
    url('business/<int:id>/business_pay', views.business_pay, name="business_pay"),
    url('setting', views.setting, name="setting"),
    url('notification', views.notification, name="notification"),
    url("logout", views.logout, name="logout"),
    url('home', views.Home, name="home"),
    url('transact',views.transact,name="transact"),
    # url('business_lists', views.business_lists.as_view()),
    url('pay', views.pay, name="pay"),
    url('list', views.tablelist, name="list"),
    url('business', views.business, name="business"),
    url('category', views.Category, name="category"),
     url('categoryapi', views.Categoryapi, name="Categoryapi"),
    url('show_category', views.show_category, name="show_category"),
    url('categories', views.categories, name="categories"),
    url('shuffle', views.shuffle, name="shuffle"),
    url('search_map', views.search_map, name="search_map"),

    url('BusinessAdd', views.BusinessAddApi.as_view()),
    


    # pyament checkout urls
    url('checkout-session', views.create_checkout_session, name="api"),
    url('payment-success', views.payment_success),
    url('payment-success', views.payment_cancel),
    url('payment-webhook', views.payment_webhook),
   
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<url>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
else:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
