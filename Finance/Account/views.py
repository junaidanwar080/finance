from django.shortcuts import render , redirect
from django.http import HttpResponse ,JsonResponse
from .models import Ref_Party_Type,Chart_of_account,Voucher_Main,Voucher_Detail,Ref_Party_Profile,Ref_Voucher_Type,Company
# from UserManagement.models import Company
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from datetime import datetime
x=datetime.now()
y=x.strftime('%Y-%m-%d')
from django.forms.models import model_to_dict
from django.core.mail import send_mail


# Main Page
def main(request): 
    if request.session.has_key('id'):
       
        username = request.session['username']
        return render(request,'main_page.html',{'username':username})
    else:
        return redirect('login_form')
#------------------------------------------------------------------------
# Chart Of Accounts
#------------------------------------------------------------------------
#chart of Accounts page call
def chart_of_accounts(request):
    if request.session.has_key('id'):
        username = request.session['username']
        return render(request,'Accounts/chart_of_accounts/chart_of_accounts.html',{'username':username})
    else:
        return redirect('login_form')

#Chart of Account Insert
def chart_of_account_insert(request):
    if request.method == 'POST':
        ac_no = request.POST['ac_no']
        ac_name = request.POST['ac_name']
        # main_code = request.POST['main_code']
        if ac_no=='' or ac_name=='' :
            return JsonResponse('Plese Fill Required Fields',safe=False)
        else:
            insert_account = Chart_of_account(Account_No = ac_no , Account_Description = ac_name , Created_on = y)
            insert_account.save()
            return JsonResponse("Account Created",safe=False)
        
def select_chart_of_account(request):
    accounts_select = Chart_of_account.objects.all()
    return render(request,'Accounts/chart_of_accounts/chart_of_accounts_select.html' , {'accounts_select':accounts_select})

#account_load_for_update
def account_load_for_update(request , account_code):
    data = Chart_of_account.objects.get(Account_No = account_code)
    return JsonResponse(model_to_dict(data))

#chart_of_account_update
def chart_of_account_update(request):
    if request.method == 'POST':
        update_ac_no = request.POST['update_ac_no']
        update_ac_name = request.POST['update_ac_name']
        if update_ac_no == '' or update_ac_name== '':
            return JsonResponse('Please Enter Required fields' , safe = False)
        else:
            update = Chart_of_account.objects.get(Account_No = update_ac_no)
            update.Account_Description = update_ac_name
            update.Updated_on = y
            update.save()
            return JsonResponse('Account Updated',safe=False)
        
    
#------------------------------------------------------------------------
#Vouchers
#------------------------------------------------------------------------
#Vouchers 
def all_journal_vouchers(request):
    if request.session.has_key('id'):
        username = request.session['username']
        select_all = Voucher_Main.objects.all()
        return render(request,'Accounts/Vouchers/journal_vouchers.html',{'select_all':select_all , 'username':username})
    else:
        return redirect('login_form')

#Voucher Detail
def voucher_detail(request ,  Trans_id):
    voucher_main = Voucher_Main.objects.get(Trans_id=Trans_id)
    voucher_details = Voucher_Detail.objects.filter(Trans_id = Trans_id)
    
    return render(request,'Accounts/Vouchers/voucher_detail.html',{'voucher_main':voucher_main , 'voucher_details':voucher_details })

# Vouchers Input Form
def journal_voucher(request):
    if request.session.has_key('id'):
        username = request.session['username']
    all_voucher_types = Ref_Voucher_Type.objects.all()
    return render(request,'Accounts/Vouchers/journal_voucher.html' ,{'date':y , 'all_voucher_types':all_voucher_types , 'username':username})

