from django.db import models

# Create your models here.
from django.db import models
import uuid
from django.utils import timezone
# Create your models here.
class Admin(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        default="False"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AdminPasswordReset(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(unique=True,max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Material(models.Model):
    title=models.CharField(max_length=255)
    status=models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Colour(models.Model):
    colour_name = models.CharField(unique=True,max_length=50,null=True,blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.colour_name


class Product(models.Model):
    product_name = models.CharField(max_length=300)
    product_codes = models.CharField(max_length=200)
    sku = models.CharField(max_length=300)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)

    film_type = models.CharField(max_length=200)  # PPF / Sun Control
    material_id = models.ForeignKey(Material ,on_delete=models.CASCADE, default=None)   # TPU / TPH
    finish = models.CharField(max_length=100)     # Gloss / Matte
    colour_id = models.ForeignKey(Colour,on_delete=models.CASCADE, default=None)     # Transparent / Black / Custom
    application_area = models.CharField(max_length=200)  # Exterior / Interior / Glass
    thickness = models.CharField(max_length=100)
    specification = models.TextField()
    warranty = models.CharField(max_length=300)

    adhesive = models.CharField(max_length=100, blank=True, null=True)
    anti_yellowing = models.CharField(max_length=100, blank=True, null=True)
    scratch_resistant = models.CharField(max_length=100, blank=True, null=True)
    uv_resistance = models.CharField(max_length=100, blank=True, null=True)
    hydrophobic = models.CharField(max_length=100, blank=True, null=True)
    stain_resistant = models.CharField(max_length=100, blank=True, null=True)
    elongation = models.CharField(max_length=100, blank=True, null=True)
    tear_strength = models.CharField(max_length=100, blank=True, null=True)

    mrp = models.DecimalField(max_digits=10, decimal_places=2)

    thumbnail_image = models.ImageField(upload_to='thumbnails/')
    image1 = models.ImageField(upload_to= "Gallery/" ,blank=True, null=True)
    image2 = models.ImageField(upload_to= "Gallery/" ,blank=True, null=True)
    image3 = models.ImageField(upload_to= "Gallery/" ,blank=True, null=True)
    image4 = models.ImageField(upload_to= "Gallery/" ,blank=True, null=True)
    installation_video_url = models.TextField(blank=True, null=True)

    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tempeerature_resistance=models.CharField(max_length=100, blank=True, null=True)
    peel_adhesion=models.CharField(max_length=100, blank=True, null=True)
    anti_rockclip = models.CharField(max_length=100, blank=True, null=True)
    elongation_rate_tpu=models.CharField(max_length=100, blank=True, null=True)
    elongation_rate_hard=models.CharField(max_length=100, blank=True, null=True)
    mou=models.CharField(max_length=200, blank=True, null=True)
    hsn_code=models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    GST=models.CharField(unique=False,blank=True,null=True,max_length=200)
    product_sequence=models.IntegerField(blank=True,null=True)


    def __str__(self):
        return self.product_name



class Banner(models.Model):
    title=models.CharField(max_length=255,blank=True,null=True)
    image=models.ImageField(upload_to='banner/',blank=True,null=True)
    CTA_text=models.CharField(max_length=255,blank=True,null=True)
    CTA_link=models.CharField(max_length=255,blank=True,null=True)
    order=models.IntegerField(blank=True,null=True)
    status=models.BooleanField(default=True)


    def __str__(self):
        return self.title

class Import_shipment(models.Model):

    supplier_name=models.CharField(max_length=100)
    supplier_invoice_no=models.CharField(max_length=200)
    invoice_currency = models.CharField(max_length=10)
    invoice_value_foreign=models.DecimalField(max_digits=10, decimal_places=2)
    exchange_rate=models.DecimalField(max_digits=10, decimal_places=2)
    invoice_value_inr=models.DecimalField(max_digits=10, decimal_places=2)
    bl_awb_no=models.CharField(max_length=200)
    arrival_date = models.DateTimeField()

    def __str__(self):
        return self.supplier_name

class Import_cost(models.Model):

    shipment_id=models.ForeignKey(Import_shipment,on_delete=models.CASCADE)
    cost_type_freight=models.CharField(max_length=200)
    cost_type_insurance=models.CharField(max_length=100)
    cost_type_duty=models.CharField(max_length=200)
    cost_type_igst=models.CharField(max_length=200)
    cost_type_port=models.CharField(max_length=100)
    cost_type_cha=models.CharField(max_length=100)
    cost_type_trasnport=models.CharField(max_length=100)
    cost_type_others=models.CharField(max_length=100)
    cost_amount_inr=models.DecimalField(max_digits=15, decimal_places=2)

    capitalized=models.BooleanField(default=False)
    reference_doc=models.CharField(max_length=200)

    def __str__(self):
        return self.cost_type_freight


class WareHouse(models.Model):
    STATUS_CHOICE =(
        ('active','Active'),
        ('deactive','Deactive'),
    )
    name=models.CharField(max_length=100)
    address=models.TextField()
    code=models.CharField(max_length=20,unique=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICE,default='active')

    def __str__(self):
        return self.name


class Location(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('deactive', 'Deactive'),
    )
    warehouse_id=models.ForeignKey(WareHouse,on_delete=models.CASCADE,related_name="locations",blank=True,null=True)
    name=models.CharField(max_length=100)
    address=models.TextField()
    code = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name


class Shipment_product(models.Model):
    shipment_id=models.ForeignKey(Import_shipment,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)

    batch_data=models.TextField()
    quantity=models.IntegerField()
    allocation_basis=models.CharField(max_length=500)
    landed_cost_allocated=models.DecimalField(max_digits=10, decimal_places=2)
    per_unit_cost_inr=models.DecimalField(max_digits=15, decimal_places=2)
    per_unit_cost_usd=models.DecimalField(max_digits=15, decimal_places=2)
    warehouse_id=models.ForeignKey(WareHouse,on_delete=models.CASCADE,related_name="shipment_products",null=True,blank=True)

    location_id=models.ForeignKey(Location,on_delete=models.CASCADE,related_name="shimpments_products",null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.batch_data


class Department(models.Model):

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Inactive'
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Roles(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Office_branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,blank=True,null=True,default='Inactive')

    def __str__(self):
        return self.name



class Employee(models.Model):

    EMPLOYMENT_TYPE_CHOICES = (
        ('Permanent', 'Permanent'),
        ('Contract', 'Contract'),
        ('Intern', 'Intern'),
    )

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Resigned', 'Resigned'),
    )

    employee_code = models.CharField(max_length=50, unique=True,default=None)
    first_name = models.CharField(max_length=100,  default=None)
    last_name = models.CharField(max_length=100, default=None)
    gender = models.CharField(max_length=10, default=None)
    date_of_birth = models.DateField(default=None)
    email = models.EmailField(unique=False)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    department_id = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='employees',default=None
    )

    role_id = models.ForeignKey(
        Roles,
        on_delete=models.PROTECT,
        related_name='employees',default=None
    )

    # location_id = models.ForeignKey(
    #     Office_branch,
    #     on_delete=models.PROTECT,
    #     related_name='employees'
    # )

    joining_date = models.DateField(default=None)

    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,default=None
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    office_branch_id = models.ForeignKey(Office_branch, on_delete=models.PROTECT, null=True, blank=True)


    def __str__(self):
        return f"{self.employee_code} - {self.first_name} {self.last_name}"
    

class Lead(models.Model):

    LEAD_TYPE_CHOICES = [
        ('Distributor', 'Distributor'),
        ('Retailer', 'Retailer'),
        ('Direct', 'Direct'),]

    INTEREST_LEVEL_CHOICES = [
        ('Warm', 'Warm'),
        ('Hot', 'Hot'),
        ('Cold', 'Cold'),
    ]

    LEAD_STATUS_CHOICES = [
        ('Lead', 'Lead'),
        ('Prospect', 'Prospect'),
        ('Converted', 'Converted'),
        ('Lost', 'Lost'),
        ('Follow_up','Follow_up'),
    ]

    LEAD_SOURCE_CHOICES = [
        ('WEBSITE', 'Website'),
        ('WHATSAPP', 'Whatsapp'),
        ('CALL', 'Call'),
        ('EMAIL', 'Email'),
        ('EXHIBITION', 'Exhibition'),
        ('REFERRAL', 'Referral'),
        ('SALES', 'Sales'),
    ]

    lead_type = models.CharField(max_length=20, choices=LEAD_TYPE_CHOICES)
    business_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    
    phone = models.CharField(max_length=20, unique=True)
    
    email = models.EmailField(unique=True)
    
    address = models.TextField()
    
    city = models.CharField(max_length=100)
    
    state = models.CharField(max_length=100)
    
    interest_level = models.CharField(max_length=10, choices=INTEREST_LEVEL_CHOICES)
    
    lead_status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='Lead')
    
    remarks = models.TextField(blank=True, null=True)
    
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    location = models.CharField(max_length=255, blank=True, null=True)
    
    week = models.CharField(max_length=20,blank=True,null=True)

    month = models.CharField(max_length=20,blank=True,null=True)

    date = models.DateField(blank=True,null=True)

    outlet_age = models.CharField(max_length=50,blank=True,null=True)

    ppf_installers = models.BooleanField(default=False)

    brand_dealing = models.CharField(max_length=200)

    past_distributor_name = models.CharField(max_length=200)

    dealer_landing_cost = models.DecimalField(max_digits=10, decimal_places=2)

    cars_per_month = models.IntegerField()

    price_feedback = models.TextField()

    quality_feedback = models.TextField()

    demo = models.BooleanField(default=False)


    # ✅ Fixed field name + ENUM
    lead_source = models.CharField(
        max_length=20,
        choices=LEAD_SOURCE_CHOICES,
        blank=True,
        null=True
    )

    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )
    assigned_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.business_name

