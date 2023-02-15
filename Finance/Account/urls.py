from django.urls import path
from . import views


urlpatterns = [
# Main page URLs
    path('',views.main,name='main'),
    
#Chart of Accounts
    path('chart_of_accounts',views.chart_of_accounts,name='chart_of_accounts'),
    path('chart_of_account_insert',views.chart_of_account_insert),
    path('select_chart_of_account',views.select_chart_of_account),
    path('account_load_for_update/<int:account_code>',views.account_load_for_update),
    path('chart_of_account_update',views.chart_of_account_update),
    
#Vouchers
    path('journal_voucher',views.journal_voucher,name='journal_voucher'),
    path('all_journal_vouchera',views.all_journal_vouchers,name='all_journal_vouchers'),
    path('voucher_insert',views.voucher_insert),
    path('voucher_detail/<int:Trans_id>',views.voucher_detail),
    
#Voucher Type
    path('voucher_types',views.voucher_types, name='voucher_types'),
    path('voucher_type_insert',views.voucher_type_insert),
    path('select_all_voucher_types',views.select_all_voucher_types),
    path('voucher_type_load_for_update/<int:code>',views.voucher_type_load_for_update),
    path('voucher_type_update',views.voucher_type_update),
     
#Party Type
    path('party_type',views.party_type,name='party_type'),
    path('insert_party_type',views.insert_party_type),
    path('type_select',views.select_party_type),
    path('delete_party_type/<str:party_type_id>',views.delete_party_type),
    path('type_load_for_update/<str:party_type>',views.type_load_for_update , name ='type_load_for_update'),
    path('type_update',views.type_update),
    
#Party Profile
    path('party_profile',views.party_profile,name='party_profile'),
    path('insert_party_profile',views.insert_party_profile),
    path('select_party_profiles',views.select_party_profiles),
    path('party_profile_load_for_update/<int:party_code>',views.party_profile_load_for_update),
    path('update_party_profile',views.update_party_profile),
     
    
# Admin Dashboard
    path('Admin_Dashboard',views.Admin_Dashboard,name='Admin_Dashboard'),
    
# Company
    path('company_page',views.company_page,name = 'company_page'),
    path('company_insert', views.company_insert),
    path('select_compnies', views.select_compnies ),
    path('company_load_for_update/<str:company_code>',views.Company_Load_For_Update),
    path('company_update',views.company_update),
    
#Users
    path('user_page', views.user_page, name='user_page' ),
    path('insert_user', views.insert_user),
    path('select_all_users', views.select_all_users), 
    path('user_profile_load_for_update/<int:user_id>',views.user_profile_load_for_update),
    path('update_user_profile',views.update_user_profile),
    
# Login  
    path('login_form',views.login_form,name='login_form'),
    path('insert_login',views.insert_login,name = 'insert_login'),

# Logout
path('logout', views.logout , name='logout'),

# Others
    path('load_all_accounts',views.load_all_accounts),
    path('load_all_party_types',views.load_all_party_types),
]