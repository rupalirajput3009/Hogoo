from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password



class AdminSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    mobile = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=255, write_only=True)
    status = serializers.CharField(max_length=20, default="NEW", required=False)
    created_at = serializers.DateTimeField(read_only=True)

    # 🔹 Validate unique email
    def validate_email(self, value):
        qs = Admin.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    # 🔹 Validate unique mobile
    def validate_mobile(self, value):
        qs = Admin.objects.filter(mobile=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("This mobile number is already in use.")
        return value

    # 🔹 Create
    def create(self, validated_data):
        return Admin.objects.create(**validated_data)

    # 🔹 Update
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.mobile = validated_data.get("mobile", instance.mobile)
        instance.password = validated_data.get("password", instance.password)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            admin = Admin.objects.get(email=email)
        except Admin.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if admin.password != password:
            raise serializers.ValidationError("Invalid password")

        return admin


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)

    status = serializers.BooleanField(default=True)

    def validate_name(self, value):
        qs = Category.objects.filter(name__iexact=value)

        # exclude self on update
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)

        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class MaterialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    status = serializers.BooleanField()

    def create(self, validated_data):
        return Material.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

class ColourSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    colour_name = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        allow_null=True
    )
    status = serializers.BooleanField()

    def create(self, validated_data):
        return Colour.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.colour_name = validated_data.get(
            "colour_name", instance.colour_name
        )
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    product_name = serializers.CharField(max_length=300)
    product_codes = serializers.CharField(max_length=200)
    sku = serializers.CharField(max_length=300)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        required=False
    )
    category_name = serializers.CharField(source="category_id.name", read_only=True)

    material_id = serializers.PrimaryKeyRelatedField(
        queryset=Material.objects.all(),
        allow_null=True,
        required=False
    )
    material_name = serializers.CharField(source="material_id.title", read_only=True)

    colour_id = serializers.PrimaryKeyRelatedField(
        queryset=Colour.objects.all(),
        allow_null=True,
        required=False
    )
    colour_name = serializers.CharField(source="colour_id.colour_name", read_only=True)

    film_type = serializers.CharField(max_length=200)
    finish = serializers.CharField(max_length=100)
    application_area = serializers.CharField(max_length=200)
    thickness = serializers.CharField(max_length=100)
    specification = serializers.CharField()
    warranty = serializers.CharField(max_length=300)

    adhesive = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    anti_yellowing = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    scratch_resistant = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    uv_resistance = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    hydrophobic = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    stain_resistant = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    elongation = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tear_strength = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    tempeerature_resistance = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    peel_adhesion = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    anti_rockclip = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    elongation_rate_tpu = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    elongation_rate_hard = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    mrp = serializers.DecimalField(max_digits=10, decimal_places=2)

    thumbnail_image = serializers.ImageField()
    image1 = serializers.ImageField(required=False, allow_null=True)
    image2 = serializers.ImageField(required=False, allow_null=True)
    image3 = serializers.ImageField(required=False, allow_null=True)
    image4 = serializers.ImageField(required=False, allow_null=True)
    installation_video_url = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    product_images = serializers.SerializerMethodField()

    status = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # ✅ corrected calculated fields
    total_product = serializers.SerializerMethodField()
    reserved_product = serializers.SerializerMethodField()
    stock_available = serializers.SerializerMethodField()

    mou = serializers.CharField(max_length=200, required=False, allow_null=True)
    hsn_code = serializers.CharField(max_length=50, required=False, allow_null=True)
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        style={'base_template': 'textarea.html'}
    )
    GST = serializers.CharField(max_length=200, required=False, allow_null=True)
    product_sequence = serializers.IntegerField(required=False, allow_null=True)

    def validate_warranty(self, value):
        if not str(value).isdigit():
            raise serializers.ValidationError("Warranty must contain only integers.")
        return value

    # -------------------
    # Serial Count Methods
    # -------------------
    def get_total_product(self, obj):
        return obj.inventory_serials.count() if hasattr(obj, "inventory_serials") else 0
    def get_stock_available(self, obj):
        return obj.inventory_serials.filter(status="IN_STOCK").count()
    def get_reserved_product(self, obj):
        return (
            obj.inventory_serials.filter(status="RESERVED").count()
            if hasattr(obj, "inventory_serials")
            else 0
        )
    def get_total_product(self, obj):
        return obj.inventory_serials.count()

    # def get_stock_available(self, obj):
    #     if hasattr(obj, "inventory_serials"):
    #         total = obj.inventory_serials.count()
    #         reserved = obj.inventory_serials.filter(status="RESERVED").count()
    #         return total - reserved
    #     return 0

    # -------------------
    # Unique Validation
    # -------------------
    def validate_product_codes(self, value):
        qs = Product.objects.filter(product_codes=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("product_codes must be unique.")
        return value

    def validate_sku(self, value):
        qs = Product.objects.filter(sku=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("sku must be unique.")
        return value
    
    # -------------------
    # Gallery Images List
    # -------------------
    def get_product_images(self, obj):
        images = []
        for field in ["image1", "image2", "image3", "image4"]:
            img = getattr(obj, field)
            if img:
                images.append(img.url)
        return images

    # -------------------
    # Create & Update
    # -------------------
    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class BannerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    image = serializers.ImageField()
    status = serializers.BooleanField(default=False)

    # 🔹 Create Method
    def create(self, validated_data):
        banner = Banner.objects.create(
            title=validated_data.get('title'),
            image=validated_data.get('image'),
            status=validated_data.get('status', False)
        )
        return banner

    # 🔹 Update Method
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class ImportShipmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    supplier_name = serializers.CharField(max_length=100)
    supplier_invoice_no = serializers.CharField(max_length=200)
    invoice_currency = serializers.CharField(max_length=10)

    invoice_value_foreign = serializers.DecimalField(
        max_digits=10, decimal_places=2
    )
    exchange_rate = serializers.DecimalField(
        max_digits=10, decimal_places=2
    )
    invoice_value_inr = serializers.DecimalField(
        max_digits=10, decimal_places=2
    )

    bl_awb_no = serializers.CharField(max_length=200)
    arrival_date = serializers.DateTimeField()

    # -------- VALIDATION ----------
    def validate_invoice_value_foreign(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invoice value must be greater than 0")
        return value

    def validate_exchange_rate(self, value):
        if value <= 0:
            raise serializers.ValidationError("Exchange rate must be greater than 0")
        return value

class ImportCostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    shipment_id = serializers.PrimaryKeyRelatedField(
        queryset=Import_shipment.objects.all()
    )

    supplier_invoice_no = serializers.SerializerMethodField()
    shipment_name = serializers.SerializerMethodField()

    cost_type_freight = serializers.CharField()
    cost_type_insurance = serializers.CharField()
    cost_type_duty = serializers.CharField()
    cost_type_igst = serializers.CharField()
    cost_type_port = serializers.CharField()
    cost_type_cha = serializers.CharField()
    cost_type_trasnport = serializers.CharField()
    cost_type_others = serializers.CharField()

    cost_amount_inr = serializers.DecimalField(max_digits=15, decimal_places=2)
    capitalized = serializers.BooleanField(default=False)
    reference_doc = serializers.CharField()

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # ---------- SerializerMethodFields ----------
    def get_supplier_invoice_no(self, obj):
        return obj.shipment_id.supplier_invoice_no

    def get_shipment_name(self, obj):
        return obj.shipment_id.supplier_name


    # ---------- CREATE ----------
    def create(self, validated_data):
        return Import_cost.objects.create(**validated_data)

    # ---------- UPDATE ----------
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(update_fields=validated_data.keys())
        return instance

    # ---------- VALIDATION ----------
    def validate_cost_amount_inr(self, value):
        if value < 0:
            raise serializers.ValidationError("Cost amount must be positive")
        return value

class ShipmentProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    shipment_id = serializers.PrimaryKeyRelatedField(
        queryset=Import_shipment.objects.all()
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    product_name = serializers.SerializerMethodField()

    batch_data = serializers.CharField()
    quantity = serializers.IntegerField()
    allocation_basis = serializers.CharField(max_length=500)
    landed_cost_allocated = serializers.DecimalField(max_digits=10, decimal_places=2)
    per_unit_cost_inr = serializers.DecimalField(max_digits=15, decimal_places=2)
    per_unit_cost_usd = serializers.DecimalField(max_digits=15, decimal_places=2)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        required=False,
        allow_null=True
    )
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=WareHouse.objects.all(),
        required=False,
        allow_null=True
    )
    location_name = serializers.SerializerMethodField()
    warehouse_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    def get_warehouse_name(self, obj):
        return obj.warehouse_id.name if obj.warehouse_id else None
    def get_location_name(self, obj):
        return obj.location_id.name if obj.location_id else None
    # ---------- CREATE ----------
    def create(self, validated_data):
        return Shipment_product.objects.create(**validated_data)

    # ---------- UPDATE ----------
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    # ---------- VALIDATION ----------
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value

    def get_product_name(self, obj):
        return obj.product_id.product_name



class DepartmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    status = serializers.ChoiceField(choices=['Active', 'Inactive'])
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    created_at = serializers.DateTimeField(read_only=True)

    def validate_name(self, value):
        if self.instance is None and Department.objects.filter(name=value).exists():
            raise serializers.ValidationError("Department already exists")
        return value

    def create(self, validated_data):
        return Department.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.status = validated_data.get("status", instance.status)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance

class RolesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    status = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)

    # 🔹 Validation
    def validate_name(self, value):
        if self.instance is None and Roles.objects.filter(name=value).exists():
            raise serializers.ValidationError("Role already exists")
        return value

    # 🔹 Create
    def create(self, validated_data):
        return Roles.objects.create(**validated_data)

    # 🔹 Update
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class OfficeBranchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    address = serializers.CharField()
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(
        required=False,
        allow_null=True,
        default='Inactive'
    )

    # 🔹 Validation
    def validate_name(self, value):
        if self.instance is None and Office_branch.objects.filter(name=value).exists():
            raise serializers.ValidationError("Office branch already exists")
        return value

    # 🔹 Create
    def create(self, validated_data):
        return Office_branch.objects.create(**validated_data)

    # 🔹 Update
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.country = validated_data.get("country", instance.country)
        instance.status = validated_data.get("status",instance.status)

        instance.save()
        return instance




class EmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    employee_code = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=255, write_only=True)

    gender = serializers.CharField(max_length=10)
    date_of_birth = serializers.DateField()

    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)

    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all()
    )
    department_name = serializers.SerializerMethodField()

    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Roles.objects.all()
    )
    role_name = serializers.SerializerMethodField()

    joining_date = serializers.DateField()

    employment_type = serializers.ChoiceField(
        choices=Employee.EMPLOYMENT_TYPE_CHOICES
    )
    status = serializers.ChoiceField(
        choices=Employee.STATUS_CHOICES,
        default='Active'
    )

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    office_branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Office_branch.objects.all(),
        required=False,
        allow_null=True
    )
    office_branch_name = serializers.SerializerMethodField()

    # 🔹 GET METHODS
    def get_department_name(self, obj):
        return obj.department_id.name if obj.department_id else None

    def get_role_name(self, obj):
        return obj.role_id.name if obj.role_id else None

    def get_office_branch_name(self, obj):
        return obj.office_branch_id.name if obj.office_branch_id else None

    # 🔥 FIXED FIELD VALIDATIONS (handles both POST & PATCH correctly)

    def validate_email(self, value):
        instance = getattr(self, 'instance', None)
        qs = Employee.objects.filter(email=value)

        if instance:
            qs = qs.exclude(id=instance.id)

        if qs.exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_phone(self, value):
        instance = getattr(self, 'instance', None)
        qs = Employee.objects.filter(phone=value)

        if instance:
            qs = qs.exclude(id=instance.id)

        if qs.exists():
            raise serializers.ValidationError("Mobile number already exists.")
        return value

    def validate_employee_code(self, value):
        instance = getattr(self, 'instance', None)
        qs = Employee.objects.filter(employee_code=value)

        if instance:
            qs = qs.exclude(id=instance.id)

        if qs.exists():
            raise serializers.ValidationError("Employee code already exists.")
        return value

    # 🔹 OPTIONAL (kept as you had it, no change)
    def validate(self, attrs):
        instance = getattr(self, 'instance', None)

        if instance:
            if Employee.objects.filter(email=attrs.get('email')).exclude(id=instance.id).exists():
                raise serializers.ValidationError({"email": "Email already exists."})

            if Employee.objects.filter(phone=attrs.get('phone')).exclude(id=instance.id).exists():
                raise serializers.ValidationError({"phone": "Mobile number already exists."})

            if Employee.objects.filter(employee_code=attrs.get('employee_code')).exclude(id=instance.id).exists():
                raise serializers.ValidationError({"employee_code": "Employee code already exists."})

        return attrs

    # 🔹 CREATE
    def create(self, validated_data):
        return Employee.objects.create(**validated_data)

    # 🔹 UPDATE
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class EmployeeLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            employee = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        # ✅ Plain text password check
        if employee.password != password:
            raise serializers.ValidationError("Invalid email or password")

        return employee

import re

class LeadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    lead_type = serializers.ChoiceField(
        choices=['Distributor', 'Retailer', 'Direct']
    )
    business_name = serializers.CharField(max_length=255)
    contact_person = serializers.CharField(max_length=255)

    phone = serializers.CharField(max_length=15)
    email = serializers.EmailField()

    location = serializers.CharField(
        max_length=255, required=False, allow_null=True, allow_blank=True
    )
    address = serializers.CharField()
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)

    interest_level = serializers.ChoiceField(
        choices=['Warm', 'Cold', 'Hot']
    )

    lead_status = serializers.ChoiceField(
        choices=['Lead', 'Prospect', 'Converted', 'Lost', 'Follow_up'],
        required=False,
        default='Lead'
    )

    remarks = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    week = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    month = serializers.CharField(required=True)
    date = serializers.DateField(required=False)

    outlet_age = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ppf_installers = serializers.BooleanField(required=False)
    brand_dealing = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    past_distributor_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    dealer_landing_cost = serializers.DecimalField(
    max_digits=10,
    decimal_places=2,
    required=True,
    error_messages={
        "required": "Dealer landing cost is required.",
        "null": "Dealer landing cost cannot be null.",
        "invalid": "Enter a valid dealer landing cost."
    }
    )

    cars_per_month = serializers.IntegerField(
    required=True,
    error_messages={
        "required": "Cars per month is required.",
        "null": "Cars per month cannot be null.",
        "invalid": "Enter a valid number of cars."
    }
    )

    price_feedback = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    quality_feedback = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    demo = serializers.BooleanField(required=False)

    created_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )

    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,
        allow_null=True
    )

    created_by_name = serializers.SerializerMethodField()
    created_by_code = serializers.SerializerMethodField()
    assigned_to_name = serializers.SerializerMethodField()
    assigned_to_code = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(read_only=True)
    assigned_at = serializers.DateTimeField(required=False, allow_null=True)
    updated_at = serializers.DateTimeField(read_only=True)

    lead_source = serializers.ChoiceField(
        choices=['WEBSITE', 'WHATSAPP', 'CALL', 'EMAIL', 'EXHIBITION', 'REFERRAL', 'SALES'],
        required=False,
        allow_null=True,
        allow_blank=True
    )

    region= serializers.PrimaryKeyRelatedField(   # ✅ accept ID
        queryset=Region.objects.all(),


        required=False,
        allow_null=True
    )
    region_name = serializers.CharField(source='region.name', read_only=True)

    def create(self, validated_data):
        return Lead.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
        return None

    def get_created_by_code(self, obj):
        if obj.created_by:
            return obj.created_by.employee_code
        return None

    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return f"{obj.assigned_to.first_name} {obj.assigned_to.last_name}".strip()
        return None

    def get_assigned_to_code(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.employee_code
        return None




class EmployeeLeadMonthlyReportSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_name = serializers.CharField()
    employee_code = serializers.CharField(allow_null=True)
    month = serializers.CharField()
    total_leads = serializers.IntegerField()
    converted_leads = serializers.IntegerField()
    conversion_ratio = serializers.CharField()
    download_url = serializers.CharField(allow_null=True)



class ExpenseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=True,
        allow_null=True
    )

    employee_name = serializers.SerializerMethodField()
    lead_id = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(),
        required=False,
        allow_null=True
    )
    lead_type = serializers.SerializerMethodField()
    lead_name = serializers.SerializerMethodField()
    vendor_name = serializers.CharField(max_length=255,required=False)
    expense_type = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateField()
    status = serializers.BooleanField(default=False)
    receipt_photo = serializers.FileField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

    def get_employee_name(self, obj):
        if obj.employee_id:
            return f"{obj.employee_id.first_name} {obj.employee_id.last_name}"
        return None
    def get_lead_type(self, obj):
        if obj.lead_id:
            return obj.lead_id.lead_type
        return None
    def get_lead_name(self, obj):
        if obj.lead_id:
            return obj.lead_id.business_name
        return None

    def create(self, validated_data):
        return Expense.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    image = serializers.ImageField()
    content = serializers.CharField()
    shortcontent = serializers.CharField()
    date = serializers.DateField()
    month = serializers.CharField(max_length=100)
    tag = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(read_only=True)

    # 🔹 Create Method
    def create(self, validated_data):
        return Blog.objects.create(**validated_data)

    # 🔹 Update Method
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.content = validated_data.get('content', instance.content)
        instance.shortcontent = validated_data.get('shortcontent', instance.shortcontent)
        instance.date = validated_data.get('date', instance.date)
        instance.month = validated_data.get('month', instance.month)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.save()
        return instance


from rest_framework import serializers
from decimal import Decimal
from django.utils import timezone
from .models import Visit, Employee, Lead, LeadFollowUp

from rest_framework import serializers
from decimal import Decimal
from django.utils import timezone
from .models import Visit, Employee, Lead, LeadFollowUp