#voucher insert
def voucher_insert(request):
    if request.method == 'POST':
        voucher_no = request.POST['voucher_id']
        voucher_type = request.POST['voucher_type']
        created_on = request.POST['transection_date']
        all_account_codes = request.POST['all_account_codes']
        all_account_codes_list = [x.strip() for x in all_account_codes.split(',')]
        all_debit_accounts = request.POST['all_debit_accounts']
        all_debit_accounts_list = [x.strip() for x in all_debit_accounts.split(',')]
        all_credit_accounts = request.POST['all_credit_accounts']
        all_credit_accounts_list = [x.strip() for x in all_credit_accounts.split(',')]
        all_descriptions = request.POST['all_descriptions']
        all_descriptions_list = [x.strip() for x in all_descriptions.split(',')]
        credit_sum = 0
        debit_sum = 0
        if voucher_no=='' or voucher_type == '':
            return JsonResponse('Please Fill all Required Fields',safe=False)
        else:
            for x in range(len(all_account_codes_list)):
                if all_account_codes_list[x] == '' or all_debit_accounts_list[x]=='' or all_credit_accounts_list[x]=='':
                    return JsonResponse('Please Fill all Required Fields',safe=False)
                else:
                    credit_sum = credit_sum + float(all_credit_accounts_list[x])
                    debit_sum = debit_sum + float(all_debit_accounts_list[x])
            if debit_sum != credit_sum:
                return JsonResponse('Debit And Credit account should be same',safe=False)
            else:
                insert_main = Voucher_Main(Voucher_No = voucher_no , Voucher_Type_Code = voucher_type , Created_on = created_on )
                insert_main.save()
                trans_id = Voucher_Main.objects.latest('Trans_id')
                for x in range(len(all_account_codes_list)):
                    insert_detail = Voucher_Detail(Account_No_id = all_account_codes_list[x] , Debit = float(all_debit_accounts_list[x]) , Credit = float(all_credit_accounts_list[x]) , Description = all_descriptions_list[x] , Trans_id = trans_id)
                    insert_detail.save()
            return JsonResponse('data inserted successfully',safe=False)
    else:
        return JsonResponse('you have an issue',safe=False)
        

#------------------------------------------------------------------------
#Voucher Type
#------------------------------------------------------------------------
def voucher_types(request):
    if request.session.has_key('id'):
        username = request.session['username']
        return render(request,'Accounts/VoucherType/voucher_types.html',{'username':username})
    else:
        return redirect('login_form')


# select_all_voucher_types
def select_all_voucher_types(request):
    select = Ref_Voucher_Type.objects.all()
    return render(request, 'Accounts/VoucherType/voucher_types_select.html',{'select':select})

def voucher_type_insert(request):
    if request.method == 'POST':
        voucher_type_name = request.POST['voucher_type_name']
        if(voucher_type_name == ''):
            return JsonResponse('Please enter Required Data', safe=False)
        else:
            insert_voucher_type = Ref_Voucher_Type(Description = voucher_type_name , Created_on = y )
            insert_voucher_type.save()
            if (insert_voucher_type):
                return JsonResponse('Voucher Type Created',safe=False)
            else:
                return JsonResponse('Voucher Type not Created',safe=False)
            
# voucher_type_load_for_update
def voucher_type_load_for_update(request , code):
    load_for_update = Ref_Voucher_Type.objects.get(Voucher_Type_Code=code)
    return JsonResponse(model_to_dict(load_for_update))

# voucher_type_update
def voucher_type_update(request):
    if request.method == 'POST':
        update_voucher_type_id = request.POST['update_voucher_type_id']
        update_voucher_type_name = request.POST['update_voucher_type_name']
        if update_voucher_type_name == '':
            return JsonResponse('Please Fill Required Fields',safe=False)
        else:
            edit = Ref_Voucher_Type.objects.get(Voucher_Type_Code = update_voucher_type_id)
            edit.Description = update_voucher_type_name
            edit.Updated_on = y
            edit.save()
            return JsonResponse('Voucher Type Updated',safe=False)

#------------------------------------------------------------------------
#Party Type
#-----------------------------------------------------------------------
def party_type(request):
    if request.session.has_key('id'):
        username = request.session['username']
        return render(request,'Accounts/PartyType/party_type.html',{'username':username})
    else:
        return redirect('login_form')

#insert_party_type
def insert_party_type(request):
    if request.method == "POST":
        party_type_code=request.POST['party_type_code']
        description=request.POST['description']
        is_enable="1"
        if (party_type_code=='' or description==''):
            return JsonResponse("Please Fill Required Fields",safe=False)  
        else:
            insert_type=Ref_Party_Type(Party_Type_Code = party_type_code , Description = description , Is_Enabled=is_enable , Created_on=y)
            insert_type.save()
            return JsonResponse('data inserted',safe=False)
        
#select_party_type       
def select_party_type(request):
    type_select = Ref_Party_Type.objects.all()
    return render(request, 'Accounts/PartyType/party_type_select.html',{'type_select':type_select})