class Expense(models.Model):
    vendor_name = models.CharField(max_length=255)
    expense_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    receipt_photo = models.FileField(upload_to='expense_receipts/', blank=True, null=True)
    employee_id= models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='expense'
    )
    lead_id = models.ForeignKey(
        'Lead',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='expense'
    )
    def __str__(self):
        return f"{self.expense_type} - {self.amount}"


class Blog(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to='blog')
    content=models.TextField()
    shortcontent=models.TextField()
    date=models.DateField()
    month=models.CharField(max_length=100)
    tag=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

class Visit(models.Model):

    FOLLOWUP_CHOICES = (
        ('CALL', 'CALL'),
        ('WHATSAPP', 'WHATSAPP'),
        ('EMAIL', 'EMAIL'),
        ('MEETING', 'MEETING'),
    )

    # ---- STATUS ----
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FOLLOW_UP', 'Follow Up'),  # added here
    )

    employee_id = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='visits'
    )

    lead_id = models.ForeignKey(
        'Lead',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='visits'
    )

    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)

    visit_purpose = models.CharField(max_length=255)

    visit_date = models.DateTimeField()
    check_in_time = models.DateTimeField(blank=True, null=True)
    checkout_time = models.DateTimeField( blank=True, null=True)

    total_hr = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    followup_date = models.DateTimeField(blank=True, null=True)
    followup_type = models.CharField(
        max_length=20,
        choices=FOLLOWUP_CHOICES,
        blank=True,
        null=True
    )
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField()
    order_information = models.TextField(blank=True, null=True)
    payment_details = models.TextField(blank=True, null=True)
    payment_image = models.ImageField(
        upload_to='payment_images/',
        blank=True,
        null=True
    )

    images = models.ImageField(
        upload_to='visit_images/',
        blank=True,
        null=True
    )

    order_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING",blank=True,null=True
    )

    def __str__(self):
        return f"Visit to {self.address} on {self.visit_date}"