from rest_framework import serializers
from decimal import Decimal
from django.utils import timezone
from .models import Visit, Employee, Lead, LeadFollowUp

from rest_framework import serializers
from decimal import Decimal
from django.utils import timezone
from .models import Visit, Employee, Lead, LeadFollowUp
from rest_framework import serializers
from math import radians, cos, sin, asin, sqrt
from math import radians, sin, cos, sqrt, atan2
class VisitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,
        allow_null=True
    )

    lead_id = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(),
        required=False,
        allow_null=True
    )
    address = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, required=False, allow_null=True)
    visit_purpose = serializers.CharField(max_length=255)
    visit_date = serializers.DateTimeField()

    check_in_time = serializers.DateTimeField(required=False, allow_null=True)
    checkout_time = serializers.DateTimeField(required=False, allow_null=True)

    total_hr = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
        read_only=True
    )

    followup_date = serializers.DateTimeField(required=False, allow_null=True)
    followup_date_display = serializers.SerializerMethodField(read_only=True)

    followup_type = serializers.ChoiceField(
        choices=Visit.FOLLOWUP_CHOICES,
        required=False,
        allow_null=True
    )

    contact_person = serializers.CharField(max_length=255, required=False, allow_null=True)
    notes = serializers.CharField(style={'base_template': 'textarea.html'})
    order_information = serializers.CharField(required=False, allow_null=True, style={'base_template': 'textarea.html'})
    payment_details = serializers.CharField(required=False, allow_null=True, style={'base_template': 'textarea.html'})
    payment_image = serializers.ImageField(required=False, allow_null=True)
    images = serializers.ImageField(required=False, allow_null=True)
    order_name = serializers.CharField(required=False, allow_null=True)
    status = serializers.SerializerMethodField()


    status = serializers.ChoiceField(
        choices=Visit.STATUS_CHOICES,
        required=False,
        default="PENDING"
    )

    # ---------------- SerializerMethodFields ----------------
    employee_name = serializers.SerializerMethodField()
    lead_type = serializers.SerializerMethodField()
    lead_name = serializers.SerializerMethodField()
    contact_person_display = serializers.SerializerMethodField()
    location_display = serializers.SerializerMethodField()
    address_display = serializers.SerializerMethodField()
    lead_status = serializers.SerializerMethodField()
    start_latitude = serializers.DecimalField(
    max_digits=9,
    decimal_places=6,
    required=False,
    allow_null=True
    )

    start_longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        allow_null=True
    )

    end_latitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        allow_null=True
    )

    end_longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        allow_null=True
    )

    total_distance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
        read_only=True
    )

    # ---------------- Validation ----------------
    def to_internal_value(self, data):
        if hasattr(data, 'copy'):
            mutable_data = data.copy()
        else:
            mutable_data = dict(data)

        for field in ['check_in_time', 'checkout_time']:
            if field in mutable_data and mutable_data.get(field) in ('', 'true', 'True', 'null', None):
                mutable_data[field] = timezone.now().isoformat()

        return super().to_internal_value(mutable_data)

    def validate(self, data):
        check_in = data.get("check_in_time")
        checkout = data.get("checkout_time")
        if check_in and checkout and checkout < check_in:
            raise serializers.ValidationError(
                {"checkout_time": "Checkout time cannot be earlier than check-in time."}
            )
        return data
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        if not lat1 or not lon1 or not lat2 or not lon2:
            return None

        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)

        # Earth radius in KM
        R = 6371.0

        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)

        a = (
            sin(dlat / 2) ** 2
            + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return Decimal(str(round(distance, 2)))

    # ---------------- CREATE ----------------
    def create(self, validated_data):
        if not validated_data.get("check_in_time"):
            validated_data["check_in_time"] = None

        if "checkout_time" not in validated_data:
            validated_data["checkout_time"] = None

        # Respect manually provided status
        status = validated_data.get("status", None)

        visit = Visit.objects.create(**validated_data)

        # Auto calculate distance from start location to end location
        if (
            visit.start_latitude and
            visit.start_longitude and
            visit.end_latitude and
            visit.end_longitude
        ):
            visit.total_distance = self.calculate_distance(
                visit.start_latitude,
                visit.start_longitude,
                visit.end_latitude,
                visit.end_longitude
            )
            visit.save(update_fields=["total_distance"])

        # Auto calculate total hours if times exist
        if visit.check_in_time and visit.checkout_time:
            total_seconds = (visit.checkout_time - visit.check_in_time).total_seconds()
            visit.total_hr = round(Decimal(total_seconds / 3600), 2)

            if not status:
                visit.status = "COMPLETED"

            visit.save(update_fields=["total_hr", "status"])

        else:
            if status:
                visit.status = status
                visit.save(update_fields=["status"])

        # Create follow-up if needed
        followup_date = validated_data.get("followup_date")

        if followup_date and visit.lead_id:
            LeadFollowUp.objects.create(
                employee_id=visit.employee_id,
                lead_id=visit.lead_id,
                visit=visit,
                followup_date=followup_date,
                notes=visit.notes,
                next_followup_date=None,
            )

        return visit

    # ---------------- UPDATE ----------------
    def update(self, instance, validated_data):
        # Update times
        if "check_in_time" in validated_data:
            instance.check_in_time = validated_data["check_in_time"]
        if "checkout_time" in validated_data:
            instance.checkout_time = validated_data["checkout_time"]

        # Update other fields
        for attr, value in validated_data.items():
            if attr not in ["check_in_time", "checkout_time"]:
                setattr(instance, attr, value)

        # Recalculate total hours if both times exist
        if instance.check_in_time and instance.checkout_time:
            total_seconds = (instance.checkout_time - instance.check_in_time).total_seconds()
            instance.total_hr = round(Decimal(total_seconds / 3600), 2)
            # Auto mark COMPLETED only if status not manually set
            if "status" not in validated_data:
                instance.status = "COMPLETED"
        else:
            instance.total_hr = None
            # Respect manually provided status if given
            if "status" in validated_data:
                instance.status = validated_data["status"]
            elif instance.followup_date:
                instance.status = "FOLLOW_UP"
            else:
                instance.status = "PENDING"

        if (
            instance.start_latitude and
            instance.start_longitude and
            instance.end_latitude and
            instance.end_longitude
        ):
            instance.total_distance = self.calculate_distance(
                instance.start_latitude,
                instance.start_longitude,
                instance.end_latitude,
                instance.end_longitude
            )
        else:
            instance.total_distance = None

        instance.save()

        # Create follow-up if followup_date exists
        followup_date = validated_data.get("followup_date") or instance.followup_date
        if followup_date and instance.lead_id:
            LeadFollowUp.objects.create(
                employee_id=instance.employee_id,
                lead_id=instance.lead_id,
                visit=instance,
                followup_date=followup_date,
                notes=instance.notes,
                next_followup_date=None,
            )

        return instance

    # ---------------- SerializerMethodFields ----------------
    def get_employee_name(self, obj):
        if obj.employee_id:
            return f"{obj.employee_id.first_name} {obj.employee_id.last_name}"
        return None

    def get_lead_type(self, obj):
        if obj.lead_id:
            return obj.lead_id.lead_type
        return None

    def get_lead_name(self, obj):
        if obj.lead_id:
            return obj.lead_id.business_name
        return None

    def get_contact_person_display(self, obj):
        if obj.contact_person:
            return obj.contact_person
        elif obj.lead_id and obj.lead_id.contact_person:
            return obj.lead_id.contact_person
        return None

    def get_location_display(self, obj):
        if obj.location:
            return obj.location
        elif obj.lead_id and obj.lead_id.location:
            return obj.lead_id.location
        return None

    def get_address_display(self, obj):
        if obj.address:
            return obj.address
        elif obj.lead_id and obj.lead_id.address:
            return obj.lead_id.address
        return None

    def get_status_display(self, obj):
        return obj.get_status_display() if obj.status else "PENDING"

    def get_followup_date_display(self, obj):
        if obj.followup_date:
            return obj.followup_date.date()
        return None

    def get_lead_status(self, obj):
        if obj.lead_id:
            return obj.lead_id.lead_status
        return None




class BusinessLegalInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessLegalInfo
        fields = "__all__"


from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import DistributorInformation, Region


# class DistributorInformationSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = DistributorInformation
#         fields = '__all__'

#         # ✅ Only required fields
#         extra_kwargs = {
#             'distributor_name': {'required': True},
#             'date_of_registration': {'required': True},
#             'contact_person_name': {'required': True},
#             'mobile_number': {'required': True},
#             'email_id': {'required': True},
#         }

#     # ==============================
#     # ✅ COMMON FUNCTION (REUSABLE)
#     # ==============================
#     def validate_unique_optional(self, field_name, value):
#         if value in ["", None]:
#             return None

#         instance = getattr(self, 'instance', None)

#         qs = DistributorInformation.objects.filter(**{field_name: value})

#         if instance:
#             qs = qs.exclude(id=instance.id)

#         if qs.exists():
#             raise serializers.ValidationError(f"{field_name.replace('_', ' ').title()} already exists")

#         return value


#     def validate_name_fields(self, data):

#         name_fields = [
#             'distributor_name',
#             'contact_person_name',
#             'bank_account_name',
#             'bank_name',
#             'branch_name',
#             'warehouse_address',
#             'logistics_partner',
#             'service_cities',
#             'kyc_verified_by',
#             'remarks'
#         ]

#         for field in name_fields:
#             value = data.get(field)

#             if value:
#                 if not re.fullmatch(r'[A-Za-z ]+', str(value)):
#                     raise serializers.ValidationError({
#                         field: "Only alphabets are allowed (A-Z and space only)"
#                     })

#         return data

#     # ==============================
#     # ✅ POSITIVE NUMBER VALIDATION (ADDED)
#     # ==============================
#     def validate_positive_number_fields(self, data):

#         number_fields = [
#             'account_number',
#             'credit_limit',
#             'payment_terms_days',
#             'storage_area_sqft',
#             'monthly_distribution_capacity'
#         ]

#         for field in number_fields:
#             value = data.get(field)

#             if value is not None:
#                 try:
#                     num = float(value)
#                 except (TypeError, ValueError):
#                     raise serializers.ValidationError({
#                         field: "Only numeric values are allowed"
#                     })

#                 if num < 0:
#                     raise serializers.ValidationError({
#                         field: "Only positive numbers or 0 are allowed"
#                     })

#         return data

#     # ==============================
#     # ✅ FIELD VALIDATIONS
#     # ==============================

#     def validate_mobile_number(self, value):
#         if not re.match(r'^[6-9]\d{9}$', value):
#             raise serializers.ValidationError("Enter valid 10 digit mobile number")
#         return value

#     def validate_alternate_mobile(self, value):
#         if value and not re.match(r'^[6-9]\d{9}$', value):
#             raise serializers.ValidationError("Enter valid alternate mobile number")
#         return value

#     def validate_aadhaar_number(self, value):
#         if value not in ["", None]:
#             if not value.isdigit() or len(value) != 12:
#                 raise serializers.ValidationError("Aadhaar must be 12 digits")
#         return self.validate_unique_optional('aadhaar_number', value)

#     def validate_pan_number(self, value):
#         if value not in ["", None]:
#             if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', value):
#                 raise serializers.ValidationError("Invalid PAN format")
#         return self.validate_unique_optional('pan_number', value)

#     def validate_gst_number(self, value):
#         return self.validate_unique_optional('gst_number', value)

#     def validate_account_number(self, value):
#         return self.validate_unique_optional('account_number', value)

#     def validate_ifsc_code(self, value):
#         if value and not re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', value):
#             raise serializers.ValidationError("Invalid IFSC code")
#         return value

#     def validate_pincode(self, value):
#         if value and not re.match(r'^\d{6}$', value):
#             raise serializers.ValidationError("Pincode must be 6 digits")
#         return value

#     # ==============================
#     # ✅ OBJECT LEVEL VALIDATION
#     # ==============================
#     def validate(self, data):

#         # Bank dependency
#         if data.get('account_number') and not data.get('ifsc_code'):
#             raise serializers.ValidationError({
#                 "ifsc_code": "IFSC code required when account number is provided"
#             })

#         # Warehouse dependency
#         if data.get('warehouse_available') and not data.get('warehouse_address'):
#             raise serializers.ValidationError({
#                 "warehouse_address": "Warehouse address required"
#             })

#         return data

#     # ==============================
#     # ✅ CREATE / UPDATE FIX (IMPORTANT)
#     # ==============================
#     def clean_empty_to_none(self, validated_data):
#         unique_fields = [
#             'aadhaar_number',
#             'pan_number',
#             'gst_number',
#             'account_number'
#         ]

#         for field in unique_fields:
#             if validated_data.get(field) in ["", None]:
#                 validated_data[field] = None

#         return validated_data




#     def create(self, validated_data):
#         validated_data = self.clean_empty_to_none(validated_data)
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         validated_data = self.clean_empty_to_none(validated_data)
#         return super().update(instance, validated_data)




class DistributorInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DistributorInformation
        fields = '__all__'

        extra_kwargs = {
            'distributor_name': {'required': True},
            'date_of_registration': {'required': True},
            'contact_person_name': {'required': True},
            'mobile_number': {'required': True},
            'email_id': {'required': True},
        }

    # ==============================
    # ✅ COMMON FUNCTION (REUSABLE)
    # ==============================
    def validate_unique_optional(self, field_name, value):
        if value in ["", None]:
            return None

        instance = getattr(self, 'instance', None)

        qs = DistributorInformation.objects.filter(**{field_name: value})

        if instance:
            qs = qs.exclude(id=instance.id)

        if qs.exists():
            raise serializers.ValidationError(
                f"{field_name.replace('_', ' ').title()} already exists"
            )

        return value

    # ==============================
    # ✅ NAME VALIDATION
    # ==============================
    def validate_name_fields(self, data):

        name_fields = [
            'distributor_name',
            'contact_person_name',
            'bank_account_name',
            'bank_name',
            'branch_name',
            'warehouse_address',
            'logistics_partner',
            'service_cities',
            'kyc_verified_by',
            'remarks'
        ]

        for field in name_fields:
            value = data.get(field)

            if value:
                if not re.fullmatch(r'[A-Za-z ]+', str(value)):
                    raise serializers.ValidationError({
                        field: "Only alphabets are allowed (A-Z and space only)"
                    })

        return data

    # ==============================
    # ✅ POSITIVE NUMBER VALIDATION (ADDED)
    # ==============================
    def validate_positive_number_fields(self, data):

        number_fields = [
            'account_number',
            'credit_limit',
            'payment_terms_days',
            'storage_area_sqft',
            'monthly_distribution_capacity'
        ]

        for field in number_fields:
            value = data.get(field)

            if value is not None:
                try:
                    num = float(value)
                except (TypeError, ValueError):
                    raise serializers.ValidationError({
                        field: "Only numeric values are allowed"
                    })

                if num < 0:
                    raise serializers.ValidationError({
                        field: "Only positive numbers or 0 are allowed"
                    })

        return data

    # ==============================
    # ✅ FIELD VALIDATIONS
    # ==============================
    def validate_mobile_number(self, value):
        if not re.match(r'^[6-9]\d{9}$', value):
            raise serializers.ValidationError("Enter valid 10 digit mobile number")
        return value

    def validate_alternate_mobile(self, value):
        if value and not re.match(r'^[6-9]\d{9}$', value):
            raise serializers.ValidationError("Enter valid alternate mobile number")
        return value

    def validate_aadhaar_number(self, value):
        if value not in ["", None]:
            if not value.isdigit() or len(value) != 12:
                raise serializers.ValidationError("Aadhaar must be 12 digits")
        return self.validate_unique_optional('aadhaar_number', value)

    def validate_pan_number(self, value):
        if value not in ["", None]:
            if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', value):
                raise serializers.ValidationError("Invalid PAN format")
        return self.validate_unique_optional('pan_number', value)

    def validate_gst_number(self, value):
        return self.validate_unique_optional('gst_number', value)

    def validate_account_number(self, value):
        return self.validate_unique_optional('account_number', value)

    def validate_ifsc_code(self, value):
        if value and not re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', value):
            raise serializers.ValidationError("Invalid IFSC code")
        return value

    def validate_pincode(self, value):
        if value and not re.match(r'^\d{6}$', value):
            raise serializers.ValidationError("Pincode must be 6 digits")
        return value

    # ==============================
    # ✅ OBJECT LEVEL VALIDATION
    # ==============================
    def validate(self, data):

        # Bank dependency
        if data.get('account_number') and not data.get('ifsc_code'):
            raise serializers.ValidationError({
                "ifsc_code": "IFSC code required when account number is provided"
            })

        # Warehouse dependency
        if data.get('warehouse_available') and not data.get('warehouse_address'):
            raise serializers.ValidationError({
                "warehouse_address": "Warehouse address required"
            })

        # ✅ NAME VALIDATION
        data = self.validate_name_fields(data)

        # ✅ NUMBER VALIDATION (ADDED)
        data = self.validate_positive_number_fields(data)

        return data

    # ==============================
    # ✅ CLEAN EMPTY VALUES
    # ==============================
    def clean_empty_to_none(self, validated_data):
        unique_fields = [
            'aadhaar_number',
            'pan_number',
            'gst_number',
            'account_number'
        ]

        for field in unique_fields:
            if validated_data.get(field) in ["", None]:
                validated_data[field] = None

        return validated_data

    # ==============================
    # ✅ CREATE / UPDATE
    # ==============================
    def create(self, validated_data):
        validated_data = self.clean_empty_to_none(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self.clean_empty_to_none(validated_data)
        return super().update(instance, validated_data)


class SerialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Serial
        fields = '__all__'

from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import DistributorInformation


# ---------------- CREATE DISTRIBUTOR ----------------
class DistributorCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = DistributorInformation
        fields = ["id", "email_id", "password", "status"]

    def create(self, validated_data):
        # HASH PASSWORD BEFORE SAVING
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)



from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import DistributorInformation


class DistributorLoginSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email_id = data.get("email_id")
        password = data.get("password")

        try:
            distributor = DistributorInformation.objects.get(email_id=email_id)
        except DistributorInformation.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        db_password = distributor.password

        # ✅ If password is hashed
        if db_password.startswith("pbkdf2"):
            if not check_password(password, db_password):
                raise serializers.ValidationError("Invalid email or password")
        else:
            # ✅ If password is still plain text (legacy users)
            if db_password != password:
                raise serializers.ValidationError("Invalid email or password")

            return distributor

        if not check_password(password, distributor.password):
            raise serializers.ValidationError("Invalid email or password")

        return distributor

from datetime import timedelta

from rest_framework import serializers
from datetime import timedelta
from rest_framework import serializers
from datetime import timedelta
from .models import Warranty
from rest_framework import serializers
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from dateutil.relativedelta import relativedelta

from rest_framework import serializers
from dateutil.relativedelta import relativedelta
from .models import Warranty


from rest_framework import serializers
from dateutil.relativedelta import relativedelta
from .models import Warranty


from rest_framework import serializers
from dateutil.relativedelta import relativedelta
from .models import Warranty, InventorySerial, Product, DistributorInformation, Admin

import re
from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from .models import Warranty, Product, InventorySerial, DistributorInformation, Admin

import re
from dateutil.relativedelta import relativedelta
from rest_framework import serializers

class WarrantySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
 
    serial_id = serializers.PrimaryKeyRelatedField(
        queryset=InventorySerial.objects.all(),
        required=False,
        allow_null=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    distributor_id = serializers.PrimaryKeyRelatedField(
        queryset=DistributorInformation.objects.all(),
        required=False,
        allow_null=True
    )
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Admin.objects.all(),
        required=False,
        allow_null=True
    )
 
    detailer_name = serializers.CharField(max_length=100)
    detailer_mobile = serializers.CharField(max_length=15)
    car_registration_number = serializers.CharField(max_length=20)
    car_brand = serializers.CharField(max_length=100)
    car_model = serializers.CharField(max_length=100)
 
    installation_date = serializers.DateField(required=False, allow_null=True)
    warranty_period = serializers.IntegerField(required=False, allow_null=True)
    warranty_start_date = serializers.DateField(required=False, allow_null=True)
    warranty_end_date = serializers.DateField(required=False, allow_null=True)
 
    warranty_status = serializers.ChoiceField(
        choices=Warranty.WARRANTY_STATUS,
        required=False
    )
    product_status = serializers.ChoiceField(
        choices=Warranty.PRODUCT_STATUS,
        required=False
    )
 
    rejection_reason = serializers.CharField(required=False, allow_blank=True)
    invoice_image = serializers.ImageField(required=False, allow_null=True, use_url=False)
    registered_by = serializers.CharField(required=False, allow_null=True)
 
    car_images = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        required=False
    )
    installation_images = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        required=False
    )
 
    serial_number = serializers.CharField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    approved_by_name = serializers.CharField(read_only=True)
 
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    generate_bill = serializers.BooleanField(required=False)
 
    license_plate_no = serializers.CharField(max_length=100,required=False,allow_blank=True,allow_null=True)
 
    color = serializers.CharField(max_length=100,required=False,allow_blank=True,allow_null=True)
 
    address = serializers.CharField(required=False,allow_blank=True,allow_null=True)
 
    owner_name = serializers.CharField(max_length=100,required=False,allow_blank=True,allow_null=True)
 
    owner_email = serializers.EmailField(max_length=100,required=False,allow_blank=True,allow_null=True)
 
    owner_mobile = serializers.CharField(max_length=100,required=False,allow_blank=True,allow_null=True)
 
    email = serializers.EmailField(required=False,allow_blank=True,allow_null=True)
    signature_img = serializers.ImageField(
        required=False, allow_null=True, use_url=False
    )
    hold_reason = serializers.CharField(required=False, allow_blank=True, allow_null=True)
 
    def validate(self, attrs):
        request = self.context.get("request")
 
        detailer_name = attrs.get("detailer_name")
        if detailer_name is not None:
            if not re.match(r'^[A-Za-z ]+$', detailer_name):
                raise serializers.ValidationError({
                    "detailer_name": "Only alphabets and spaces are allowed."
                })
 
        # POST validation
        if request and request.method == "POST":
            if attrs.get("installation_date") is None:
                raise serializers.ValidationError({
                    "installation_date": "Installation date is required."
                })
 
        # PATCH / PUT validation for status change
        if request and request.method in ["PATCH", "PUT"]:
            status_changing = (
                "product_status" in attrs or
                "warranty_status" in attrs
            )
 
            if status_changing:
                instance = getattr(self, "instance", None)
 
                approved_from_request = attrs.get("approved_by", None)
                approved_existing = instance.approved_by if instance else None
 
                final_approved = approved_from_request if approved_from_request is not None else approved_existing
 
                if not final_approved:
                    raise serializers.ValidationError({
                        "approved_by": "approved_by is required before changing product or warranty status."
                    })
 
        return attrs
 
    def create(self, validated_data):
 
        start_date = validated_data.get("installation_date")
        validated_data["warranty_start_date"] = None
        validated_data["warranty_end_date"] = None
        warranty_status = validated_data.get("warranty_status")
        product_status = validated_data.get("product_status")
        # Calculate only when ACTIVE / ACTIVATED
        if (
            warranty_status == "ACTIVE" or
            product_status == "ACTIVATED"
        ):
            years = validated_data.get("warranty_period", 0)
            validated_data["warranty_start_date"] = start_date
            validated_data["warranty_end_date"] = (
                start_date + relativedelta(years=years)
                if start_date else None
            )
        # Default statuses
        if "warranty_status" not in validated_data:
            validated_data["warranty_status"] = "PENDING"
        if "product_status" not in validated_data:
            validated_data["product_status"] = "PENDING"
        return Warranty.objects.create(**validated_data)
 
    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        warranty_status = instance.warranty_status
        product_status = instance.product_status

        if (
            warranty_status == "ACTIVE" or
            product_status == "ACTIVATED"
        ):
            years = instance.warranty_period or 0

            instance.warranty_start_date = instance.installation_date

            if instance.installation_date:
                instance.warranty_end_date = (
                    instance.installation_date +
                    relativedelta(years=years)
                )
        else:
            instance.warranty_start_date = None
            instance.warranty_end_date = None

        instance.save()
        return instance
    def to_representation(self, instance):
        data = super().to_representation(instance)
 
        data["invoice_image"] = (
            f"/media/{instance.invoice_image.name}"
            if instance.invoice_image else None
        )
 
        data["car_images"] = [
            f"/media/{img}"
            for img in (getattr(instance, "car_images", []) or [])
        ]
 
        data["installation_images"] = [
            f"/media/{img}"
            for img in (getattr(instance, "installation_images", []) or [])
        ]
 
        data["serial_number"] = (
            instance.serial_id.serial_number
            if instance.serial_id else None
        )
 
        data["product_name"] = (
            instance.product_id.product_name
            if instance.product_id else None
        )
 
        data["approved_by_name"] = (
            getattr(instance.approved_by, "name", None)
            or getattr(instance.approved_by, "username", None)
            or getattr(instance.approved_by, "email", None)
        )
        return data


class EmployeeSalarySerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    employee_name = serializers.SerializerMethodField()

    basic_salary = serializers.FloatField()
    alloances = serializers.FloatField(default=0)
    deductions = serializers.FloatField(default=0)

    gross_salary = serializers.FloatField(read_only=True)
    effective_from = serializers.DateField()
    status = serializers.BooleanField(default=True)

    def get_employee_name(self, obj):
        if obj.employee_id:
            return f"{obj.employee_id.first_name} {obj.employee_id.last_name}"
        return None

    # ✅ CREATE
    def create(self, validated_data):
        basic = validated_data.get("basic_salary", 0)
        allo = validated_data.get("alloances", 0)
        deduct = validated_data.get("deductions", 0)

        # 🔥 AUTO CALCULATION
        gross = basic + allo - deduct

        validated_data["gross_salary"] = gross

        return EmployeeSalary.objects.create(**validated_data)

    # ✅ UPDATE
    def update(self, instance, validated_data):
        instance.basic_salary = validated_data.get("basic_salary", instance.basic_salary)
        instance.alloances = validated_data.get("alloances", instance.alloances)
        instance.deductions = validated_data.get("deductions", instance.deductions)
        instance.employee_id = validated_data.get("employee_id", instance.employee_id)
        instance.effective_from = validated_data.get("effective_from", instance.effective_from)
        instance.status = validated_data.get("status", instance.status)

        # 🔥 AUTO RECALCULATION
        instance.gross_salary = (
            instance.basic_salary +
            instance.alloances -
            instance.deductions
        )

        instance.save()
        return instance



class EmployeePersonalDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    employee_id = serializers.PrimaryKeyRelatedField(
    queryset=Employee.objects.all(),
    required=True,
    allow_null=False,
    error_messages={
        'required': 'Employee ID is required.',
        'null': 'Employee ID is required.',
        'does_not_exist': 'Invalid Employee ID.',
        'incorrect_type': 'Employee ID must be a number.'
    }
    )

    father_name = serializers.CharField(max_length=100, allow_blank=True, required=False)
    mother_name = serializers.CharField(max_length=100, allow_blank=True, required=False)

    marital_status = serializers.ChoiceField(
        choices=[('single', 'Single'), ('married', 'Married')],
        default='single',
        required=False
    )

    spouse_name = serializers.CharField(max_length=100, allow_blank=True, required=False)
    address = serializers.CharField(max_length=200, allow_blank=True, required=False)
    emergency_contact_name = serializers.CharField(max_length=100, allow_blank=True, required=False)
    emergency_contact_phone = serializers.CharField(required=False, allow_null=True)

    # ✅ VALIDATION FOR UNIQUE EMPLOYEE
    def validate_employee_id(self, value):
        if Employee_personal_details.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee ID already exists.")
        return value

    def validate_emergency_contact_phone(self, value):
        if value is None or value == "":
            return value

        if not value.isdigit():
            raise serializers.ValidationError("Emergency contact phone must contain only digits.")

        return value

    # Create new record
    def create(self, validated_data):
        return Employee_personal_details.objects.create(**validated_data)

    # Update existing record
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class EmployeeDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeDocuments
        fields = "__all__"

    # ✅ Unique employee validation
    def validate_employee_id(self, employee_id):
        instance = getattr(self, 'instance', None)

        if instance:
            if EmployeeDocuments.objects.exclude(id=instance.id).filter(employee_id=employee_id).exists():
                raise serializers.ValidationError("Documents already exist for this employee")
        else:
            if EmployeeDocuments.objects.filter(employee_id=employee_id).exists():
                raise serializers.ValidationError("Documents already exist for this employee")

        return employee_id

    # ✅ PAN Card Validation
    def validate_pancard_number(self, value):
        if value:
            value = value.upper()  # ensure uppercase
            if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', value):
                raise serializers.ValidationError(
                    "Invalid PAN format. Example: ABCDE1234F"
                )
        return value

    # ✅ Aadhaar Validation
    def validate_aadhar_number(self, value):
        if value:
            if not re.match(r'^\d{12}$', value):
                raise serializers.ValidationError(
                    "Aadhaar must be exactly 12 digits"
                )
        return value

    # ✅ Driving License Validation
    def validate_driving_license_number(self, value):
        if value:
            if not re.match(r'^[A-Z]{2}[0-9]{2}[0-9]{4}[0-9]{7}$', value):
                raise serializers.ValidationError(
                    "Invalid Driving License format. Example: GJ0120210001234"
                )
        return value

    # ✅ Make all images required on CREATE
    def validate(self, attrs):

        image_fields = [
            "aadhar_front",
            "aadhar_back",
            "pan_card",
            "photo",
            "driving_license_front",
            "driving_license_back",
        ]

        if not self.instance:  # only during create
            for field in image_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError({
                        field: "This image field is required."
                    })

        return attrs

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    password = serializers.CharField(max_length=255, write_only=True)
    is_active = serializers.BooleanField(default=True)
    role = serializers.CharField(max_length=50,allow_blank=True, required=False)
    role_id = serializers.SerializerMethodField()

    # -------------------
    # Validation
    # -------------------
    def validate_username(self, value):
        # When creating new user
        if self.instance is None:
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError("Username already registered")
        else:
            # When updating existing user, ignore current instance
            if User.objects.filter(username=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Username already registered")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long")
        return make_password(value)  # automatically hash password

    # -------------------
    # Create & Update
    # -------------------
    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_role_id(self, obj):
        return obj.employee_id.role_id.id if obj.employee_id and obj.employee_id.role_id else None


class InventorySerialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.ChoiceField(
        choices=["IN_STOCK", "RESERVED", "PICKED", "PACKED", "DELIVERED","STOCK_OUT"]
    )
    product_id = serializers.PrimaryKeyRelatedField(read_only=True)
    serial_number = serializers.CharField(read_only=True)
    batch_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # Add location and warehouse
    location = serializers.SerializerMethodField(read_only=True)
    warehouse = serializers.SerializerMethodField(read_only=True)
    sku=serializers.SerializerMethodField(read_only=True)
    barcode_image = serializers.ImageField(read_only=True)
    product_name = serializers.SerializerMethodField(read_only=True)  # ✅ added
    def get_product_name(self, obj):
        if obj.product_id:
            return obj.product_id.product_name
        return None
    def get_sku(self, obj):
        if obj.product_id:
            return obj.product_id.sku
        return None

    def get_location(self, obj):
        if obj.location:
            return {"id": obj.location.id, "name": obj.location.name}

        # get location from shipment product fallback
        shipment_products = Shipment_product.objects.filter(
            product_id=obj.product_id, batch_data=obj.batch_id
        )
        if shipment_products.exists():
            first = shipment_products.first()
            if first.location_id:
                return {"id": first.location_id.id, "name": first.location_id.name}
        return None

    def get_warehouse(self, obj):
        if obj.warehouse:
            return {"id": obj.warehouse.id, "name": obj.warehouse.name}

        # get warehouse from shipment product fallback
        shipment_products = Shipment_product.objects.filter(
            product_id=obj.product_id, batch_data=obj.batch_id
        )
        if shipment_products.exists():
            first = shipment_products.first()
            if first.warehouse_id:
                return {"id": first.warehouse_id.id, "name": first.warehouse_id.name}
        return None

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

    def create(self, validated_data):
        raise serializers.ValidationError("Direct creation is not allowed.")


class InventorySerialHistorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    # Matching InventorySerial response format
    sku = serializers.SerializerMethodField(read_only=True)
    location = serializers.SerializerMethodField(read_only=True)
    warehouse = serializers.SerializerMethodField(read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)

    class Meta:
        model = InventorySerialHistory
        fields = '__all__'

    def get_sku(self, obj):
        if obj.product:
            return obj.product.sku
        return None

    def get_location(self, obj):
        if obj.location:
            return {"id": obj.location.id, "name": obj.location.name}
        return None

    def get_warehouse(self, obj):
        if obj.warehouse:
            return {"id": obj.warehouse.id, "name": obj.warehouse.name}
        return None

    def create(self, validated_data):
        raise serializers.ValidationError("Direct creation is not allowed.")



from django.utils import timezone
from decimal import Decimal
from datetime import time
from rest_framework import serializers
from decimal import Decimal
from datetime import time
from django.utils import timezone
from .models import Expenses_login, Employee
from datetime import time, datetime as dt_cls



class ExpensesLoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )
    employee_name = serializers.CharField(source="employee.first_name", read_only=True)
    start_time = serializers.DateTimeField(required=True, allow_null=True)
    end_time = serializers.DateTimeField(required=False, allow_null=True)
    date = serializers.DateField(required=False)

    status = serializers.BooleanField(required=False)
    full_leave = serializers.BooleanField(read_only=True)
    half_leave = serializers.BooleanField(read_only=True)

    total_hours = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    OFFICE_START = time(9, 0, 0)

    def validate(self, attrs):
        start_time = attrs.get("start_time", getattr(self.instance, "start_time", None))
        end_time = attrs.get("end_time", getattr(self.instance, "end_time", None))
        employee = attrs.get("employee", getattr(self.instance, "employee", None))
        attendance_date = attrs.get("date", getattr(self.instance, "date", None))

        if not attendance_date and start_time:
            attendance_date = start_time.date()

        if start_time and end_time and end_time < start_time:
            raise serializers.ValidationError({
                "end_time": "End time cannot be earlier than start time."
            })

        if employee and attendance_date:
            qs = Expenses_login.objects.filter(
                employee=employee,
                date=attendance_date
            )
            if self.instance:
                qs = qs.exclude(id=self.instance.id)

            if qs.exists():
                raise serializers.ValidationError({
                    "error": "Attendance already marked for this date."
                })

        return attrs

    def _get_expected_start(self, attendance_date, start_time):
        expected = dt_cls.combine(attendance_date, self.OFFICE_START)
        if start_time and start_time.tzinfo is not None:
            expected = timezone.make_aware(expected, timezone.get_current_timezone())
        return expected

    def _get_delay_seconds(self, attendance_date, start_time):
        if not attendance_date or not start_time:
            return 0
        expected = self._get_expected_start(attendance_date, start_time)
        return (start_time - expected).total_seconds()

    def _get_previous_month_records(self, employee, attendance_date, exclude_id=None):
        qs = Expenses_login.objects.filter(
            employee=employee,
            date__year=attendance_date.year,
            date__month=attendance_date.month,
            date__lt=attendance_date
        )
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        return qs

    def _count_minor_lates_before_today(self, employee, attendance_date, exclude_id=None):
        qs = self._get_previous_month_records(employee, attendance_date, exclude_id).exclude(
            start_time__isnull=True
        )
        count = 0
        for rec in qs:
            delay = self._get_delay_seconds(rec.date, rec.start_time)
            if 60 <= delay <= 600:
                count += 1
        return count

    def _calculate_attendance(self, employee, attendance_date, start_time, end_time=None, exclude_id=None):
        result = {
            "status": False,
            "half_leave": False,
            "full_leave": False,
            "total_hours": Decimal("0.00")
        }

        if not start_time:
            return result

        delay_seconds = self._get_delay_seconds(attendance_date, start_time)

        is_minor_late = False
        allowed_minor_late = False
        minor_late_penalty = False

        # 1. Late rule
        if delay_seconds < 60:
            pass

        elif 60 <= delay_seconds <= 600:
            is_minor_late = True
            previous_minor_lates = self._count_minor_lates_before_today(
                employee=employee,
                attendance_date=attendance_date,
                exclude_id=exclude_id
            )

            # first 3 times allowed, 4th onward penalty
            if previous_minor_lates < 3:
                allowed_minor_late = True
            else:
                minor_late_penalty = True

        elif delay_seconds > 600:
            result["half_leave"] = True

        # 2. Hours rule
        if start_time and end_time:
            delta = end_time - start_time
            total_hours = round(delta.total_seconds() / 3600, 2)

            if total_hours < 0:
                raise serializers.ValidationError({
                    "end_time": "Total hours cannot be negative."
                })

            result["total_hours"] = Decimal(str(total_hours))
            result["status"] = True

            # FULL DAY
            if total_hours >= 8.9:
                result["full_leave"] = False

                # first 3 minor lates => no half leave
                if is_minor_late and allowed_minor_late:
                    result["half_leave"] = False

                # 4th minor late onward => half leave
                elif minor_late_penalty:
                    result["half_leave"] = True

                # more than 10 min late => half leave
                elif delay_seconds > 600:
                    result["half_leave"] = True

                else:
                    result["half_leave"] = False

            # HALF DAY
            elif 4.5 <= total_hours < 8.9:
                result["half_leave"] = True
                result["full_leave"] = False

            # FULL LEAVE
            else:
                result["full_leave"] = True
                result["half_leave"] = False

        if result["full_leave"]:
            result["half_leave"] = False

        return result


    def create(self, validated_data):
        validated_data["status"] = validated_data.get("status", False)

        employee = validated_data.get("employee")
        start_time = validated_data.get("start_time")
        end_time = validated_data.get("end_time")
        attendance_date = validated_data.get("date")

        if not attendance_date and start_time:
            attendance_date = start_time.date()
            validated_data["date"] = attendance_date

        flags = self._calculate_attendance(
            employee=employee,
            attendance_date=attendance_date,
            start_time=start_time,
            end_time=end_time,
            exclude_id=None
        )

        validated_data["status"] = flags["status"]
        validated_data["half_leave"] = flags["half_leave"]
        validated_data["full_leave"] = flags["full_leave"]
        validated_data["total_hours"] = flags["total_hours"]

        return Expenses_login.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.employee = validated_data.get("employee", instance.employee)
        instance.start_time = validated_data.get("start_time", instance.start_time)
        instance.end_time = validated_data.get("end_time", instance.end_time)
        instance.date = validated_data.get("date", instance.date)

        if not instance.date and instance.start_time:
            instance.date = instance.start_time.date()

        flags = self._calculate_attendance(
            employee=instance.employee,
            attendance_date=instance.date,
            start_time=instance.start_time,
            end_time=instance.end_time,
            exclude_id=instance.id
        )

        instance.status = flags["status"]
        instance.half_leave = flags["half_leave"]
        instance.full_leave = flags["full_leave"]
        instance.total_hours = flags["total_hours"]

        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "employee": instance.employee.id if instance.employee else None,
             "employee_name": (
                f"{instance.employee.first_name} {instance.employee.last_name}"
                if instance.employee else None
            ),

            "start_time": instance.start_time,
            "end_time": instance.end_time,
            "date": instance.date,
            "status": instance.status,
            "full_leave": instance.full_leave,
            "half_leave": instance.half_leave,
            "total_hours": str(
                instance.total_hours if instance.total_hours is not None else Decimal("0.00")
            )
        }





from decimal import Decimal


from django.db import transaction
from rest_framework import serializers

from .models import PurchaseOrder, InventorySerial

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from .models import PurchaseOrder, Product, InventorySerial

from rest_framework import serializers
from django.db import transaction
from django.utils import timezone

from .models import (
    PurchaseOrder,
    Product,
    InventorySerial,
    DistributerOrders
)


from rest_framework import serializers
from django.db import transaction
from django.utils import timezone

from .models import (
    PurchaseOrder,
    Product,
    InventorySerial,
    DistributerOrders
)




# from rest_framework import serializers
# from django.db import transaction


# class PurchaseOrderSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     po_number = serializers.CharField(max_length=50)
#     po_date = serializers.DateTimeField(read_only=True)

#     distributor_id = serializers.PrimaryKeyRelatedField(
#         queryset=DistributorInformation.objects.all()
#     )

#     product_items = serializers.JSONField()
#     total_items = serializers.IntegerField(required=False)
#     total_quantity = serializers.IntegerField(required=False)

#     remarks = serializers.CharField(required=False, allow_null=True, allow_blank=True)
#     status = serializers.CharField(required=False)

#     created_by = serializers.PrimaryKeyRelatedField(
#         queryset=DistributorInformation.objects.all(),
#         required=False,
#         allow_null=True
#     )

#     approved_by = serializers.PrimaryKeyRelatedField(
#         queryset=Admin.objects.all(),
#         required=False,
#         allow_null=True
#     )

#     approved_at = serializers.DateTimeField(required=False, allow_null=True)

#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     unit_distributor_price = serializers.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         required=False
#     )
#     total_distributor_price = serializers.DecimalField(
#         max_digits=15,
#         decimal_places=2,
#         required=False
#     )

#     qty_picked = serializers.IntegerField(required=False)

#     def validate_total_quantity(self, value):

#         if value is not None:
#             try:
#                 value = int(value)
#             except (TypeError, ValueError):
#                 raise serializers.ValidationError("Only numeric values are allowed")

#             if value < 0:
#                 raise serializers.ValidationError("Only positive numbers or 0 are allowed")

#         return value


#     def to_representation(self, instance):
#         company_obj = CompanyProfile.objects.first()

#         data = {
#             "id": instance.id,
#             "po_number": instance.po_number,
#             "po_date": instance.po_date,
#             "distributor_id": instance.distributor_id.id if instance.distributor_id else None,
#             "remarks": instance.remarks,
#             "status": instance.status,
#             "created_by": instance.created_by.id if instance.created_by else None,
#             "approved_by": instance.approved_by.id if instance.approved_by else None,
#             "approved_at": instance.approved_at,
#             "created_at": instance.created_at,
#             "updated_at": instance.updated_at,
#             "total_items": instance.total_items,
#             "total_quantity": instance.total_quantity,
#             "qty_picked": instance.qty_picked,
#             "company_name": company_obj.company_name if company_obj else None,
#             "region": (
#                 instance.distributor_id.region.name
#                 if instance.distributor_id and instance.distributor_id.region
#                 else None
#             ),
#         }

#         formatted_items = []
#         distributor_price = 0.0

#         for item in instance.product_items or []:
#             if not isinstance(item, dict):
#                 continue

#             qty = int(item.get("quantity", 0) or 0)
#             picked = int(item.get("qty_picked", 0) or 0)
#             mrp = float(item.get("mrp", 0) or 0)
#             unit_price = float(item.get("unit_distributor_price", 0) or 0)
#             product_id = item.get("product_id")

#             hsn_code = ""
#             if product_id:
#                 try:
#                     product = Product.objects.get(id=product_id)
#                     hsn_code = product.hsn_code or ""
#                 except Product.DoesNotExist:
#                     pass

#             stock_available = InventorySerial.objects.filter(
#                 product_id_id=product_id,
#                 status="IN_STOCK"
#             ).count()

#             total_distributor_price = qty * unit_price
#             distributor_price += total_distributor_price

#             formatted_items.append({
#                 "product_id": product_id,
#                 "product_name": item.get("product_name"),
#                 "stock_available": stock_available,
#                 "quantity": qty,
#                 "qty_picked": picked,
#                 "short_pick": qty - picked,
#                 "remarks": item.get("remarks", ""),
#                 "mrp": mrp,
#                 "unit_distributor_price": unit_price,
#                 "total_price": qty * mrp,
#                 "total_distributor_price": total_distributor_price,
#                 "hsn_code": hsn_code,
#                 "cartons": item.get("cartons", ""),
#                 "gross_weight": item.get("gross_weight", ""),
#                 "net_weight": item.get("net_weight", ""),
#             })

#         data["product_items"] = formatted_items
#         data["distributor_price"] = distributor_price
#         return data

#     def _generate_short_pick_po_number(self, parent_po_number):
#         base_po = parent_po_number

#         match = re.match(r"^(.*?)(?:-SP(\d+))?$", parent_po_number)
#         if match:
#             base_po = match.group(1)

#         existing_po_numbers = PurchaseOrder.objects.filter(
#             po_number__startswith=f"{base_po}-SP"
#         ).values_list("po_number", flat=True)

#         max_num = 0
#         for po_num in existing_po_numbers:
#             sp_match = re.match(rf"^{re.escape(base_po)}-SP(\d+)$", po_num)
#             if sp_match:
#                 num = int(sp_match.group(1))
#                 if num > max_num:
#                     max_num = num

#         return f"{base_po}-SP{max_num + 1}"

#     def _reserve_serials_for_po(self, po):
#         for item in po.product_items or []:
#             if not isinstance(item, dict):
#                 continue

#             prod_id = item.get("product_id")
#             ordered_qty = int(item.get("quantity", 0) or 0)

#             if ordered_qty <= 0:
#                 continue

#             already_reserved = DistributerOrders.objects.filter(
#                 purchase_order_id=po,
#                 inventory_serial_id__product_id_id=prod_id
#             ).count()

#             remaining_to_reserve = ordered_qty - already_reserved

#             if remaining_to_reserve <= 0:
#                 continue

#             try:
#                 product = Product.objects.get(id=prod_id)
#             except Product.DoesNotExist:
#                 continue

#             serials = InventorySerial.objects.filter(
#                 product_id=product,
#                 status="IN_STOCK"
#             ).order_by("id")[:remaining_to_reserve]

#             for serial in serials:
#                 serial.status = "RESERVED"
#                 serial.save(update_fields=["status"])

#                 DistributerOrders.objects.create(
#                     distributor_id=po.distributor_id,
#                     inventory_serial_id=serial,
#                     purchase_order_id=po
#                 )

#     def _create_short_pick_po(self, source_po, short_items):
#         if not short_items:
#             return None

#         total_items = len(short_items)
#         total_quantity = sum(
#             int(item.get("quantity", 0) or 0)
#             for item in short_items
#         )

#         new_po = PurchaseOrder.objects.create(
#             po_number=self._generate_short_pick_po_number(source_po.po_number),
#             distributor_id=source_po.distributor_id,
#             remarks=f"Auto-generated short pick PO from {source_po.po_number}",
#             status="SUBMITTED",
#             created_by=source_po.created_by,
#             approved_by=None,
#             approved_at=None,
#             product_items=short_items,
#             total_items=total_items,
#             total_quantity=total_quantity,
#             qty_picked=0,
#             po_date=timezone.now()
#         )

#         return new_po

#     @transaction.atomic
#     def create(self, validated_data):
#         items = validated_data.pop("product_items", [])

#         final_items = []
#         total_items = 0
#         total_quantity = 0
#         total_picked = 0

#         for item in items:
#             product_id = item.get("product_id")
#             quantity = int(item.get("quantity", 0) or 0)
#             picked = int(item.get("qty_picked", 0) or 0)

#             try:
#                 product = Product.objects.get(id=product_id)
#             except Product.DoesNotExist:
#                 continue

#             item_data = {
#                 "product_id": product.id,
#                 "product_name": product.product_name,
#                 "quantity": quantity,
#                 "qty_picked": picked,
#                 "mrp": float(product.mrp),
#                 "unit_distributor_price": float(item.get("unit_distributor_price", 0) or 0),
#                 "remarks": item.get("remarks", ""),
#                 "hsn_code": product.hsn_code or "",
#                 "cartons": item.get("cartons", ""),
#                 "gross_weight": item.get("gross_weight", ""),
#                 "net_weight": item.get("net_weight", ""),
#                 "short_pick_generated": False,
#             }

#             final_items.append(item_data)
#             total_items += 1
#             total_quantity += quantity
#             total_picked += picked

#         validated_data["product_items"] = final_items
#         validated_data["total_items"] = total_items
#         validated_data["total_quantity"] = total_quantity
#         validated_data["qty_picked"] = total_picked
#         validated_data["status"] = validated_data.get("status") or "DRAFT"

#         po = PurchaseOrder.objects.create(**validated_data)
#         return po

#     @transaction.atomic
#     def update(self, instance, validated_data):
#         old_status = instance.status
#         items = validated_data.get("product_items", None)
#         top_level_qty_picked = validated_data.get("qty_picked", None)
#         new_status = validated_data.get("status", old_status)

#         existing_items_map = {
#             item.get("product_id"): item
#             for item in (instance.product_items or [])
#             if isinstance(item, dict)
#         }

#         if old_status not in ["CANCELLED", "REJECTED"] and new_status in ["CANCELLED", "REJECTED"]:
#             reserved_serials = InventorySerial.objects.filter(
#                 orders__purchase_order_id=instance,
#                 status="RESERVED"
#             )
#             for serial in reserved_serials:
#                 serial.status = "IN_STOCK"
#                 serial.save()

#         if items is not None:
#             updated_items = []
#             total_it = 0
#             total_qy = 0
#             total_pk = 0

#             for item in items:
#                 product_id = item.get("product_id")
#                 original_item = existing_items_map.get(product_id, {})

#                 if "-SP" in str(instance.po_number) and original_item:
#                     qty = int(original_item.get("quantity", 0) or 0)
#                 else:
#                     qty = int(item.get("quantity", original_item.get("quantity", 0)) or 0)

#                 picked = int(item.get("qty_picked", original_item.get("qty_picked", 0)) or 0)

#                 if picked > qty:
#                     picked = qty

#                 product = Product.objects.get(id=product_id)

#                 item_data = {
#                     "product_id": product.id,
#                     "product_name": product.product_name,
#                     "quantity": qty,
#                     "qty_picked": picked,
#                     "mrp": float(product.mrp),
#                     "unit_distributor_price": float(
#                         item.get(
#                             "unit_distributor_price",
#                             original_item.get("unit_distributor_price", 0)
#                         ) or 0
#                     ),
#                     "remarks": item.get("remarks", original_item.get("remarks", "")),
#                     "hsn_code": product.hsn_code or "",
#                     "cartons": item.get("cartons", original_item.get("cartons", "")),
#                     "gross_weight": item.get("gross_weight", original_item.get("gross_weight", "")),
#                     "net_weight": item.get("net_weight", original_item.get("net_weight", "")),
#                     "short_pick_generated": original_item.get("short_pick_generated", False),
#                 }

#                 updated_items.append(item_data)
#                 total_it += 1
#                 total_qy += qty
#                 total_pk += picked

#             instance.product_items = updated_items
#             instance.total_items = total_it
#             instance.total_quantity = total_qy
#             instance.qty_picked = total_pk

#         elif top_level_qty_picked is not None:
#             current_items = instance.product_items or []
#             updated_items = []

#             rem_to_pick = int(top_level_qty_picked or 0)
#             total_qy = 0
#             total_it = 0
#             total_pk = 0

#             for item in current_items:
#                 qy = int(item.get("quantity", 0) or 0)
#                 it_pk = qy if rem_to_pick >= qy else rem_to_pick
#                 rem_to_pick = max(0, rem_to_pick - qy)

#                 item["qty_picked"] = it_pk
#                 item["short_pick_generated"] = item.get("short_pick_generated", False)

#                 updated_items.append(item)

#                 total_it += 1
#                 total_qy += qy
#                 total_pk += it_pk

#             instance.product_items = updated_items
#             instance.total_items = total_it
#             instance.total_quantity = total_qy
#             instance.qty_picked = total_pk

#         if new_status == "PICKED" and instance.total_quantity == 0 and instance.product_items:
#             instance.total_quantity = sum(
#                 int(item.get("quantity", 0) or 0)
#                 for item in instance.product_items
#             )

#         for attr, value in validated_data.items():
#             if attr not in ["product_items", "qty_picked", "total_items", "total_quantity"]:
#                 setattr(instance, attr, value)

#         should_create_short_pick_po = (
#             new_status == "PICKED"
#             and (items is not None or top_level_qty_picked is not None or old_status != "PICKED")
#         )

#         short_pick_items = []
#         refreshed_items = []

#         for item in (instance.product_items or []):
#             product_id = item.get("product_id")
#             qty = int(item.get("quantity", 0) or 0)
#             picked = int(item.get("qty_picked", 0) or 0)
#             already_generated = item.get("short_pick_generated", False)

#             short_pick_qty = qty - picked

#             if (
#                 should_create_short_pick_po
#                 and picked > 0
#                 and short_pick_qty > 0
#                 and not already_generated
#             ):
#                 short_item = {
#                     "product_id": product_id,
#                     "product_name": item.get("product_name"),
#                     "quantity": short_pick_qty,
#                     "qty_picked": 0,
#                     "mrp": float(item.get("mrp", 0) or 0),
#                     "unit_distributor_price": float(item.get("unit_distributor_price", 0) or 0),
#                     "remarks": item.get("remarks", ""),
#                     "hsn_code": item.get("hsn_code", ""),
#                     "cartons": item.get("cartons", ""),
#                     "gross_weight": item.get("gross_weight", ""),
#                     "net_weight": item.get("net_weight", ""),
#                     "short_pick_generated": False,
#                 }

#                 short_pick_items.append(short_item)
#                 item["short_pick_generated"] = True

#             refreshed_items.append(item)