#delete_party_type
def delete_party_type(request , party_type_id):
    delete_party_type = Ref_Party_Type.objects.get(Party_Type_Code=party_type_id)
    msg=delete_party_type.delete()
    if(msg):
        return redirect( 'party_type')
    else:
        return JsonResponse('data not deleted',safe=False)

#Type Load For Update
def type_load_for_update(request , party_type):
    print(party_type)
    type = Ref_Party_Type.objects.get(Party_Type_Code = party_type)
    return JsonResponse(model_to_dict(type))

#type Update
def type_update(request):
    if request.method == 'POST':
        if (request.POST['update_description'] == ''):
            return JsonResponse('Please write name',safe=False)
        else:
            party_type_code = request.POST['update_party_type_code']
            description = request.POST['update_description']
            update_on = y
            type_data = Ref_Party_Type.objects.get(Party_Type_Code=party_type_code)
            type_data.Description= description
            type_data.Updated_on= update_on
            type_data.save()
            return JsonResponse('Type Record Updated',safe=False)
        
#---------------------------------------------------------------------------------------------------------
#party_Profile
#---------------------------------------------------------------------------------------------------------
def party_profile(request):
    if request.session.has_key('id'):
        username = request.session['username']
        return render(request,'Accounts/Party_Profile/party_profile.html',{'username':username})
    else:
        return redirect('login_form')

def select_party_profiles(request):
    select_all = Ref_Party_Profile.objects.all()
    return render(request,'Accounts/Party_Profile/Party_Profiles_Select.html',{'select_all':select_all})

#insert Party Profile
def insert_party_profile(request):
    if request.method == 'POST':
        party_name=request.POST['party_name']
        account=request.POST['account']
        ntn_number=request.POST['ntn_number']
        address=request.POST['address']
        phone_no=request.POST['phone_no']
        description=request.POST['description']
        party_type_code=request.POST['party_type_code']
        if (party_name=='' or ntn_number=='' or account == ''):
            return JsonResponse('Please Fill Required Fields',safe=False)
        else:
            party_profile_insert = Ref_Party_Profile(Name = party_name , Address = address , NTN_No = ntn_number , Phone_No = phone_no , 
                                                     Description = description , Account_No_id = account , Party_Type_Code_id = party_type_code, Created_on = y)
            party_profile_insert.save()
            return JsonResponse('data inserted',safe=False)
    else:
        return JsonResponse('You are sending Wrong Request',safe=False)
    
# party_profile_load_for_update
def party_profile_load_for_update(request , party_code):
    party_profile_load = Ref_Party_Profile.objects.get(Party_Code = party_code)
    # print(party_profile_load)
    # return render(request,'Accounts/Party_Profile/PartyProfileModals.html',{'party_profile_load':party_profile_load})
    return JsonResponse(model_to_dict(party_profile_load))

# update_party_profile
def update_party_profile(request):
    if request.method == 'POST':
        update_party_code = request.POST['update_party_code']
        update_party_name = request.POST['update_party_name']
        update_account = request.POST['update_account']
        update_ntn_number = request.POST['update_ntn_number']
        update_address = request.POST['update_address']
        update_phone_no = request.POST['update_phone_no']
        update_description = request.POST['update_description']
        data = Ref_Party_Profile.objects.get(Party_Code = update_party_code)
        data.Name = update_party_name
        data.Account_No_id = update_account 
        data.NTN_No = update_ntn_number
        data.Address = update_address
        data.Phone_No = update_phone_no
        data.Description = update_description
        data.Updated_on = y
        data.save()
        return JsonResponse('Party Record Updated',safe=False)




#--------------------------------------------------------------------------------------
# User
#---------------------------------------------------------------------------------
def user_page(request):
    if request.session.has_key('id'):
        username = request.session['username']
        return render(request,'Admin_Penal/User/users.html',{'username':username})
    else:
        return redirect('login_form')
        

# Insert User
def insert_user(request):
    if request.method == "POST":
        # User_id = request.POST['User_id']
        Name = request.POST['Name']
        Email = request.POST['Email']
        # Phone = request.POST['Phone']
        # Gender = request.POST['Gender']
        Login_Name = request.POST['Login_Name']
        Password = request.POST['Password']
        # Company_Cde_id = request.POST['Company_Cde_id']
        # print( Name, Email, Phone, Gender, Login_Name, Password, Company_Cde_id)
        super_admin = 1
        ins = User( first_name = Name, email = Email, username = Login_Name, password = Password, is_superuser= super_admin)
        ins.save()
        send_mail(
        'Test Mail',
        'It is testing email',
        'junaidanwar080@gmail.com',
        [Email],
)
        return JsonResponse('User Created',safe=False)