# class Distributor(models.Model):

#     DISTRIBUTOR_TYPE_CHOICES = [
#         ('Individual', 'Individual'),
#         ('Proprietorship', 'Proprietorship'),
#         ('Partnership', 'Partnership'),
#         ('Pvt Ltd', 'Pvt Ltd'),
#         ('LLP', 'LLP'),
#     ]

#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Approved', 'Approved'),
#         ('Rejected', 'Rejected'),
#         ('Suspended', 'Suspended'),
#     ]


#     distributor_type = models.CharField( max_length=20, choices=DISTRIBUTOR_TYPE_CHOICES)

#     distributor_name = models.CharField(max_length=150)

#     brand_name = models.CharField( max_length=150,blank=True,null=True)

#     date_of_registration = models.DateField()

#     status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='Pending')

#     sales_region = models.CharField(  max_length=100)

#     authorized_products = models.TextField()

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.distributor_name

from django.db import models

class BusinessLegalInfo(models.Model):
    BUSINESS_TYPE_CHOICES = [
        ('MANUFACTURER', 'Manufacturer'),
        ('DISTRIBUTOR', 'Distributor'),
        ('WHOLESALER', 'Wholesaler'),]
    business_type = models.CharField(
        max_length=20,choices=BUSINESS_TYPE_CHOICES)
    years_in_business = models.PositiveIntegerField()
    gst_number = models.CharField(max_length=15,unique=True)
    gst_certificate = models.FileField(upload_to='documents/gst/')
    pan_number = models.CharField(max_length=10,unique=True)
    pan_card_copy = models.FileField(upload_to='documents/pan/')
    created_at = models.DateTimeField(auto_now_add=True)


    # Required only for Pvt Ltd / LLP
    cin_llpin = models.CharField(max_length=21,null=True,blank=True)

    incorporation_certificate = models.FileField(upload_to='documents/incorporation/',
                                                 null=True,blank=True)

    def __str__(self):
        return f"{self.business_type} - {self.pan_number}"

