from django.db import models


# Party Type Model
class Ref_Party_Type(models.Model):
    Party_Type_Code = models.CharField(primary_key=True,max_length = 5)
    Description = models.CharField(max_length = 200, null=True)
    Is_Enabled = models.CharField(max_length = 1, null=True)
    Created_on = models.DateTimeField( null=True)
    Created_by = models.CharField( max_length = 100 ,null=True)
    Updated_on = models.DateTimeField( null=True)
    Updated_by = models.CharField(max_length = 100, null=True)
    
# Chart Of Account Model
class Chart_of_account(models.Model):
    Account_No = models.CharField(primary_key=True,max_length = 5)
    Main_Code = models.CharField(max_length = 5, null=True)
    Sub_Code = models.CharField(max_length = 5, null=True)
    Dept_Code = models.CharField(max_length = 5, null=True)
    Account_Description = models.CharField(max_length=100, null=True)
    Account_Type = models.CharField(max_length=100, null=True)
    Created_on = models.DateTimeField( null=True)
    Created_by = models.CharField( max_length = 100 ,null=True)
    Updated_on = models.DateTimeField( null=True)
    Updated_by = models.CharField(max_length = 100, null=True)
    
# Party Profile Model
class Ref_Party_Profile(models.Model):
    Party_Code = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length = 200, null=True)
    Address = models.CharField(max_length = 500, null=True)
    NTN_No = models.CharField(max_length = 50, null=True)
    Phone_No = models.CharField(max_length = 50, null=True)
    Description = models.CharField(max_length = 500, null=True)
    Payment_Terms = models.CharField(max_length = 500, null=True)
    Party_Type_Code = models.ForeignKey(
        'Ref_Party_Type', related_name='Type_Code' ,null=True,
        on_delete=models.CASCADE,
    )
    Account_No = models.ForeignKey(
        'Chart_of_account', related_name='Acc_No' ,null=True,
        on_delete=models.CASCADE,
    )
    Created_on = models.DateTimeField( null=True)
    Created_by = models.CharField( max_length = 100 ,null=True)
    Updated_on = models.DateTimeField( null=True)
    Updated_by = models.CharField(max_length = 100, null=True)
    
# Voucher Type
class Ref_Voucher_Type(models.Model):
    Voucher_Type_Code = models.BigAutoField(primary_key=True)
    Description = models.CharField(max_length=200, null=True)
    Is_Enabled = models.CharField(max_length=1,null=True)
    Created_on = models.DateTimeField( null=True)
    Created_by = models.CharField( max_length = 100 ,null=True)
    Updated_on = models.DateTimeField( null=True)
    Updated_by = models.CharField(max_length = 100, null=True)
    
# Voucher Main
class Voucher_Main(models.Model):
    Trans_id = models.BigAutoField(primary_key=True)
    Voucher_No = models.CharField(max_length=100, null=True)
    
    Voucher_Type_Code = models.ForeignKey(
        'Ref_Voucher_Type', related_name='V_Type_Code' ,null=True,
        on_delete=models.CASCADE,
    )
    Created_on = models.DateTimeField( null=True)
    Created_by = models.CharField( max_length = 100 ,null=True)
    
# Voucher Detail
class Voucher_Detail(models.Model):
    Trans_id = models.ForeignKey(
        'Voucher_Main', related_name='Transection_id' ,null=True,
        on_delete=models.CASCADE,
    )
    Account_No = models.ForeignKey(
        'Chart_of_account', related_name='Ac_No' ,null=True,max_length=10,
        on_delete=models.CASCADE,
    )
    Debit = models.DecimalField(max_digits=13, decimal_places=3,null=True)
    Credit = models.DecimalField(max_digits=13, decimal_places=3,null=True)
    Description = models.CharField( max_length = 300 ,null=True)
    
    
# Create your models here.
class Company(models.Model):
    Company_Code = models.CharField(primary_key=True, max_length=18)
    Company_Name = models.CharField(null=True, max_length=30)
    Description = models.TextField(null=True, max_length=255)
    Address = models.TextField(null=True, max_length=50)
    Logo = models.CharField(null=True, max_length=18)
    Created_on = models.DateTimeField( null=True)
    Created_by = models.CharField( max_length = 100 ,null=True)
    Updated_on = models.DateTimeField( null=True)
    Updated_by = models.CharField(max_length = 100, null=True)
