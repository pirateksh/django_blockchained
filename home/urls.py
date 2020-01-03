from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('mine_block/', views.mine_block, name='mine_block'),
    path('get_chain/', views.get_chain, name='get_chain'),
    path('is_valid/', views.is_valid, name='is_valid'),
    path('add_employment_transaction/', views.add_employment_transaction,
         name='add_employment_transaction'),
    path('add_criminal_transaction/', views.add_criminal_transaction,
         name='add_criminal_transaction'),
    path('add_health_transaction/', views.add_health_transaction,
         name='add_health_transaction'),
    path('connect_node/', views.connect_node, name='connect_node'),
    path('replace_chain/', views.replace_chain, name='replace_chain'),
    path('get_transactions/', views.get_transactions, name='get_transactions'),
    path('empty_transactions/', views.empty_transactions,
         name='empty_transactions'),
    path('all_transaction/', views.all_transactions, name='all_transactions'),
    path('fetch_record/<str:record_type>/<str:public_key>/', views.fetch_record, name='fetch_record'),
]