class Region(models.Model):

    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,

        default='disable',blank=True,null=True
    )

    def __str__(self):
        return self.name

class DistributorInformation(models.Model):

    DISTRIBUTOR_TYPE_CHOICES = [
        ('Individual', 'Individual'),
        ('Proprietorship', 'Proprietorship'),
        ('Partnership', 'Partnership'),
        ('Pvt Ltd', 'Pvt Ltd'),
        ('LLP', 'LLP'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Suspended', 'Suspended'),
    ]


    distributor_type = models.CharField( max_length=20, choices=DISTRIBUTOR_TYPE_CHOICES,
    blank=True,null=True,default="Pvt Ltd")

    distributor_name = models.CharField(max_length=150)

    brand_name = models.CharField( max_length=150,blank=True,null=True)

    date_of_registration = models.DateField()

    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='Pending')

    sales_region = models.CharField(max_length=100,blank=True,null=True)

    region = models.ForeignKey(Region ,on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='sales_region')

    authorized_products = models.TextField(blank=True,null=True)

    contact_person_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=50,blank=True,null=True)
    mobile_number = models.CharField(max_length=15)
    alternate_mobile = models.CharField(max_length=15, blank=True, null=True)
    email_id = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    address_line_1 = models.CharField(max_length=200,blank=True,null=True)
    address_line_2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    pincode = models.CharField(max_length=10,blank=True,null=True)
    country = models.CharField(max_length=50, default="India")

    BUSINESS_TYPE_CHOICES = [
        ('MANUFACTURER', 'Manufacturer'),
        ('DISTRIBUTOR', 'Distributor'),
        ('WHOLESALER', 'Wholesaler'),]
    business_type = models.CharField(
        max_length=20,choices=BUSINESS_TYPE_CHOICES,blank=True,null=True)
    years_in_business = models.PositiveIntegerField(blank=True,null=True)
    gst_number = models.CharField(max_length=15,unique=True,blank=True,null=True)
    gst_certificate = models.FileField(upload_to='documents/gst/',blank=True,null=True)
    pan_number = models.CharField(max_length=10,unique=True,blank=True,null=True)
    pan_card_copy = models.FileField(upload_to='documents/pan/',blank=True,null=True)



    # Required only for Pvt Ltd / LLP
    cin_llpin = models.CharField(max_length=21,null=True,blank=True)

    incorporation_certificate = models.FileField(upload_to='documents/incorporation/',
                                                 null=True,blank=True)

    ADDRESS_PROOF_CHOICES = [
        ('Aadhaar', 'Aadhaar'),
        ('Passport', 'Passport'),
        ('Voter ID', 'Voter ID'),
    ]

    owner_name = models.CharField(max_length=100,blank=True,null=True)
    owner_dob = models.DateField(blank=True,null=True)
    aadhaar_number = models.CharField(max_length=12, unique=True,blank=True,null=True)

    aadhaar_front = models.FileField(upload_to='kyc/aadhaar/',blank=True,null=True)
    aadhaar_back = models.FileField(upload_to='kyc/aadhaar/',blank=True,null=True)
    owner_photo = models.FileField(upload_to='kyc/photo/',blank=True,null=True)
    address_proof = models.CharField(max_length=20, choices=ADDRESS_PROOF_CHOICES, blank=True, null=True)
    address_proof_copy = models.FileField(upload_to='kyc/address/',blank=True, null=True)

    authorized_signatory_name = models.CharField(max_length=100,blank=True,null=True)
    signatory_pan = models.CharField(max_length=10,blank=True,null=True)

    signatory_pan_copy = models.FileField(upload_to="signatory/pan/",blank=True,null=True)
    board_resolution = models.FileField(upload_to="signatory/board_resolution/", blank=True, null=True)
    partnership_deed = models.FileField(upload_to="signatory/partnership_deed/", blank=True, null=True)
    llp_agreement = models.FileField(upload_to="signatory/llp_agreement/", blank=True, null=True)

    firm_type = models.CharField(
        max_length=20,
        choices=[
            ("company", "Company"),
            ("partnership", "Partnership"),
            ("llp", "LLP")],default="Company")

    bank_account_name=models.CharField(max_length=150,blank=True,null=True)
    bank_name=models.CharField(max_length=100,blank=True,null=True)
    account_number=models.CharField(max_length=20, unique=True,blank=True,null=True)
    ifsc_code=models.CharField(max_length=11,blank=True,null=True)
    branch_name=models.CharField(max_length=100,blank=True,null=True)
    cancelled_cheque=models.FileField(upload_to="cancelled_cheques/",blank=True,null=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    payment_terms_days = models.IntegerField(blank=True,null=True)

    warehouse_available = models.BooleanField(blank=True,null=True)
    warehouse_address = models.TextField(blank=True, null=True)

    storage_area_sqft = models.IntegerField(blank=True, null=True)
    logistics_partner = models.CharField(max_length=100, blank=True, null=True)

    monthly_distribution_capacity = models.IntegerField(blank=True,null=True)
    service_cities = models.TextField(blank=True,null=True)

    agreement_signed = models.BooleanField(default=True,blank=True,null=True)
    agreement_copy = models.FileField(upload_to="agreements/",blank=True,null=True)
    kyc_verified = models.BooleanField(blank=True,null=True)
    kyc_verified_by = models.CharField(max_length=100,blank=True,null=True)
    kyc_verified_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.distributor_name


class InventorySerial(models.Model):
    STATUS_CHOICES = (
    ('IN_STOCK', 'In Stock'),
    ('RESERVED', 'Reserved'),
    ('PICKED', 'Picked'),
    ('PACKED', 'Packed'),
    ('DELIVERED', 'Delivered'),
)

    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory_serials"  # ✅ CHANGED
    )
    batch_id = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="IN_STOCK")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,blank=True,null=True,related_name="inventory_serials")
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE,blank=True,null=True,related_name="inventory_serials")
    barcode_image = models.ImageField(upload_to="barcodes/", blank=True, null=True)
    def __str__(self):
        return self.serial_number

class InventorySerialHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory_serial_history")
    serial_number = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    batch_id = models.CharField(max_length=100, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    warehouse = models.ForeignKey(WareHouse, on_delete=models.SET_NULL, blank=True, null=True)

    snapshot_date = models.DateField()  # e.g., 2026-03-01
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.serial_number} - {self.status} ({self.snapshot_date})"

class Serial(models.Model):

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('RESERVED', 'Reserved'),
        ('SOLD', 'Sold'),
        ('INSTALLED', 'Installed'),]

    # Assuming Product and Batch models already exist
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='serials')

    batch = models.CharField(max_length=100,blank=True,null=True)

    serial_number = models.CharField(max_length=100,unique=True)

    shipping_model = models.CharField(max_length=100)
    status = models.CharField( max_length=20,choices=STATUS_CHOICES,default='AVAILABLE')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.serial_number
class Warranty(models.Model):
    WARRANTY_STATUS = (
        ('ACTIVE', 'ACTIVE'),
        ('EXPIRED', 'EXPIRED'),
        ('VOID', 'VOID'),
        ('PENDING', 'PENDING'),
        ('HOLD', 'HOLD'),
    )

    PRODUCT_STATUS = (
        ('PENDING', 'Pending Company Approval'),
        ('ACTIVATED', 'Warranty Activated'),
        ('REJECTED', 'Rejected'),
        ('INVALID', 'Invalid'),
    )


    serial_id = models.ForeignKey(
        InventorySerial, on_delete=models.CASCADE, related_name='warranties',blank=True,null=True
    )
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='warranties'
    )
    distributor_id = models.ForeignKey(
        DistributorInformation,
        on_delete=models.CASCADE,
        related_name='warranties',
        null=True,
        blank=True
    )

    detailer_name = models.CharField(max_length=100)
    detailer_mobile = models.CharField(max_length=15)

    car_registration_number = models.CharField(max_length=20)
    car_brand = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)

    installation_date = models.DateField(default=timezone.now)

    warranty_period = models.IntegerField(
        help_text="Warranty in months", blank=True, null=True
    )
    warranty_start_date = models.DateField(blank=True, null=True)
    warranty_end_date = models.DateField(blank=True, null=True)

    warranty_status = models.CharField(
        max_length=10, choices=WARRANTY_STATUS, default='PENDING'
    )
    product_status = models.CharField(
        max_length=20, choices=PRODUCT_STATUS, default='PENDING'
    )

    rejection_reason = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(
        Admin,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='approved_warranties'
    )

    # ✅ MULTIPLE IMAGES (NO EXTRA MODEL)
    car_images = models.JSONField(blank=True, null=True)
    installation_images = models.JSONField(blank=True, null=True)

    invoice_image = models.ImageField(
        upload_to='invoice_images/', blank=True, null=True
    )

    registered_by = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    generate_bill = models.BooleanField(default=False)
    license_plate_no = models.CharField(max_length=100,blank=True,null=True)
    color = models.CharField(max_length=100,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    owner_name = models.CharField(max_length=100,blank=True,null=True)
    owner_email=models.EmailField(unique=False,blank=True,null=True)
    owner_mobile=models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(unique=False,blank=True,null=True)
    signature_img=models.ImageField(upload_to="signature/",blank=True,null=True)
    hold_reason = models.TextField(blank=True,null=True)


    def __str__(self):
        return f"Warranty for {self.serial_id}"


class EmployeeSalary(models.Model):
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="salaries",blank=True,null=True)
    basic_salary=models.FloatField()
    alloances=models.FloatField()
    deductions=models.FloatField()
    gross_salary=models.FloatField()
    effective_from=models.DateField()
    status=models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        return f"Employee {self.employee_id} Salary"