#         instance.product_items = refreshed_items

#         if new_status == "APPROVED":
#             self._reserve_serials_for_po(instance)

#         elif new_status in ["PICKED", "PACKED", "DELIVERED"]:
#             if new_status == "PICKED":
#                 self._reserve_serials_for_po(instance)

#             order_serials = InventorySerial.objects.filter(
#                 orders__purchase_order_id=instance
#             )

#             for serial in order_serials:
#                 serial.status = new_status
#                 serial.save()

#         instance.save()

#         if should_create_short_pick_po and short_pick_items:
#             self._create_short_pick_po(instance, short_pick_items)

#         return instance


class PurchaseOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    po_number = serializers.CharField(max_length=50)
    po_date = serializers.DateTimeField(read_only=True)

    product_items = serializers.JSONField()
    total_items = serializers.IntegerField(required=False)
    total_quantity = serializers.IntegerField(required=False)

    remarks = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.CharField(required=False)

    created_by = serializers.PrimaryKeyRelatedField(
        queryset=DistributorInformation.objects.all(),
        required=False,
        allow_null=True
    )

    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Admin.objects.all(),
        required=False,
        allow_null=True
    )
    company_id = serializers.PrimaryKeyRelatedField(
    queryset=CompanyProfile.objects.all(),
    required=False,
    allow_null=True
    )

    approved_at = serializers.DateTimeField(required=False, allow_null=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    unit_distributor_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False
    )

    total_distributor_price = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        required=False
    )

    qty_picked = serializers.IntegerField(required=False)

    distributor_id = serializers.PrimaryKeyRelatedField(
        queryset=DistributorInformation.objects.all(),
        required=False,
        allow_null=True
    )

    distributor_name = serializers.SerializerMethodField()

    def get_distributor_name(self, obj):
        if obj.distributor_id:
            return obj.distributor_id.distributor_name
        return None

    def validate_po_number(self, value):
        if self.instance is None:
            if PurchaseOrder.objects.filter(po_number=value).exists():
                raise serializers.ValidationError(
                    "A purchase order with this number already exists."
                )
        else:
            if PurchaseOrder.objects.filter(po_number=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "A purchase order with this number already exists."
                )
        return value

    def _get_company_obj(self, instance):
        """
        Correct company fetch:
        First try distributor's company.
        Fallback to first company only if distributor company not available.
        """

        distributor = instance.distributor_id

        if distributor:
            # Case 1: FK field name company_id
            if hasattr(distributor, "company_id") and distributor.company_id:
                try:
                    if hasattr(distributor, "company"):
                        return distributor.company
                except Exception:
                    pass

                try:
                    return CompanyProfile.objects.filter(id=distributor.company_id).first()
                except Exception:
                    pass

            # Case 2: FK field name company
            if hasattr(distributor, "company") and distributor.company:
                return distributor.company

            # Case 3: FK field name company_profile
            if hasattr(distributor, "company_profile") and distributor.company_profile:
                return distributor.company_profile

        return CompanyProfile.objects.first()

    def to_representation(self, instance):
        company_obj = instance.company_id

        data = {
            "id": instance.id,
            "po_number": instance.po_number,
            "po_date": instance.po_date,
            "distributor_id": instance.distributor_id.id if instance.distributor_id else None,
            "distributor_name": (
                instance.distributor_id.distributor_name
                if instance.distributor_id
                else None
            ),
            "remarks": instance.remarks,
            "status": instance.status,
            "created_by": instance.created_by.id if instance.created_by else None,
            "approved_by": instance.approved_by.id if instance.approved_by else None,
            "approved_at": instance.approved_at,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "total_items": instance.total_items,
            "total_quantity": instance.total_quantity,
            "qty_picked": instance.qty_picked,

            "company_id": company_obj.id if company_obj else None,
            "company_name": company_obj.company_name if company_obj else None,

            "region": (
                str(instance.distributor_id.region_id)
                if instance.distributor_id and instance.distributor_id.region_id
                else None
            ),
        }

        formatted_items = []
        distributor_price = 0.0

        for item in instance.product_items or []:
            if not isinstance(item, dict):
                continue

            qty = int(item.get("quantity", 0) or 0)
            picked = int(item.get("qty_picked", 0) or 0)
            mrp = float(item.get("mrp", 0) or 0)
            unit_price = float(item.get("unit_distributor_price", 0) or 0)
            product_id = item.get("product_id")

            hsn_code = ""
            if product_id:
                try:
                    product = Product.objects.get(id=product_id)
                    hsn_code = product.hsn_code or ""
                except Product.DoesNotExist:
                    pass

            stock_available = InventorySerial.objects.filter(
                product_id_id=product_id,
                status="IN_STOCK"
            ).count()

            total_distributor_price = qty * unit_price
            distributor_price += total_distributor_price

            formatted_items.append({
                "product_id": product_id,
                "product_name": item.get("product_name"),
                "stock_available": stock_available,
                "quantity": qty,
                "qty_picked": picked,
                "short_pick": qty - picked,
                "remarks": item.get("remarks", ""),
                "mrp": mrp,
                "unit_distributor_price": unit_price,
                "total_price": qty * mrp,
                "total_distributor_price": total_distributor_price,
                "hsn_code": hsn_code,
                "cartons": item.get("cartons", ""),
                "gross_weight": item.get("gross_weight", ""),
                "net_weight": item.get("net_weight", ""),
            })

        data["product_items"] = formatted_items
        data["distributor_price"] = distributor_price
        return data

    def _generate_short_pick_po_number(self, parent_po_number):
        base_po = parent_po_number

        match = re.match(r"^(.*?)(?:-SP(\d+))?$", parent_po_number)
        if match:
            base_po = match.group(1)

        existing_po_numbers = PurchaseOrder.objects.filter(
            po_number__startswith=f"{base_po}-SP"
        ).values_list("po_number", flat=True)

        max_num = 0
        for po_num in existing_po_numbers:
            sp_match = re.match(rf"^{re.escape(base_po)}-SP(\d+)$", po_num)
            if sp_match:
                num = int(sp_match.group(1))
                if num > max_num:
                    max_num = num

        return f"{base_po}-SP{max_num + 1}"

    def _reserve_serials_for_po(self, po):
        short_items = []

        for item in po.product_items or []:
            if not isinstance(item, dict):
                continue

            prod_id = item.get("product_id")
            ordered_qty = int(item.get("quantity", 0) or 0)

            if ordered_qty <= 0:
                continue

            already_reserved = DistributerOrders.objects.filter(
                purchase_order_id=po,
                inventory_serial_id__product_id_id=prod_id
            ).count()

            remaining_to_reserve = ordered_qty - already_reserved

            if remaining_to_reserve <= 0:
                continue

            try:
                product = Product.objects.get(id=prod_id)
            except Product.DoesNotExist:
                continue

            serials = list(
                InventorySerial.objects.select_for_update().filter(
                    product_id=product,
                    status="IN_STOCK"
                ).order_by("?")[:remaining_to_reserve]
            )

            for serial in serials:
                serial.status = "RESERVED"
                serial.save(update_fields=["status"])

                DistributerOrders.objects.create(
                    distributor_id=po.distributor_id,
                    inventory_serial_id=serial,
                    purchase_order_id=po
                )

            shortage_qty = remaining_to_reserve - len(serials)

            if shortage_qty > 0:
                item["quantity"] = ordered_qty - shortage_qty
                short_items.append({
                    "product_id": prod_id,
                    "product_name": item.get("product_name"),
                    "quantity": shortage_qty,
                    "qty_picked": 0,
                    "mrp": float(item.get("mrp", 0) or 0),
                    "unit_distributor_price": float(item.get("unit_distributor_price", 0) or 0),
                    "remarks": "Auto split from APPROVED shortage",
                    "hsn_code": item.get("hsn_code", ""),
                    "cartons": item.get("cartons", ""),
                    "gross_weight": item.get("gross_weight", ""),
                    "net_weight": item.get("net_weight", ""),
                    "short_pick_generated": False,
                })

        return short_items

    def _create_short_pick_po(self, source_po, short_items, status="SUBMITTED", remarks=None):
        if not short_items:
            return None

        total_items = len(short_items)
        total_quantity = sum(int(item.get("quantity", 0) or 0) for item in short_items)

        new_po = PurchaseOrder.objects.create(
            po_number=self._generate_short_pick_po_number(source_po.po_number),
            distributor_id=source_po.distributor_id,
            remarks=remarks or f"Auto-generated short pick PO from {source_po.po_number}",
            status=status,
            created_by=source_po.created_by,
            approved_by=None,
            approved_at=None,
            product_items=short_items,
            total_items=total_items,
            total_quantity=total_quantity,
            qty_picked=0,
            po_date=timezone.now()
        )

        return new_po

    def _mark_picked_and_stockout(self, po):
        stockout_items = []

        for item in po.product_items or []:
            if not isinstance(item, dict):
                continue

            prod_id = item.get("product_id")

            reserved_serials = list(
                InventorySerial.objects.select_for_update().filter(
                    orders__purchase_order_id=po,
                    product_id_id=prod_id,
                    status="RESERVED"
                ).distinct().order_by("?")
            )

            actual_reserved_qty = len(reserved_serials)
            picked = int(item.get("qty_picked", 0) or 0)

            if picked > actual_reserved_qty:
                picked = actual_reserved_qty

            remaining_stockout_qty = actual_reserved_qty - picked

            picked_serials = reserved_serials[:picked]
            stockout_serials = reserved_serials[picked:picked + remaining_stockout_qty]

            for serial in picked_serials:
                serial.status = "PICKED"
                serial.save(update_fields=["status"])

            for serial in stockout_serials:
                serial.status = "STOCK_OUT"
                serial.save(update_fields=["status"])

            if remaining_stockout_qty > 0 and not item.get("stockout_split_generated", False):
                item["quantity"] = picked
                item["qty_picked"] = picked

                stockout_items.append({
                    "product_id": prod_id,
                    "product_name": item.get("product_name"),
                    "quantity": remaining_stockout_qty,
                    "qty_picked": 0,
                    "mrp": float(item.get("mrp", 0) or 0),
                    "unit_distributor_price": float(item.get("unit_distributor_price", 0) or 0),
                    "remarks": "Auto split from PICKED stockout",
                    "hsn_code": item.get("hsn_code", ""),
                    "cartons": item.get("cartons", ""),
                    "gross_weight": item.get("gross_weight", ""),
                    "net_weight": item.get("net_weight", ""),
                    "short_pick_generated": False,
                    "stockout_split_generated": False,
                })

                item["stockout_split_generated"] = True
            else:
                item["quantity"] = picked
                item["qty_picked"] = picked

        return stockout_items

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("product_items", [])

        final_items = []
        total_items = 0
        total_quantity = 0
        total_picked = 0
        total_dist_price = 0.0

        for item in items:
            product_id = item.get("product_id")
            quantity = int(item.get("quantity", 0) or 0)
            picked = int(item.get("qty_picked", 0) or 0)
            unit_price = float(item.get("unit_distributor_price", 0) or 0)

            try:
                product = Product.objects.get(id=product_id)
            except (Product.DoesNotExist, ValueError, TypeError):
                continue

            item_data = {
                "product_id": product.id,
                "product_name": product.product_name,
                "quantity": quantity,
                "qty_picked": picked,
                "mrp": float(product.mrp or 0),
                "unit_distributor_price": unit_price,
                "remarks": item.get("remarks", ""),
                "hsn_code": product.hsn_code or "",
                "cartons": item.get("cartons", ""),
                "gross_weight": item.get("gross_weight", ""),
                "net_weight": item.get("net_weight", ""),
                "short_pick_generated": False,
            }

            final_items.append(item_data)
            total_items += 1
            total_quantity += quantity
            total_picked += picked
            total_dist_price += quantity * unit_price

        validated_data["product_items"] = final_items
        validated_data["total_items"] = total_items
        validated_data["total_quantity"] = total_quantity
        validated_data["qty_picked"] = total_picked
        validated_data["total_distributor_price"] = total_dist_price
        validated_data["status"] = validated_data.get("status") or "DRAFT"

        po = PurchaseOrder.objects.create(**validated_data)
        return po

    @transaction.atomic
    def update(self, instance, validated_data):
        old_status = instance.status
        items = validated_data.get("product_items", None)
        top_level_qty_picked = validated_data.get("qty_picked", None)
        new_status = validated_data.get("status", old_status)

        existing_items_map = {
            str(item.get("product_id")): item
            for item in (instance.product_items or [])
            if isinstance(item, dict)
        }

        if old_status not in ["CANCELLED", "REJECTED"] and new_status in ["CANCELLED", "REJECTED"]:
            reserved_serials = InventorySerial.objects.filter(
                orders__purchase_order_id=instance,
                status="RESERVED"
            ).distinct()

            for serial in reserved_serials:
                serial.status = "IN_STOCK"
                serial.save(update_fields=["status"])

        if items is not None:
            updated_items = []
            total_it = 0
            total_qy = 0
            total_pk = 0

            for item in items:
                product_id = item.get("product_id")

                if not product_id:
                    continue

                original_item = existing_items_map.get(str(product_id), {})

                qty = int(item.get("quantity", original_item.get("quantity", 0)) or 0)
                picked = int(item.get("qty_picked", original_item.get("qty_picked", 0)) or 0)

                if picked > qty:
                    picked = qty

                try:
                    product = Product.objects.get(id=product_id)
                except (Product.DoesNotExist, ValueError, TypeError):
                    continue

                item_data = {
                    "product_id": product.id,
                    "product_name": product.product_name,
                    "quantity": qty,
                    "qty_picked": picked,
                    "mrp": float(product.mrp),
                    "unit_distributor_price": float(
                        item.get(
                            "unit_distributor_price",
                            original_item.get("unit_distributor_price", 0)
                        ) or 0
                    ),
                    "remarks": item.get("remarks", original_item.get("remarks", "")),
                    "hsn_code": product.hsn_code or "",
                    "cartons": item.get("cartons", original_item.get("cartons", "")),
                    "gross_weight": item.get("gross_weight", original_item.get("gross_weight", "")),
                    "net_weight": item.get("net_weight", original_item.get("net_weight", "")),
                    "short_pick_generated": original_item.get("short_pick_generated", False),
                    "stockout_split_generated": original_item.get("stockout_split_generated", False),
                }

                updated_items.append(item_data)
                total_it += 1
                total_qy += qty
                total_pk += picked

            instance.product_items = updated_items
            instance.total_items = total_it
            instance.total_quantity = total_qy
            instance.qty_picked = total_pk

        elif top_level_qty_picked is not None:
            current_items = instance.product_items or []
            updated_items = []

            rem_to_pick = int(top_level_qty_picked or 0)
            total_qy = 0
            total_it = 0
            total_pk = 0

            for item in current_items:
                qy = int(item.get("quantity", 0) or 0)
                it_pk = qy if rem_to_pick >= qy else rem_to_pick
                rem_to_pick = max(0, rem_to_pick - qy)

                item["qty_picked"] = it_pk
                item["short_pick_generated"] = item.get("short_pick_generated", False)
                item["stockout_split_generated"] = item.get("stockout_split_generated", False)

                updated_items.append(item)

                total_it += 1
                total_qy += qy
                total_pk += it_pk

            instance.product_items = updated_items
            instance.total_items = total_it
            instance.total_quantity = total_qy
            instance.qty_picked = total_pk

        if new_status == "PICKED" and instance.total_quantity == 0 and instance.product_items:
            instance.total_quantity = sum(
                int(item.get("quantity", 0) or 0)
                for item in instance.product_items
            )

        safe_fields = [
            "status",
            "remarks",
            "approved_by",
            "approved_at",
            "distributor_id",
            "company_id",
        ]

        for attr, value in validated_data.items():
            if attr in safe_fields:
                setattr(instance, attr, value)

        if new_status == "APPROVED" and old_status != "APPROVED":
            approve_short_items = self._reserve_serials_for_po(instance)

            if approve_short_items:
                self._create_short_pick_po(
                    instance,
                    approve_short_items,
                    status="SUBMITTED",
                    remarks=f"Auto split PO from APPROVED shortage of {instance.po_number}"
                )

        elif new_status == "PICKED":
            stockout_items = self._mark_picked_and_stockout(instance)

            if stockout_items:
                self._create_short_pick_po(
                    instance,
                    stockout_items,
                    status="STOCK_OUT",
                    remarks=f"Auto stockout split PO from PICKED shortage of {instance.po_number}"
                )

        if new_status in ["APPROVED", "PICKED"]:
            instance.total_quantity = sum(
                int(it.get("quantity", 0) or 0)
                for it in instance.product_items
            )
            instance.qty_picked = sum(
                int(it.get("qty_picked", 0) or 0)
                for it in instance.product_items
            )

        elif new_status in ["PACKED", "DELIVERED"]:
            order_serials = InventorySerial.objects.filter(
                orders__purchase_order_id=instance,
                status="PICKED"
            ).distinct()

            for serial in order_serials:
                serial.status = new_status
                serial.save(update_fields=["status"])

        instance.save()
        return instance