# Select User
def select_all_users(request):
    allusers = User.objects.all()
    return render(request,'Admin_Penal/User/select_all_users.html', {'User_table': allusers})

def user_profile_load_for_update(request , user_id):
    # print('came here')
    user_data = User.objects.get(id = user_id)
    return JsonResponse(model_to_dict(user_data))

def update_user_profile(request):
    if request.method == "POST":
        edit_user_id = request.POST['edit_user_id']
        edit_first_name = request.POST['edit_first_name']
        edit_last_name = request.POST['edit_last_name']
        edit_user_name = request.POST['edit_username']
        user_id = User.objects.get( id = edit_user_id)
        user_id.username = edit_user_name
        user_id.first_name = edit_first_name
        user_id.last_name = edit_last_name
        user_id.save()
        return JsonResponse("User Data Updated",safe=False)
    
#-------------------------------------------------------------------------------
#Log in , Logout
#-------------------------------------------------------------------------------
def login_form(request):
    return render(request, 'login.html')

#insert login
def insert_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate( username=username, password=password)
        if user  is not None:
            request.session['id']=user.id
            request.session['username']=user.username
            request.session['is_superuser']=user.is_superuser
            if user.is_superuser is True:
                return redirect('Admin_Dashboard')
            else:
                return redirect('main')
        else:
            return redirect('login_form')
    
        
        
# logout
def logout(request):
    request.session.flush()
    request.session.clear_expired()
    return render(request, 'login.html')
        
#---------------------------------------------------------------------------------
#Admin Dash Board
#---------------------------------------------------------------------------------
def Admin_Dashboard(request): 
    if request.session.has_key('id'):
        username = request.session['username']
        return render(request,'Admin_Penal/Admin_Dashboard.html',{'username':username})
    else:
        return redirect('login_form')

#---------------------------------------------------------------------------------
# company
#---------------------------------------------------------------------------------
def company_page(request):
    if request.session.has_key('id'):
        username = request.session['username']
        return render(request,'Admin_Penal/Company/create_company.html',{'username':username})
    else:
        return redirect('login_form')

# Company Insert
def company_insert(request):
    if request.method == "POST":
        Company_Code = request.POST['Company_Cde']
        Company_Name = request.POST['Company_Name']
        Description = request.POST['Description']
        Address = request.POST['Address']
        Logo = request.POST['Logo']
        if Company_Code=='' or Company_Name=='':
            return JsonResponse('Please Fill Required Fields',safe=False)
        else:
            create_company = Company(Company_Code=Company_Code, Company_Name=Company_Name, Description=Description, Address=Address, Logo=Logo)
            create_company.save()
            return JsonResponse('Company Created',safe=False)

# Company data load for update
def Company_Load_For_Update(request , company_code):
    load_companies = Company.objects.get(Company_Code=company_code)
    return JsonResponse(model_to_dict(load_companies))

# Update Company Data
def company_update( request):
    if request.method == "POST":
        Company_Code = request.POST['edit_Company_Cde']
        Company_Name = request.POST['edit_Company_Name']
        Description = request.POST['edit_Description']
        Address = request.POST['edit_Address']
        Logo = request.POST['edit_Logo']
        update = Company.objects.get(Company_Code=Company_Code)
        update.Company_Name = Company_Name
        update.save()
        return JsonResponse('Company Updated',safe=False)
    

# Company Select
def select_compnies(request):
    select_companies = Company.objects.all() 
    return render(request,'Admin_Penal/Company/select_all_companies.html',{'select_companies': select_companies})
#-------------------------------------------------------------------------------
#Others
#-------------------------------------------------------------------------------
def load_all_accounts(request):
    select_accounts = Chart_of_account.objects.all()
    return render(request,'Accounts/other/load_all_accounts.html',{'select_accounts':select_accounts})

def load_all_party_types(request):
    all_types = Ref_Party_Type.objects.all()
    return render(request,'Accounts/other/load_all_party_types.html',{'all_types':all_types})