class Employee_personal_details(models.Model):
    MARITAL_STATUS_CHOICES = (('single', 'Single'),
                              ('married', 'Married'),)

    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE,
                                  related_name='Employee',blank=True,null=True
                                 )
    father_name=models.CharField(max_length=100,blank=True,null=True)
    mother_name=models.CharField(max_length=100,blank=True,null=True)
    marital_status = models.CharField(
        max_length=10,
        choices=MARITAL_STATUS_CHOICES,
        default='single')
    spouse_name=models.CharField(max_length=100,blank=True,null=True)
    address=models.CharField(max_length=200,blank=True,null=True)
    emergency_contact_name=models.CharField(max_length=100,blank=True,null=True)
    emergency_contact_phone=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.father_name

class EmployeeDocuments(models.Model):

    employee_id = models.ForeignKey( Employee, on_delete=models.CASCADE,related_name="documents")

    pancard_number = models.CharField( max_length=20, blank=True,null=True)

    aadhar_number = models.CharField(max_length=12,blank=True,null=True)

    driving_license_number = models.CharField(max_length=30,blank=True,null=True)

    aadhar_front = models.ImageField( upload_to="documents/aadhar/", blank=True, null=True )

    aadhar_back = models.ImageField( upload_to="documents/aadhar/", blank=True, null=True)

    pan_card = models.ImageField( upload_to="documents/pan/", blank=True, null=True)

    photo = models.ImageField( upload_to="documents/photo/", blank=True, null=True )

    driving_license_front = models.ImageField(upload_to="documents/driving_license/",
                                              blank=True, null=True)

    driving_license_back = models.ImageField(upload_to="documents/driving_license/",
                                             blank=True,null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documents - {self.employee_id}"


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.username

from django.utils import timezone

class Expenses_login(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,blank=True, null=True)
    start_time =  models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    date =models.DateField(default=timezone.localdate)
    total_hours=models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status=models.BooleanField(default=False)
    full_leave=models.BooleanField(default=False)
    half_leave=models.BooleanField(default=False)

    def __str__(self):
        return f"Expense Login for {self.employee.first_name} {self.employee.last_name} on {self.date}"

class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    company_logo = models.FileField(upload_to='company_logos/', null=True, blank=True)

    bank_name = models.CharField(max_length=255)
    account_no = models.CharField(max_length=50)
    branch = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=20)
    pancard_no = models.CharField(max_length=20)
    branch_code = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15)
    remark = models.TextField(null=True, blank=True)
    sign = models.ImageField(upload_to='profile/',null=True,blank=True)

    def __str__(self):
        return self.company_name

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'DRAFT'),
        ('SUBMITTED', 'SUBMITTED'),
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED'),
        ('PARTIALLY_APPROVED', 'PARTIALLY_APPROVED'),
        ('CANCELLED', 'CANCELLED'),
        ('PICKED', 'PICKED'),
        ('PACKED', 'PACKED'),
        ('DELIVERED', 'DELIVERED'),

    ]
    po_number = models.CharField(max_length=50, unique=True)
    po_date=models.DateTimeField(auto_now_add=True)

    distributor_id = models.ForeignKey(
        DistributorInformation,
        on_delete=models.CASCADE,
        related_name="purchase_orders"
    )
    product_items=models.JSONField()
    total_items = models.IntegerField(default=0)
    total_quantity = models.IntegerField(default=0)

    remarks = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="SUBMITTED",
    )
    created_by = models.ForeignKey(
        DistributorInformation,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_pos"
    )

    approved_by = models.ForeignKey(
        "Admin",   # or your Admin model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_pos"
    )

    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    unit_distributor_price=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_distributor_price=models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    qty_picked=models.IntegerField(default=0, blank=True, null=True)

    company_id= models.ForeignKey(
        CompanyProfile,
        on_delete=models.SET_NULL,
        related_name="purchase_orders",
        null=True,
        blank=True
    )
    def __str__(self):
        return self.po_number