class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields ="__all__"
class LeaveBalanceSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=LeaveBalance._meta.get_field('employee_id').related_model.objects.all())
    employee_name = serializers.SerializerMethodField()

    cl = serializers.IntegerField(required=False, default=0)
    sl = serializers.IntegerField(required=False, default=0)
    pl = serializers.IntegerField(required=False, default=0)
    ul = serializers.IntegerField(required=False, default=0)
    compensatory_off = serializers.IntegerField(required=False, default=0)
    public_holiday = serializers.IntegerField(required=False, default=0)
    maternity_leave = serializers.IntegerField(required=False, default=0)
    paternity_leave = serializers.IntegerField(required=False, default=0)

    used_days = serializers.IntegerField(required=False, default=0)

    # read-only
    total_allocated = serializers.IntegerField(read_only=True)
    remaining_days = serializers.IntegerField(read_only=True)
    leave_type = serializers.CharField(required=False, allow_blank=True)
    year = serializers.DateField(required=False)

    created_at = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        employee = attrs.get("employee_id")
        year = attrs.get("year")

        if employee and year:

            qs = LeaveBalance.objects.filter(
                employee_id=employee,
                year__year=year.year,
                year__month=year.month
            )

            # 🔥 exclude update case
            if self.instance:
                qs = qs.exclude(id=self.instance.id)

            if qs.exists():
                raise serializers.ValidationError({
                    "error": "Leave already exists for this employee in this month and year."
                })

        return attrs

    def get_employee_name(self, obj):
        if obj.employee_id:
            return f"{obj.employee_id.first_name} {obj.employee_id.last_name}"
        return None


    # 🔹 CREATE
    def create(self, validated_data):
        total = (
            int(validated_data.get("cl", 0) or 0) +
            int(validated_data.get("sl", 0) or 0) +
            int(validated_data.get("pl", 0) or 0) +
            int(validated_data.get("ul", 0) or 0) +
            int(validated_data.get("compensatory_off", 0) or 0) +
            int(validated_data.get("public_holiday", 0) or 0) +
            int(validated_data.get("maternity_leave", 0) or 0) +
            int(validated_data.get("paternity_leave", 0) or 0)
        )

        validated_data["total_allocated"] = total
        validated_data["remaining_days"] = total - int(validated_data.get("used_days", 0) or 0)

        return LeaveBalance.objects.create(**validated_data)

    # 🔹 UPDATE
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        total = (
            int(instance.cl or 0) +
            int(instance.sl or 0) +
            int(instance.pl or 0) +
            int(instance.ul or 0) +
            int(instance.compensatory_off or 0) +
            int(instance.public_holiday or 0) +
            int(instance.maternity_leave or 0) +
            int(instance.paternity_leave or 0)
        )

        instance.total_allocated = total
        instance.remaining_days = total - int(instance.used_days or 0)

        instance.save()
        return instance

class LeaveRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    leave_type = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    total_leaves = serializers.IntegerField()
    reason = serializers.CharField()
    upload_doc = serializers.ImageField(required=False, allow_null=True)

    status = serializers.CharField(required=False)
    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,
        allow_null=True
    )

    created_at = serializers.DateTimeField(read_only=True)
    approved_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return LeaveRequest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        old_status = instance.status
        old_leave_type = instance.leave_type
        old_leaves = instance.total_leaves

        new_status = validated_data.get("status", instance.status)
        new_leave_type = validated_data.get("leave_type", instance.leave_type)
        new_leaves = validated_data.get("total_leaves", instance.total_leaves)

        # Leave type mapping
        leave_type_map = {
            "CL": "cl",
            "SL": "sl",
            "PL": "pl",
            "UL": "ul",
            "COMPENSATORY_OFF": "compensatory_off",
            "PUBLIC_HOLIDAY": "public_holiday",
            "MATERNITY_LEAVE": "maternity_leave",
            "PATERNITY_LEAVE": "paternity_leave",
        }

        old_field = leave_type_map.get(str(old_leave_type).upper())
        new_field = leave_type_map.get(str(new_leave_type).upper())

        if not new_field:
            raise serializers.ValidationError({
                "leave_type": f"Invalid leave type: {new_leave_type}"
            })

        # ✅ employee ke liye ek hi leave balance record lo
        balance, created = LeaveBalance.objects.get_or_create(
            employee_id=instance.employee_id,
            defaults={
                "leave_type": "All",
                "total_allocated": 0,
                "used_days": 0,
                "remaining_days": 0,
                "cl": 0,
                "sl": 0,
                "pl": 0,
                "ul": 0,
                "compensatory_off": 0,
                "public_holiday": 0,
                "maternity_leave": 0,
                "paternity_leave": 0,
            }
        )

        # current values
        old_field_value = getattr(balance, old_field, 0) if old_field else 0
        new_field_value = getattr(balance, new_field, 0)

        # ---------------------------------------------------
        # 1) Pending/Rejected -> Approved
        # ---------------------------------------------------
        if old_status != "approved" and new_status == "approved":
            if new_leaves > new_field_value:
                raise serializers.ValidationError({
                    "error": f"Not enough {new_leave_type} balance. Available: {new_field_value}"
                })

            setattr(balance, new_field, new_field_value - new_leaves)
            balance.used_days += new_leaves

        # ---------------------------------------------------
        # 2) Approved -> Rejected/Cancelled/Pending
        # ---------------------------------------------------
        elif old_status == "approved" and new_status != "approved":
            if not old_field:
                raise serializers.ValidationError({
                    "leave_type": f"Invalid old leave type: {old_leave_type}"
                })

            old_current_value = getattr(balance, old_field, 0)
            setattr(balance, old_field, old_current_value + old_leaves)
            balance.used_days -= old_leaves

        # ---------------------------------------------------
        # 3) Approved -> Approved
        #    (days ya leave type dono change ho sakte hain)
        # ---------------------------------------------------
        elif old_status == "approved" and new_status == "approved":
            if old_field == new_field:
                diff = new_leaves - old_leaves

                if diff > 0:
                    # leave increase hui hai
                    if diff > new_field_value:
                        raise serializers.ValidationError({
                            "error": f"Not enough {new_leave_type} balance to increase leave. Available: {new_field_value}"
                        })
                    setattr(balance, new_field, new_field_value - diff)
                    balance.used_days += diff

                elif diff < 0:
                    # leave decrease hui hai
                    setattr(balance, new_field, new_field_value + abs(diff))
                    balance.used_days -= abs(diff)

            else:
                # leave type change hua hai
                # pehle old leave return karo
                old_current_value = getattr(balance, old_field, 0)
                setattr(balance, old_field, old_current_value + old_leaves)

                # ab new leave deduct karo
                updated_new_field_value = getattr(balance, new_field, 0)
                if new_leaves > updated_new_field_value:
                    raise serializers.ValidationError({
                        "error": f"Not enough {new_leave_type} balance. Available: {updated_new_field_value}"
                    })

                setattr(balance, new_field, updated_new_field_value - new_leaves)

                # used_days net adjust
                balance.used_days = balance.used_days - old_leaves + new_leaves

        # negative used_days protection
        if balance.used_days < 0:
            balance.used_days = 0

        # total/remaining recalculate
        balance.total_allocated = (
            (balance.cl or 0) +
            (balance.sl or 0) +
            (balance.pl or 0) +
            (balance.ul or 0) +
            (balance.compensatory_off or 0) +
            (balance.public_holiday or 0) +
            (balance.maternity_leave or 0) +
            (balance.paternity_leave or 0) +
            (balance.used_days or 0)
        )

        balance.remaining_days = (
            (balance.cl or 0) +
            (balance.sl or 0) +
            (balance.pl or 0) +
            (balance.ul or 0) +
            (balance.compensatory_off or 0) +
            (balance.public_holiday or 0) +
            (balance.maternity_leave or 0) +
            (balance.paternity_leave or 0)
        )

        balance.save()

        # ✅ request instance update last me karo
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class ExpenseClaimSerializer(serializers.ModelSerializer):

    # ---------- EXTRA DISPLAY FIELDS ----------
    employee_name = serializers.SerializerMethodField(read_only=True)
    lead_type = serializers.SerializerMethodField(read_only=True)
    approved_by_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ExpenseClaim
        fields = "__all__"

    # ---------- METHODS ----------
    def get_employee_name(self, obj):
        if obj.employee_id:
            return f"{obj.employee_id.first_name} {obj.employee_id.last_name}"
        return None

    def get_lead_type(self, obj):
        if obj.lead_id:
            return obj.lead_id.lead_type
        return None

    def get_approved_by_name(self, obj):
        if obj.approved_by:
            return f"{obj.approved_by.first_name} {obj.approved_by.last_name}"
        return None

class LeadFollowUpSerializer(serializers.ModelSerializer):

    employee_name = serializers.SerializerMethodField(read_only=True)
    lead_type = serializers.SerializerMethodField()
    lead_name = serializers.SerializerMethodField()
    contact_person = serializers.SerializerMethodField()
    contact_person_display = serializers.SerializerMethodField()
    lead_status = serializers.SerializerMethodField()

    class Meta:
        model = LeadFollowUp
        fields = "__all__"

    # 🔹 Employee Name
    def get_employee_name(self, obj):
        if obj.employee_id:
            return f"{obj.employee_id.first_name} {obj.employee_id.last_name}"
        return None

    # 🔹 Lead Type
    def get_lead_type(self, obj):
        if obj.lead_id:
            return obj.lead_id.lead_type
        return None

    # 🔹 Lead Name
    def get_lead_name(self, obj):
        if obj.lead_id:
            return obj.lead_id.business_name
        return None

    # 🔹 Contact Person
    def get_contact_person(self, obj):
        if obj.lead_id:
            return obj.lead_id.contact_person
        return None

    # ✅ FIXED METHOD NAME
    def get_contact_person_display(self, obj):
        if obj.lead_id:
            return obj.lead_id.phone   # 👈 your phone field
        return None

    # 🔹 Lead Status
    def get_lead_status(self, obj):
        if obj.lead_id:
            return obj.lead_id.lead_status
        return None

class WareHouseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    address = serializers.CharField()
    code = serializers.CharField(max_length=20)
    status = serializers.ChoiceField(choices=[('active', 'Active'), ('deactive', 'Deactive')])

    # Create
    def create(self, validated_data):
        return WareHouse.objects.create(**validated_data)

    # Update
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.code = validated_data.get('code', instance.code)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    # WRITE: warehouse id
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=WareHouse.objects.all(),
        required=True
    )

    # READ: warehouse name
    warehouse_name = serializers.CharField(
        source='warehouse_id.name',
        read_only=True
    )

    name = serializers.CharField(max_length=100)
    address = serializers.CharField()
    code = serializers.CharField(max_length=20)
    status = serializers.ChoiceField(
        choices=[('active', 'Active'), ('deactive', 'Deactive')]
    )

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.warehouse_id = validated_data.get(
            'warehouse_id', instance.warehouse_id
        )
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.code = validated_data.get('code', instance.code)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance



class DistributerOrdersSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    distributor_id = serializers.PrimaryKeyRelatedField(
        queryset=DistributorInformation.objects.all()
    )

    inventory_serial_id = serializers.PrimaryKeyRelatedField(
        queryset=InventorySerial.objects.all()
    )
    purchase_order_id = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseOrder.objects.all()
    )
    order_date = serializers.DateTimeField(read_only=True)

    serial_number = serializers.SerializerMethodField(read_only=True)
    product_id = serializers.SerializerMethodField(read_only=True)   # ✅ Added
    product_name = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)  # ✅ Added
    def get_status(self, obj):
        if obj.purchase_order_id:
            return obj.purchase_order_id.status
        return None



    # ✅ Serial Number
    def get_serial_number(self, obj):
        if obj.inventory_serial_id:
            return getattr(obj.inventory_serial_id, "serial_number", None)
        return None

    # ✅ Product ID
    def get_product_id(self, obj):
        if obj.inventory_serial_id and obj.inventory_serial_id.product_id:
            return obj.inventory_serial_id.product_id.id
        return None

    # ✅ Product Name
    def get_product_name(self, obj):
        if obj.inventory_serial_id and obj.inventory_serial_id.product_id:
            return getattr(obj.inventory_serial_id.product_id, "product_name", None)
        return None

    # ✅ Create
    def create(self, validated_data):
        return DistributerOrders.objects.create(**validated_data)

    # ✅ Update
    def update(self, instance, validated_data):
        instance.distributor_id = validated_data.get("distributor_id", instance.distributor_id)
        instance.inventory_serial_id = validated_data.get("inventory_serial_id", instance.inventory_serial_id)
        instance.purchase_order_id = validated_data.get("purchase_order_id", instance.purchase_order_id)
        instance.save()
        return instance

class PicProductSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    purchase_order_id = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseOrder.objects.all()
    )

    reserved_products = serializers.SerializerMethodField()

    def get_reserved_products(self, obj):

        # 🔥 Only fetch from InventorySerial
        reserved_serials = InventorySerial.objects.filter(
            status="RESERVED"
        ).values()

        return list(reserved_serials)


class PackProductSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    purchase_order_id = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseOrder.objects.all()
    )

    picked_products = serializers.SerializerMethodField()

    def get_picked_products(self, obj):

        # 🔥 Only fetch from InventorySerial
        picked_serials = InventorySerial.objects.filter(
            status="PICKED"
        ).values()

        return list(picked_serials)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from myapp.models import Po_payment, DistributorInformation, PurchaseOrder, Admin

from rest_framework import serializers
from .models import Po_payment, DistributorInformation, PurchaseOrder, Admin
from django.conf import settings
from rest_framework import serializers

from django.conf import settings
from rest_framework import serializers

class PoPaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    distributor = serializers.PrimaryKeyRelatedField(
        queryset=DistributorInformation.objects.all(),
        write_only=True,
        required=True,
        error_messages={"required": "Distributor is required."}
    )
    distributor_name = serializers.CharField(read_only=True)

    purchase_order = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseOrder.objects.all(),
        write_only=True,
        required=True,
        error_messages={"required": "Purchase order is required."}
    )
    po_number = serializers.CharField(read_only=True)

    # ✅ multiple images
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        error_messages={"required": "Amount is required."}
    )

    payment_date = serializers.DateField(
        required=True,
        error_messages={"required": "Payment date is required."}
    )

    approved_by = serializers.PrimaryKeyRelatedField(
        queryset=Admin.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    admin_name = serializers.CharField(read_only=True)

    # ✅ ADDED STATUS CHOICES (ONLY ADD THIS)
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    status = serializers.ChoiceField(
        choices=STATUS_CHOICES,
        required=False
    )

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # ✅ FIX: support multiple images from form-data
    def to_internal_value(self, data):
        request = self.context.get("request")

        if request:
            images = request.FILES.getlist("images")

            if images:
                data = data.copy()
                data.setlist("images", images)

        return super().to_internal_value(data)

    # ✅ CREATE
    def create(self, validated_data):
        images = validated_data.pop('images', [])

        payment = Po_payment.objects.create(**validated_data)

        image_paths = []

        for image in images:
            file_name = f"{uuid.uuid4()}_{image.name.replace(' ', '_')}"
            file_path = f"uploads/{file_name}"

            full_path = os.path.join(settings.MEDIA_ROOT, file_path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            image_paths.append(file_path)

        payment.images = image_paths
        payment.save()

        return payment

    # ✅ UPDATE
    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])

        instance.amount = validated_data.get("amount", instance.amount)
        instance.payment_date = validated_data.get("payment_date", instance.payment_date)
        instance.approved_by = validated_data.get("approved_by", instance.approved_by)
        instance.status = validated_data.get("status", instance.status)

        image_paths = instance.images or []

        for image in images:
            file_name = f"{uuid.uuid4()}_{image.name.replace(' ', '_')}"
            file_path = f"uploads/{file_name}"

            full_path = os.path.join(settings.MEDIA_ROOT, file_path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            image_paths.append(file_path)

        instance.images = image_paths
        instance.save()

        return instance

    # ✅ RESPONSE
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "distributor": instance.distributor.id if instance.distributor else None,
            "distributor_name": str(instance.distributor) if instance.distributor else None,
            "purchase_order": instance.purchase_order.id if instance.purchase_order else None,
            "po_number": instance.purchase_order.po_number if instance.purchase_order else None,

            "images": [
                settings.MEDIA_URL + img for img in (instance.images or [])
            ],

            "amount": instance.amount,
            "payment_date": instance.payment_date,
            "approved_by": instance.approved_by.id if instance.approved_by else None,
            "admin_name": str(instance.approved_by) if instance.approved_by else None,

            # ✅ STATUS ADDED HERE TOO
            "status": instance.status,
            "company_id": instance.company_id.id if instance.company_id else None,
            "company_name": instance.company_id.company_name if instance.company_id else None,

            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }



class TravelPlanSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )

    month = serializers.CharField()

    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False, allow_null=True)

    region = serializers.CharField()
    states = serializers.CharField()
    rm = serializers.CharField()
    tsm = serializers.CharField()

    # ✅ VALIDATION
    def validate(self, data):
        employee = data.get("employee_id")
        month = data.get("month")

        # 🔹 check required fields
        if not employee:
            raise serializers.ValidationError("Employee is required")

        if not month:
            raise serializers.ValidationError("Month is required")

        # 🔹 Month format validation + past month check
        try:
            try:
                # ✅ Full month name → February-2026
                input_date = datetime.strptime(month, "%B-%Y")
            except ValueError:
                # ✅ Short month name → Feb-2026
                input_date = datetime.strptime(month, "%b-%Y")

        except ValueError:
            raise serializers.ValidationError(
                "Invalid format. Use Month-YYYY format only "
                "(e.g. February-2026 or Feb-2026)"
            )

        today = datetime.today()
        current_month = datetime(today.year, today.month, 1)

        # compare only month/year
        input_month = datetime(input_date.year, input_date.month, 1)

        if input_month < current_month:
            raise serializers.ValidationError(
                "Past month or year is not allowed."
            )

        # 🔹 Duplicate check
        qs = TravelPlan.objects.filter(
            employee_id=employee,
            month__iexact=month
        )

        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError(
                f"{month} is already exists for this employee."
            )

        return data

    # ✅ CREATE
    def create(self, validated_data):
        return TravelPlan.objects.create(**validated_data)

    # ✅ UPDATE
    def update(self, instance, validated_data):
        instance.employee_id = validated_data.get(
            'employee_id', instance.employee_id
        )
        instance.month = validated_data.get("month", instance.month)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.region = validated_data.get("region", instance.region)
        instance.states = validated_data.get("states", instance.states)
        instance.rm = validated_data.get("rm", instance.rm)
        instance.tsm = validated_data.get("tsm", instance.tsm)

        instance.save()
        return instance

class DailyPlanSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    travel_plan = serializers.PrimaryKeyRelatedField(queryset=TravelPlan.objects.all())
    travel_plan_data = serializers.SerializerMethodField()

    date = serializers.DateField()
    place = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)

    def get_travel_plan_data(self, obj):
        return {
            "id": obj.travel_plan.id,
            "employee_id": obj.travel_plan.employee_id.id if obj.travel_plan.employee_id else None,
            "month": obj.travel_plan.month,
            "start_date": obj.travel_plan.start_date,
            "end_date": obj.travel_plan.end_date,
            "region": obj.travel_plan.region,
            "states": obj.travel_plan.states,
            "rm": obj.travel_plan.rm,
            "tsm": obj.travel_plan.tsm
        }

    def create(self, validated_data):
        return DailyPlan.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.travel_plan = validated_data.get("travel_plan", instance.travel_plan)
        instance.date = validated_data.get("date", instance.date)
        instance.place = validated_data.get("place", instance.place)
        instance.notes = validated_data.get("notes", instance.notes)

        instance.save()
        return instance






from decimal import Decimal
import calendar
from rest_framework import serializers
from .models import Salary_payment, Employee, EmployeeSalary

# agar ye models hain to import karo
# from .models import Attendance, LeaveRequest, Holiday

import calendar
from decimal import Decimal
from django.db.models import Sum
from rest_framework import serializers



from django.db.models import Sum
from decimal import Decimal
import calendar
from rest_framework import serializers
from rest_framework import serializers
from decimal import Decimal
from django.db.models import Sum



import calendar

from decimal import Decimal, ROUND_HALF_UP

from rest_framework import serializers

# make sure these are already imported in your file
# from .models import Salary_payment, Employee, EmployeeSalary, Expenses_login, LeaveRequest, Holiday

import calendar
from decimal import Decimal, ROUND_HALF_UP
from rest_framework import serializers

class SalaryPaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )
    month = serializers.IntegerField()
    year = serializers.IntegerField()

    present_days = serializers.IntegerField(read_only=True)
    paid_leave_days = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    unpaid_leave_days = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    holidays = serializers.IntegerField(read_only=True)
    half_days = serializers.IntegerField(read_only=True)
    weekly_offs = serializers.IntegerField(read_only=True)
    absent_days = serializers.IntegerField(read_only=True)

    total_hour = serializers.SerializerMethodField()

    gross_salary = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    deductions = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    net_salary = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    generated_at = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        month = attrs.get("month")
        year = attrs.get("year")
        employee = attrs.get("employee")

        if month < 1 or month > 12:
            raise serializers.ValidationError({"month": "Month must be between 1 and 12."})

        if year < 2000 or year > 2100:
            raise serializers.ValidationError({"year": "Enter a valid year."})

        if employee and month and year:
            duplicate_qs = Salary_payment.objects.filter(
                employee=employee,
                month=month,
                year=year
            )

            if self.instance:
                duplicate_qs = duplicate_qs.exclude(id=self.instance.id)

            if duplicate_qs.exists():
                raise serializers.ValidationError({
                    "non_field_errors": ["Salary already exists for this employee in this month and year."]
                })

        return attrs

    def get_month_days(self, year, month):
        return calendar.monthrange(year, month)[1]

    def get_weekly_offs(self, year, month):
        total_days = self.get_month_days(year, month)
        sundays = 0
        from datetime import date

        for day in range(1, total_days + 1):
            d = date(year, month, day)
            if d.weekday() == 6:
                sundays += 1
        return sundays

    def get_employee_salary(self, employee, month, year):
        salary = EmployeeSalary.objects.filter(
            employee_id=employee,
            status=True
        ).order_by("-effective_from").first()

        if not salary:
            raise serializers.ValidationError({
                "employee": "Active salary structure not found for this employee."
            })

        return salary

    def get_total_hour(self, obj):
                return str(obj.total_hour or "0.00")

    def calculate_salary_data(self, employee, month, year):
        from datetime import date, time, datetime

        total_month_days = self.get_month_days(year, month)
        total_sundays_in_month = self.get_weekly_offs(year, month)

        present_count = 0
        half_day_count = 0
        paid_leave_days = Decimal("0.00")
        unpaid_leave_days = Decimal("0.00")
        holidays_count = 0
        total_hour_sum = Decimal("0.00")
        late_comings_count = 0
        short_hours_strikes = 0
        very_short_hours_strikes = 0

        start_date = date(int(year), int(month), 1)
        end_date = date(int(year), int(month), total_month_days)

        attendance_records = Expenses_login.objects.filter(
            employee=employee,
            date__range=[start_date, end_date]
        )

        attendance_map = {}
        for att in attendance_records:
            if att.date not in attendance_map:
                attendance_map[att.date] = []
            attendance_map[att.date].append(att)

        leaves = LeaveRequest.objects.filter(
            employee_id=employee,
            status="approved",
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        holidays = {
            h.holiday_date: h for h in Holiday.objects.filter(
                holiday_date__range=[start_date, end_date],
                is_paid=True
            )
        }

        # only non-sunday paid holidays counted separately
        # so that Sunday holiday is not double-counted as holiday + weekly off
        weekly_off_dates = set()
        for day_num in range(1, total_month_days + 1):
            curr_date = date(int(year), int(month), day_num)
            if curr_date.weekday() == 6:
                weekly_off_dates.add(curr_date)

        holidays_count = sum(
            1 for holiday_date in holidays.keys()
            if holiday_date not in weekly_off_dates
        )

        # attendance / leave / half-day / hours logic kept same
        for day_num in range(1, total_month_days + 1):
            curr_date = date(int(year), int(month), day_num)

            day_atts = attendance_map.get(curr_date, [])
            if day_atts:
                is_present = False
                is_half = False
                is_full = False

                valid_atts = [a for a in day_atts if a.start_time]
                is_late_deduction = False

                if valid_atts:
                    first_att = min(valid_atts, key=lambda x: x.start_time)
                    actual_start = first_att.start_time
                    expected_start = datetime.combine(curr_date, time(9, 0))

                    if actual_start.tzinfo is not None:
                        from django.utils import timezone
                        expected_start = timezone.make_aware(expected_start)

                    delay_seconds = (actual_start - expected_start).total_seconds()

                    if delay_seconds >= 600:
                        is_late_deduction = True
                    elif delay_seconds >= 60:
                        late_comings_count += 1
                        if late_comings_count > 3:
                            is_late_deduction = True

                raw_hours = sum(Decimal(str(a.total_hours or 0)) for a in day_atts)
                total_hour_sum += raw_hours

                if raw_hours >= Decimal("9.0"):
                    is_present = True
                elif Decimal("8.90") <= raw_hours < Decimal("9.0"):
                    short_hours_strikes += 1
                    if short_hours_strikes > 3:
                        is_half = True
                    else:
                        is_present = True
                else:
                    very_short_hours_strikes += 1
                    if very_short_hours_strikes > 3:
                        is_full = True
                    else:
                        is_half = True

                for att in day_atts:
                    if att.full_leave:
                        is_full = True
                    elif att.half_leave:
                        is_half = True

                if is_late_deduction:
                    is_half = True

                if is_full:
                    pass
                elif is_half:
                    half_day_count += 1
                    continue
                elif is_present:
                    present_count += 1
                    continue

            day_leave = None
            for lr in leaves:
                if lr.start_date <= curr_date <= lr.end_date:
                    day_leave = lr
                    break

            if day_leave:
                total_lr_days = (day_leave.end_date - day_leave.start_date).days + 1
                if total_lr_days > 0:
                    day_weight = Decimal(str(day_leave.total_leaves)) / Decimal(str(total_lr_days))
                    if day_leave.leave_type in ["CL", "SL", "PL"]:
                        paid_leave_days += day_weight
                    else:
                        unpaid_leave_days += day_weight
                continue

        # weekly offs are total Sundays in the month
        weekly_offs_count = total_sundays_in_month

        # absent should be calculated after fixing Sundays and non-Sunday holidays
        accounted_days = (
            Decimal(str(present_count))
            + Decimal(str(half_day_count))
            + paid_leave_days
            + unpaid_leave_days
            + Decimal(str(holidays_count))
            + Decimal(str(weekly_offs_count))
        )

        absent_days = Decimal(str(total_month_days)) - accounted_days
        if absent_days < 0:
            absent_days = Decimal("0.00")

        salary_obj = self.get_employee_salary(employee, month, year)
        gross_salary = Decimal(str(salary_obj.gross_salary or 0))

        # FIX:
        # DO NOT add salary_obj.deductions again here,
        # because gross_salary already includes:
        # basic_salary + allowances - deductions
        per_day_salary = gross_salary / Decimal(str(total_month_days))

        lop_days = unpaid_leave_days + absent_days + (Decimal(str(half_day_count)) * Decimal("0.5"))
        lop_amount = per_day_salary * lop_days

        total_deductions = lop_amount
        net_salary = gross_salary - total_deductions

        if net_salary < 0:
            net_salary = Decimal("0.00")

        return {
            "present_days": present_count,
            "paid_leave_days": paid_leave_days.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "unpaid_leave_days": unpaid_leave_days.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "holidays": holidays_count,
            "half_days": half_day_count,
            "weekly_offs": weekly_offs_count,
            "absent_days": int(absent_days.quantize(Decimal("1"), rounding=ROUND_HALF_UP)),
            "total_hour": total_hour_sum.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "gross_salary": gross_salary.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "deductions": total_deductions.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "net_salary": net_salary.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        }

    def create(self, validated_data):
        employee = validated_data["employee"]
        month = validated_data["month"]
        year = validated_data["year"]

        if Salary_payment.objects.filter(employee=employee, month=month, year=year).exists():
            raise serializers.ValidationError({
                "non_field_errors": ["Salary already generated for this employee, month and year."]
            })

        calculated_data = self.calculate_salary_data(employee, month, year)

        return Salary_payment.objects.create(
            employee=employee,
            month=month,
            year=year,
            present_days=calculated_data["present_days"],
            paid_leave_days=calculated_data["paid_leave_days"],
            unpaid_leave_days=calculated_data["unpaid_leave_days"],
            holidays=calculated_data["holidays"],
            half_days=calculated_data["half_days"],
            weekly_offs=calculated_data["weekly_offs"],
            absent_days=calculated_data["absent_days"],
            total_hour=calculated_data["total_hour"],
            gross_salary=calculated_data["gross_salary"],
            deductions=calculated_data["deductions"],
            net_salary=calculated_data["net_salary"],
        )

    def update(self, instance, validated_data):
        employee = validated_data.get("employee", instance.employee)
        month = validated_data.get("month", instance.month)
        year = validated_data.get("year", instance.year)

        duplicate_qs = Salary_payment.objects.filter(
            employee=employee,
            month=month,
            year=year
        ).exclude(id=instance.id)

        if duplicate_qs.exists():
            raise serializers.ValidationError({
                "non_field_errors": ["Salary already exists for this employee, month and year."]
            })

        calculated_data = self.calculate_salary_data(employee, month, year)

        instance.employee = employee
        instance.month = month
        instance.year = year
        instance.present_days = calculated_data["present_days"]
        instance.paid_leave_days = calculated_data["paid_leave_days"]
        instance.unpaid_leave_days = calculated_data["unpaid_leave_days"]
        instance.holidays = calculated_data["holidays"]
        instance.half_days = calculated_data["half_days"]
        instance.weekly_offs = calculated_data["weekly_offs"]
        instance.absent_days = calculated_data["absent_days"]
        instance.total_hour = calculated_data["total_hour"]
        instance.gross_salary = calculated_data["gross_salary"]
        instance.deductions = calculated_data["deductions"]
        instance.net_salary = calculated_data["net_salary"]
        instance.save()

        return instance
from datetime import datetime

class DistributorTargetSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    distributor = serializers.PrimaryKeyRelatedField(
        queryset=DistributorInformation.objects.all()
    )

    month = serializers.CharField()
    target = serializers.CharField(allow_blank=True, required=False)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # ✅ VALIDATION (ONLY place where conversion happens)
    def validate(self, data):

        # ✅ handle POST + PATCH safely
        if self.instance:
            distributor = data.get('distributor') or self.instance.distributor
        else:
            distributor = data.get('distributor')

        month_str = data.get('month')

        # ✅ month handling
        if month_str:
            try:
                month_date = datetime.strptime(month_str, "%Y-%m").date().replace(day=1)
            except ValueError:
                raise serializers.ValidationError({
                    "month": "Month must be in YYYY-MM format"
                })
        else:
            if self.instance:
                month_date = self.instance.month   # PATCH case
            else:
                raise serializers.ValidationError({
                    "month": "This field is required"
                })

        # ✅ duplicate check
        qs = DistributorInformation_Target.objects.filter(
            distributor=distributor,
            month=month_date
        )

        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError({
                "month": "This distributor already has a target for this month and year."
            })

        # ✅ assign back
        data['distributor'] = distributor
        data['month'] = month_date

        return data


    # ✅ CREATE (NO conversion here)
    def create(self, validated_data):
        return DistributorInformation_Target.objects.create(**validated_data)

    # ✅ UPDATE (NO conversion here)
    def update(self, instance, validated_data):
        instance.distributor = validated_data.get('distributor', instance.distributor)
        instance.month = validated_data.get('month', instance.month)
        instance.target = validated_data.get('target', instance.target)

        instance.save()
        return instance

    # ✅ RESPONSE FORMAT
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['month'] = instance.month.strftime('%Y-%m')
        return data

class ProductTargetSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    month = serializers.CharField()   # ✅ string
    target = serializers.CharField(allow_blank=True, required=False)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # ✅ VALIDATION
    def validate(self, data):

        # ✅ SAFE handling for POST + PATCH
        if self.instance:
            product = data.get('product') or self.instance.product
        else:
            product = data.get('product')

        month_str = data.get('month')

        # ✅ month handling
        if month_str:
            try:
                month_date = datetime.strptime(month_str, "%Y-%m").date().replace(day=1)
            except ValueError:
                raise serializers.ValidationError({
                    "month": "Month must be in YYYY-MM format"
                })
        else:
            if self.instance:
                month_date = self.instance.month
            else:
                raise serializers.ValidationError({
                    "month": "This field is required"
                })

        # ✅ duplicate check
        qs = Product_Target.objects.filter(
            product=product,
            month=month_date
        )

        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError({
                "month": "This product already has a target for this month and year."
            })

        # ✅ assign back
        data['product'] = product
        data['month'] = month_date

        return data


    # ✅ CREATE (NO date() here)
    def create(self, validated_data):
        return Product_Target.objects.create(**validated_data)

    # ✅ UPDATE
    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.month = validated_data.get('month', instance.month)
        instance.target = validated_data.get('target', instance.target)

        instance.save()
        return instance

    # ✅ RESPONSE
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['month'] = instance.month.strftime('%Y-%m')
        return data



class CategoryTargetSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    month = serializers.CharField()   # ✅ accept "2023-09"
    target = serializers.CharField(allow_blank=True, required=False)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # ✅ VALIDATION
    def validate(self, data):
        # 👇 use existing instance values if not provided
        category = data.get('category') or self.instance.category
        month_str = data.get('month')

        # 👇 handle month safely
        if month_str:
            try:
                month_date = datetime.strptime(month_str, "%Y-%m").date().replace(day=1)
            except ValueError:
                raise serializers.ValidationError({
                    "month": "Month must be in YYYY-MM format"
                })
        else:
            month_date = self.instance.month   # 👈 IMPORTANT

        # duplicate check
        qs = Category_Target.objects.filter(
            category=category,
            month=month_date
        )

        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError({
                "month": "Already exists for this month"
            })

        data['month'] = month_date
        data['category'] = category

        return data



    # ✅ CREATE
    def create(self, validated_data):
        return Category_Target.objects.create(**validated_data)

    # ✅ UPDATE
    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.month = validated_data.get('month', instance.month)
        instance.target = validated_data.get('target', instance.target)

        instance.save()
        return instance

    # ✅ RESPONSE
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['month'] = instance.month.strftime('%Y-%m')
        return data

import re
import os
from PIL import Image
class CompanyProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    company_name = serializers.CharField(max_length=255)
    company_address = serializers.CharField()

    # ✅ CHANGED → FileField (for SVG support)
    company_logo = serializers.FileField(required=False, allow_null=True)

    bank_name = serializers.CharField(max_length=255)
    account_no = serializers.CharField(max_length=50)
    branch = serializers.CharField(max_length=255)
    branch_code = serializers.CharField(max_length=20)

    ifsc_code = serializers.CharField(max_length=20)
    pancard_no = serializers.CharField(required=True, allow_null=True)

    email = serializers.EmailField()
    contact_no = serializers.CharField(max_length=15)

    remark = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # ✅ CHANGED → FileField (for SVG support)
    sign = serializers.FileField(required=False, allow_null=True)

    # =========================
    # ✅ IMAGE + SVG VALIDATION
    # =========================
    def validate_image_file(self, file):
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.svg']
        ext = os.path.splitext(file.name)[1].lower()

        # ❌ Invalid extension
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                "Only JPG, JPEG, PNG, SVG files are allowed."
            )

        # ❌ File size > 2MB
        if file.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("File size must be under 2MB")

        # ✅ SVG validation
        if ext == '.svg':
            try:
                content = file.read().decode('utf-8')
                if '<svg' not in content:
                    raise serializers.ValidationError("Invalid SVG file")
            except Exception:
                raise serializers.ValidationError("Invalid SVG file")

            file.seek(0)  
            return file

        # ✅ JPG / PNG validation
        try:
            img = Image.open(file)
            img.verify()
        except Exception:
            raise serializers.ValidationError("Invalid or corrupted image")

        return file

    # =========================
    # ✅ APPLY VALIDATION
    # =========================
    def validate_company_logo(self, value):
        return self.validate_image_file(value)

    def validate_sign(self, value):
        return self.validate_image_file(value)

    # =========================
    # ✅ Account Number Validation
    # =========================
    def validate_account_no(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Account number must contain only digits.")

        if len(value) < 9 or len(value) > 18:
            raise serializers.ValidationError("Account number must be between 9 and 18 digits.")

        return value

    # =========================
    # ✅ IFSC Code Validation
    # =========================
    def validate_ifsc_code(self, value):
        value = value.upper()

        pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Invalid IFSC code format. Example: SBIN0001234"
            )

        return value

    # =========================
    # ✅ Contact Number Validation
    # =========================
    def validate_contact_no(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Contact number must contain only digits.")

        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Contact number must be between 10 and 15 digits.")

        return value

    # =========================
    # ✅ Email Validation
    # =========================
    def validate_email(self, value):
        instance = getattr(self, 'instance', None)

        if instance:
            if CompanyProfile.objects.filter(email=value).exclude(id=instance.id).exists():
                raise serializers.ValidationError("Email already exists.")
        else:
            if CompanyProfile.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists.")

        return value

    # =========================
    # ✅ CREATE
    # =========================
    def create(self, validated_data):
        return CompanyProfile.objects.create(**validated_data)

    # =========================
    # ✅ UPDATE
    # =========================
    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance




class ShipmentSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    order_id = serializers.PrimaryKeyRelatedField(
        queryset=PurchaseOrder.objects.all()
    )

    tracking_number = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    shipment_status = serializers.ChoiceField(
        choices=Shipment.SHIPMENT_STATUS,
        default="created"
    )

    shipped_at = serializers.DateTimeField(
        required=False,
        allow_null=True
    )

    estimated_delivery = serializers.DateField(
        required=False,
        allow_null=True
    )

    created_at = serializers.DateTimeField(read_only=True)

    name = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        allow_null=True
    )

    contact_number = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    service_type = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True
    )
    image = serializers.ImageField(
        required=False,
        allow_null=True
    )

    # ✅ CREATE
    def create(self, validated_data):
        return Shipment.objects.create(**validated_data)

    # ✅ UPDATE
    def update(self, instance, validated_data):

        instance.order_id = validated_data.get("order_id", instance.order_id)
        instance.tracking_number = validated_data.get("tracking_number", instance.tracking_number)
        instance.shipment_status = validated_data.get("shipment_status", instance.shipment_status)
        instance.shipped_at = validated_data.get("shipped_at", instance.shipped_at)
        instance.estimated_delivery = validated_data.get("estimated_delivery", instance.estimated_delivery)
        instance.name = validated_data.get("name", instance.name)
        instance.contact_number = validated_data.get("contact_number", instance.contact_number)
        instance.email = validated_data.get("email", instance.email)
        instance.service_type = validated_data.get("service_type", instance.service_type)
        instance.image = validated_data.get("image", instance.image)

        instance.save()
        return instance

class CarBrandSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=30)

    # Create method
    def create(self, validated_data):
        return CarBrand.objects.create(**validated_data)

    # Update method
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class CarModelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    # write (input)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=CarBrand.objects.all()
    )
    # read (output)
    brand_name = serializers.CharField(source='brand_id.name', read_only=True)

    name = serializers.CharField(max_length=30)

    # ✅ Create
    def create(self, validated_data):
        return CarModel.objects.create(**validated_data)

    # ✅ Update
    def update(self, instance, validated_data):
        instance.brand_id = validated_data.get('brand_id', instance.brand_id)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class GetQuoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    full_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    contact = serializers.CharField(max_length=15)
    Address = serializers.CharField()

    # ✅ Foreign Keys (write)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=CarBrand.objects.all()
    )
    model_id = serializers.PrimaryKeyRelatedField(
        queryset=CarModel.objects.all()
    )

    # ✅ Foreign Keys (read)
    brand_name = serializers.CharField(source='brand_id.name', read_only=True)
    model_name = serializers.CharField(source='model_id.name', read_only=True)

    service = serializers.ChoiceField(
        choices=GetQuote.SERVICE_CHOICE,
        default='WINDOW FILM'
    )

    created_at = serializers.DateTimeField(read_only=True)

    # ✅ Create
    def create(self, validated_data):
        return GetQuote.objects.create(**validated_data)

    # ✅ Update
    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.Address = validated_data.get('Address', instance.Address)
        instance.brand_id = validated_data.get('brand_id', instance.brand_id)
        instance.model_id = validated_data.get('model_id', instance.model_id)
        instance.service = validated_data.get('service', instance.service)
        instance.save()
        return instance

class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    status = serializers.CharField(default='disable')

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty")
        return value

    # ✅ CREATE
    def create(self, validated_data):
        return Region.objects.create(**validated_data)

    # ✅ UPDATE
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class RegionTargetSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    region = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all()
    )

    month = serializers.CharField()   # ✅ accept "2023-09"
    target = serializers.CharField(allow_blank=True, required=False)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # ✅ VALIDATION
    def validate(self, data):
        # 👇 use existing instance values if not provided
        region = data.get('region') or self.instance.region
        month_str = data.get('month')

        # 👇 handle month safely
        if month_str:
            try:
                month_date = datetime.strptime(month_str, "%Y-%m").date().replace(day=1)
            except ValueError:
                raise serializers.ValidationError({
                    "month": "Month must be in YYYY-MM format"
                })
        else:
            month_date = self.instance.month   # 👈 IMPORTANT

        # duplicate check
        qs = Region_Target.objects.filter(
            region=region,
            month=month_date
        )

        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError({
                "month": "Already exists for this month"
            })

        data['month'] = month_date
        data['region'] = region

        return data

    # ✅ CREATE
    def create(self, validated_data):
        return Region_Target.objects.create(**validated_data)

    # ✅ UPDATE
    def update(self, instance, validated_data):
        instance.region = validated_data.get('region', instance.region)
        instance.month = validated_data.get('month', instance.month)
        instance.target = validated_data.get('target', instance.target)

        instance.save()
        return instance

    # ✅ RESPONSE
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['month'] = instance.month.strftime('%Y-%m')
        return data


class GallerySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    image = serializers.ImageField()
    gallery_sequence = serializers.IntegerField()

    def create(self, validated_data):
        return Gallery.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.gallery_sequence = validated_data.get('gallery_sequence', instance.gallery_sequence)
        instance.save()
        return instance


class DashboardSerializer(serializers.Serializer):
    department = serializers.IntegerField()
    roles = serializers.IntegerField()
    office_branches = serializers.IntegerField()
    employee = serializers.IntegerField()
    users = serializers.IntegerField()
    personal_details = serializers.IntegerField()
    employee_salary = serializers.IntegerField()
    employee_documents = serializers.IntegerField()
    leave_balance = serializers.IntegerField()
    leave_request = serializers.IntegerField()
    employee_attendance = serializers.IntegerField()
    salary_payout = serializers.IntegerField()
    leads = serializers.IntegerField()
    visits = serializers.IntegerField()
    lead_followups = serializers.IntegerField()
    travel_plan = serializers.IntegerField()
    expense = serializers.IntegerField()
    holiday = serializers.IntegerField()



class ReplacementRequestSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    old_serial_number = serializers.CharField(write_only=True, required=True)
    new_serial_number = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    old_serial = serializers.SerializerMethodField(read_only=True)
    new_serial = serializers.SerializerMethodField(read_only=True)

    reason = serializers.CharField(required=True)
    remarks = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    status = serializers.CharField(required=False)

    requested_at = serializers.DateTimeField(read_only=True)
    approved_at = serializers.DateTimeField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)

    distributor_detail = serializers.SerializerMethodField(read_only=True)
    product_detail = serializers.SerializerMethodField(read_only=True)
    old_po_detail = serializers.SerializerMethodField(read_only=True)
    replacement_po_detail = serializers.SerializerMethodField(read_only=True)
    new_distributor_detail = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

    def get_image(self, obj):
        return obj.image or []

    def _save_images(self):
        request = self.context.get("request")
        if not request:
            return []

        files = request.FILES.getlist("image")
        image_urls = []

        for file in files:
            saved_path = default_storage.save(
                f"replacement_images/{file.name}",
                file
            )
            image_urls.append(
                request.build_absolute_uri("/media/" + saved_path)
            )

        return image_urls

    def get_old_serial(self, obj):
        if not obj.old_serial:
            return None

        return {
            "id": obj.old_serial.id,
            "serial_number": obj.old_serial.serial_number,
            "status": obj.old_serial.status,
            "product_id": obj.old_serial.product_id.id if obj.old_serial.product_id else None,
            "product_name": obj.old_serial.product_id.product_name if obj.old_serial.product_id else None,
        }

    def get_new_serial(self, obj):
        if not obj.new_serial:
            return None

        return {
            "id": obj.new_serial.id,
            "serial_number": obj.new_serial.serial_number,
            "status": obj.new_serial.status,
            "product_id": obj.new_serial.product_id.id if obj.new_serial.product_id else None,
            "product_name": obj.new_serial.product_id.product_name if obj.new_serial.product_id else None,
        }


    def get_new_distributor_detail(self, obj):

    # If new distributor exists then use it
        distributor = getattr(obj, "new_distributor", None)

        # Otherwise fallback to old distributor
        if not distributor:
            distributor = getattr(obj, "distributor_id", None)

        if not distributor:
            return None

        region = getattr(distributor, "sales_region", None)

        return {
            "id": distributor.id,
            "distributor_type": getattr(distributor, "distributor_type", None),
            "distributor_name": getattr(distributor, "distributor_name", None),
            "region": str(region) if region else None,
            # "region_id": region.id if region else None,
        }

    def get_distributor_detail(self, obj):
        distributor = getattr(obj, "distributor_id", None)

        if not distributor:
            return None

        region = getattr(distributor, "sales_region", None)

        return {
            "id": distributor.id,
            "distributor_type": getattr(distributor, "distributor_type", None),
            "distributor_name": getattr(distributor, "distributor_name", None),
            "region": str(region) if region else None,
            # "region_id": region.id if region else None,
        }

    def get_product_detail(self, obj):
        product = getattr(obj, "product_id", None)

        if not product and obj.old_serial:
            product = obj.old_serial.product_id

        if not product:
            return None

        return {
            "id": product.id,
            "product_name": getattr(product, "product_name", None),
        }

    def get_old_po_detail(self, obj):
        old_po = getattr(obj, "purchase_order_id", None)

        if not old_po:
            return None

        return {
            "id": old_po.id,
            "po_number": getattr(old_po, "po_number", None),
            "status": old_po.status,
        }

    def get_replacement_po_detail(self, obj):
        replacement_po = getattr(obj, "replacement_po", None)

        if not replacement_po:
            return None

        return {
            "id": replacement_po.id,
            "po_number": getattr(replacement_po, "po_number", None),
            "status": replacement_po.status,
        }

    def _find_old_order_detail(self, old_serial):
        return DistributerOrders.objects.filter(
            inventory_serial_id=old_serial
        ).order_by("-id").first()

    def _find_warranty(self, old_serial):
        return Warranty.objects.filter(
            serial_id=old_serial,
            warranty_status="ACTIVE"
        ).order_by("-id").first()

    def create(self, validated_data):

        old_serial_number = validated_data.pop("old_serial_number")
        image_urls = self._save_images()

        try:
            old_serial = InventorySerial.objects.get(
                serial_number=old_serial_number
            )
        except InventorySerial.DoesNotExist:
            raise serializers.ValidationError({
                "old_serial_number": "Old serial number does not exist."
            })

        if old_serial.status != "DELIVERED":
            raise serializers.ValidationError({
                "old_serial_number": "Only DELIVERED serial can be replaced."
            })

        already_pending = ReplacementRequest.objects.filter(
            old_serial=old_serial,
            status__in=["PENDING", "APPROVED"]
        ).exists()

        if already_pending:
            raise serializers.ValidationError({
                "old_serial_number": "Replacement request already exists for this serial."
            })

        old_order = self._find_old_order_detail(old_serial)

        if not old_order:
            raise serializers.ValidationError({
                "purchase_order": "Order history not found for this old serial."
            })

        old_po = old_order.purchase_order_id

        if not old_po:
            raise serializers.ValidationError({
                "purchase_order": "Old purchase order not found for this serial."
            })

        distributor = old_order.distributor_id

        replacement = ReplacementRequest.objects.create(
            old_serial=old_serial,
            distributor_id=distributor,
            product_id=old_serial.product_id,
            purchase_order_id=old_po,
            reason=validated_data.get("reason"),
            remarks=validated_data.get("remarks"),
            status="PENDING",
            image=image_urls
        )

        return replacement

    def update(self, instance, validated_data):

        new_status = validated_data.get("status", instance.status)
        new_serial_number = validated_data.get("new_serial_number", None)

        new_image_urls = self._save_images()
        if new_image_urls:
            old_images = instance.image or []
            instance.image = old_images + new_image_urls

        if "reason" in validated_data:
            instance.reason = validated_data.get("reason")

        if "remarks" in validated_data:
            instance.remarks = validated_data.get("remarks")

        if new_status == "REJECTED":

            if instance.status != "PENDING":
                raise serializers.ValidationError({
                    "status": "Only PENDING replacement can be rejected."
                })

            instance.status   = "REJECTED"
            instance.save()
            return instance

        if new_status == "APPROVED":

            if instance.status != "PENDING":
                raise serializers.ValidationError({
                    "status": "Only PENDING replacement can be approved."
                })

            with transaction.atomic():

                old_serial = instance.old_serial
                product = instance.product_id or old_serial.product_id
                distributor = instance.distributor_id
                old_po = instance.purchase_order_id

                if not distributor:
                    raise serializers.ValidationError({
                        "distributor": "Distributor not found for this old serial."
                    })

                if not old_po:
                    raise serializers.ValidationError({
                        "purchase_order": "Old purchase order not found."
                    })

                warranty = self._find_warranty(old_serial)

                if not warranty:
                    raise serializers.ValidationError({
                        "warranty": "Replacement not allowed. Warranty is not active."
                    })

                if (
                    warranty.warranty_end_date and
                    warranty.warranty_end_date < timezone.now().date()
                ):
                    raise serializers.ValidationError({
                        "warranty": "Replacement not allowed. Warranty has expired."
                    })

                if new_serial_number:
                    try:
                        new_serial = InventorySerial.objects.select_for_update().get(
                            serial_number=new_serial_number
                        )
                    except InventorySerial.DoesNotExist:
                        raise serializers.ValidationError({
                            "new_serial_number": "New serial number does not exist."
                        })
                else:
                    new_serial = InventorySerial.objects.select_for_update().filter(
                        product_id=product,
                        status="IN_STOCK"
                    ).order_by("id").first()

                    if not new_serial:
                        raise serializers.ValidationError({
                            "new_serial_number": "No IN_STOCK serial available for this product."
                        })

                if new_serial.status != "IN_STOCK":
                    raise serializers.ValidationError({
                        "new_serial_number": "New serial must be IN_STOCK."
                    })

                if new_serial.id == old_serial.id:
                    raise serializers.ValidationError({
                        "new_serial_number": "Old serial and new serial cannot be same."
                    })

                if new_serial.product_id != product:
                    raise serializers.ValidationError({
                        "new_serial_number": "New serial product must be same as old serial product."
                    })

                replacement_po = PurchaseOrder.objects.create(
                distributor_id=distributor,
                remarks=f"Replacement PO for old serial {old_serial.serial_number}",
                status="APPROVED",
                product_items=[
                    {
                        "product_id": product.id,
                        "quantity": 1,
                        "price": 0,
                        "gst": 0,
                        "total": 0,
                        "qty_picked": 0,
                        "short_pick": 0,
                        "remarks": "Replacement Product",
                    }
                ]
            )

                if hasattr(replacement_po, "po_number"):
                    old_po_number = getattr(old_po, "po_number", "OLD")
                    replacement_po.po_number = f"{old_po_number}-RPL-{replacement_po.id}"
                    replacement_po.save(update_fields=["po_number"])

                old_serial.status = "REPLACED"
                old_serial.save(update_fields=["status"])

                new_serial.status = "RESERVED"
                new_serial.save(update_fields=["status"])

                # Replacement PO entry create
                DistributerOrders.objects.create(
                    purchase_order_id=replacement_po,
                    distributor_id=distributor,
                    inventory_serial_id=new_serial,
                )

                instance.new_serial = new_serial
                instance.replacement_po = replacement_po
                instance.status = "APPROVED"
                instance.approved_at = timezone.now()
                instance.save()

            return instance

        if new_status == "COMPLETED":

            if instance.status != "APPROVED":
                raise serializers.ValidationError({
                    "status": "Only APPROVED replacement can be completed."
                })

            if not instance.new_serial:
                raise serializers.ValidationError({
                    "new_serial": "New serial is required before completing replacement."
                })

            instance.new_serial.status = "DELIVERED"
            instance.new_serial.save(update_fields=["status"])

            instance.status = "COMPLETED"
            instance.completed_at = timezone.now()
            instance.save()

            return instance

        instance.save()
        return instance

class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })
        return data
    
class DistributorResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        distributor = self.context["request"].user

        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        # check old password
        if not check_password(old_password, distributor.password):
            raise serializers.ValidationError({
                "old_password": "Old password is incorrect"
            })

        # check confirm password
        if new_password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "New password and confirm password do not match"
            })

        return data
    
class EmployeeResetPasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):

        employee = self.context["employee"]

        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        # check old password
        if employee.password != old_password:
            raise serializers.ValidationError({
                "old_password": "Old password is incorrect"
            })

        # check confirm password
        if new_password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })

        return data

class TestimonialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)

    image = serializers.ImageField(
        required=False,
        allow_null=True
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
        default=""
    )

    rating = serializers.IntegerField()

    created_at = serializers.DateTimeField(read_only=True)

    # 🔹 Create
    def create(self, validated_data):
        return Testimonial.objects.create(**validated_data)

    # 🔹 Update
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.rating = validated_data.get('rating', instance.rating)

        instance.save()
        return instance