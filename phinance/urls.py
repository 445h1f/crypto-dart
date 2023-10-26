"""
URL configuration for phinance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from portfolio import views as portfolio_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view=user_views.connect, name='index'),
    path('login/', view=user_views.connect, name='connect'),
    # path('portfolio/', view=portfolio_views., name='portfolio'),
    path('trade/add', view=login_required(portfolio_views.add_trade), name='add_trade'),
    path('trade/close/<str:trade_id>', view=login_required(portfolio_views.close_trade), name='close_trade'),
    # path('web3_auth/', include('web3_auth.urls')),
    # path('web3_auth/moralis_auth', view=web3_views.moralis_auth, name='moralis_auth'),
    path('request_message', view=user_views.request_message, name='request_message'),
    # path('login/my_profile', view=portfolio_views.my_profile, name='my_profile'),
    path('verify_message', view=user_views.verify_message, name='verify_message'),
    path('auth/', include('django.contrib.auth.urls')),
    path('dashboard/', view=login_required(portfolio_views.dashboard), name='dashboard'),
    path('trade/all', view=login_required(portfolio_views.view_all_trades), name="view_all_trades"),
    path('news', view=login_required(portfolio_views.view_news), name="news"),
]