class Holiday(models.Model):
    holiday_name=models.CharField(max_length=100,blank=True,null=True)
    holiday_date=models.DateField()
    holiday_type=models.CharField(max_length=150)
    is_paid=models.BooleanField(default=False)
    description=models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.holiday_name} ({self.holiday_date})"

class LeaveBalance(models.Model):
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="Leave_Balance",blank=True,null=True)
    leave_type=models.CharField(max_length=100)
    total_allocated=models.IntegerField()
    used_days=models.IntegerField(default=0)
    remaining_days=models.IntegerField()
    cl=models.IntegerField(default=0,blank=True,null=True)
    sl=models.IntegerField(default=0,blank=True,null=True)
    pl=models.IntegerField(default=0,blank=True,null=True)
    ul=models.IntegerField(default=0,blank=True,null=True)
    compensatory_off=models.IntegerField(default=0,blank=True,null=True)
    public_holiday=models.IntegerField(default=0,blank=True,null=True)
    maternity_leave=models.IntegerField(default=0,blank=True,null=True)
    paternity_leave=models.IntegerField(default=0,blank=True,null=True)

    def __str__(self):
        return f"{self.employee_id} - {self.leave_type}"


class LeaveRequest(models.Model):

    LEAVE_TYPE_CHOICES = [
        ("CL", "Casual Leave"),
        ("SL", "Sick Leave"),
        ("PL", "Paid Leave"),
        ("UL", "Unpaid Leave"),
        ("MATERNITY_LEAVE", "maternity_leave"),
        ("PATERNITY_LEAVE", "paternity_leave"),
        
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    employee_id = models.ForeignKey(
        "Employee",
        on_delete=models.CASCADE,
        related_name="leave_requests"
    )
    leave_type = models.CharField(max_length=100, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_leaves = models.PositiveIntegerField()
    reason = models.TextField()
    upload_doc = models.ImageField(upload_to="leave_docs/", null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )

    approved_by = models.ForeignKey(
        "Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_request"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_id.first_name} - {self.leave_type}"

class ExpenseClaim(models.Model):
     STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
     employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='expense_claim', blank=True, null=True)
     lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='expense_claim', blank=True, null=True)
     claim_date=models.DateField()
     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
     status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='Pending' )
     approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True,blank=True,related_name='approved_expense_claims' )
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return f" {self.total_amount} - {self.status}"

class LeadFollowUp(models.Model):
    lead_id=models.ForeignKey(Lead,on_delete=models.CASCADE,related_name="followup",blank=True,null=True)
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="followup",blank=True,null=True)
    followup_date=models.DateField()
    notes = models.TextField(blank=True, null=True)
    next_followup_date = models.DateField(blank=True, null=True)
    status=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    visit=models.ForeignKey(Visit,on_delete=models.CASCADE,related_name="followup",blank=True,null=True)

    def __str__(self):
        return f"Lead {self.lead_id} - {self.status}"


class DistributerOrders(models.Model):
    distributor_id = models.ForeignKey(DistributorInformation, on_delete=models.CASCADE, related_name="orders")
    inventory_serial_id = models.ForeignKey(InventorySerial, on_delete=models.CASCADE, related_name="orders")
    purchase_order_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.distributor_id}"

class Pic_product(models.Model):
    purchase_order_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="picked_products")

    def __str__(self):
        return f"Picked Product for PO {self.purchase_order_id}"
class Pack_product(models.Model):
    purchase_order_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="packed_products")

    def __str__(self):
        return f"Packed Product for PO {self.purchase_order_id}"

class Contact(models.Model):
    name = models.CharField(max_length=100 ,blank=True ,null=True)
    email =models.EmailField(unique=False)
    mobile =models.CharField(max_length=10)
    message =models.TextField()

    def __str__(self):
         return str(self.name)

class Po_payment(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    distributor = models.ForeignKey(
        DistributorInformation,
        on_delete=models.CASCADE,
        related_name="po_payments",blank=True, null=True
    )
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="payments",blank=True, null=True
    )
    images = models.JSONField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    approved_by = models.ForeignKey(Admin,
                on_delete=models.CASCADE,related_name="approved_payments",blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.amount}"

class TravelPlan(models.Model):
    employee_id = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='TravelPlan'
    )
    month = models.CharField(max_length=20)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    region = models.CharField(max_length=100)
    states = models.CharField(max_length=200)
    rm = models.CharField(max_length=100)
    tsm = models.CharField(max_length=100)

    def __str__(self):
        return self.month

class DailyPlan(models.Model):
    travel_plan = models.ForeignKey(
        TravelPlan,
        related_name="daily_plans",
        on_delete=models.CASCADE
    )

    date = models.DateField()
    place = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.place}"


class Salary_payment(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="payrolls"
    )
    month = models.IntegerField()
    year = models.IntegerField()

    present_days = models.IntegerField(default=0)
    paid_leave_days = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    unpaid_leave_days = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    holidays = models.IntegerField(default=0)
    half_days = models.IntegerField(default=0)
    weekly_offs = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)

    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,blank=True,null=True)

    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "month", "year")

    def __str__(self):
        return f"{self.employee.employee_code} - {self.month}/{self.year}"

class DistributorInformation_Target(models.Model):

    distributor = models.ForeignKey(DistributorInformation, on_delete=models.CASCADE)
    month = models.DateField()  # store 1st day of month
    target = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.distributor} - {self.month.strftime('%Y-%m')}"

class Product_Target(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    month = models.DateField()  # store 1st day of month
    target = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.month.strftime('%Y-%m')}"


class Category_Target(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    month = models.DateField()  # store 1st day of month
    target = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.month.strftime('%Y-%m')}"

import uuid

class Shipment(models.Model):

    SHIPMENT_STATUS = (
        ('created', 'Created'),
        ('picked', 'Picked By Courier'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out For Delivery'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    )

    order_id= models.ForeignKey("PurchaseOrder", on_delete=models.CASCADE, related_name="shipments")

    tracking_number = models.CharField(max_length=100, unique=True)

    shipment_status = models.CharField(max_length=50, choices=SHIPMENT_STATUS, default="created")

    shipped_at = models.DateTimeField(null=True, blank=True)

    estimated_delivery = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    name = models.CharField(max_length=200,blank=True,null=True)

    contact_number = models.CharField(max_length=20,blank=True,null=True)
    
    email = models.EmailField(blank=True, null=True)
    
    service_type = models.CharField(max_length=100, blank=True, null=True)
    
    image=models.ImageField(upload_to='courier_images/', blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = "TRK-" + str(uuid.uuid4()).split("-")[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tracking_number


class CarBrand(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    brand_id =  models.ForeignKey(
        CarBrand,
        on_delete=models.CASCADE,
        related_name="cars"
    )
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class GetQuote(models.Model):
    SERVICE_CHOICE = [
        ('SUNROOF PROTECTION FILM', 'SUNROOF PROTECTION FILM'),
        ('PAINT PROTECTION FILM', 'PAINT PROTECTION FILM'),
        ('WINDOW FILM', 'WINDOW FILM'),
        ('WINDSCREEN PROTECTION FILM', 'WINDSCREEN PROTECTION FILM')
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    Address = models.TextField()

    brand_id = models.ForeignKey(
        CarBrand,
        on_delete=models.CASCADE,
        related_name="quotes"
    )

    model_id = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        related_name="quotes"
    )

    # ✅ FIXED HERE
    service = models.CharField(
        max_length=100,
        choices=SERVICE_CHOICE,
        default='WINDOW FILM'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Region_Target(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    month = models.DateField()  # store 1st day of month
    target = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.distributor} - {self.month.strftime('%Y-%m')}"

class Gallery(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    gallery_sequence = models.IntegerField()

    def __str__(self):
        return self.name


class ReplacementRequest(models.Model):

    STATUS_CHOICES = (

        ("PENDING", "PENDING"),
        ("APPROVED", "APPROVED"),
        ("REJECTED", "REJECTED"),
        ("COMPLETED", "COMPLETED"),

    )
    old_serial = models.ForeignKey(
        "InventorySerial",
        on_delete=models.CASCADE,
        related_name="old_replacement_requests"
    )

    new_serial = models.ForeignKey(
        "InventorySerial",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="new_replacement_requests"
    )

    reason = models.TextField()
    remarks = models.TextField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    distributor_id = models.ForeignKey(
        "DistributorInformation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,related_name="replacement_requests"
    )
    new_distributor = models.ForeignKey(
        "DistributorInformation",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    product_id = models.ForeignKey(
        "Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    purchase_order_id = models.ForeignKey(
        "PurchaseOrder",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="original_replacement_requests"
    )
    replacement_po = models.ForeignKey(
        "PurchaseOrder",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replacement_po_requests"
    )

    image = models.JSONField(default=list, blank=True, null=True)
    def __str__(self):
        return f"Replacement #{self.id} - {self.old_serial.serial_number}"


from django.utils import timezone
from datetime import timedelta

class EmployeeForgotPassword(models.Model):
    email = models.EmailField()
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)
    
    
from datetime import timedelta
class DistriutorForgotPassword(models.Model):
    email = models.EmailField()
    distributor = models.ForeignKey("DistributorInformation",on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)
    
class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='testimonial/',blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    rating = models.IntegerField(default=1)
   
    created_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name