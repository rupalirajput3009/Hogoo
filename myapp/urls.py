
from django.urls import path
from .views import *

urlpatterns = [
    path('admin_data/', AdminView.as_view()),
    path('admin_data/<int:id>/', AdminView.as_view()),
    path('admin_login/', AdminLoginAPIView.as_view()),
    path('admin_profile/', AdminProfileView.as_view()),

    path("admin_forgot_password/", AdminForgotPasswordView.as_view()),
    path("admin_reset_password/", AdminResetPasswordView.as_view()),

    path("category/<int:id>/", CategoryView.as_view()),  # single / update / delete
    path("category/", CategoryView.as_view()),


    path('products/', ProductAPI.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductAPI.as_view(), name='product-detail'),
    path('products/sequence/', ProductAPI.as_view(), name='product-sequence'),

    path('banner/',BannerAPIView.as_view(),name='banner_list_create'),
    path('banner/<int:pk>/',BannerAPIView.as_view(),name='banner_details'),

    path("colour/", ColourAPIView.as_view(), name="colour"),
    path("colour/<int:pk>/", ColourAPIView.as_view(), name="colour-detail"),

    path("material/", MaterialAPIView.as_view(), name="material"),
    path("material/<int:pk>/", MaterialAPIView.as_view(), name="material-detail"),

    path('shipments/', ImportShipmentAPI.as_view()),
    path('shipments/<int:pk>/', ImportShipmentAPI.as_view()),

    path('costs/', ImportCostAPI.as_view()),
    path('costs/<int:pk>/', ImportCostAPI.as_view()),

    path('shipment_products/', ShipmentProductAPI.as_view()),
    path('shipment_products/<int:pk>/', ShipmentProductAPI.as_view()),

    path("departments/", DepartmentAPI.as_view()),
    path("departments/<int:pk>/", DepartmentAPI.as_view()),

    path("roles/", RolesAPI.as_view()),
    path("roles/<int:pk>/", RolesAPI.as_view()),

    path("office_branches/", OfficeBranchAPI.as_view()),
    path("office_branches/<int:pk>/", OfficeBranchAPI.as_view()),

    path("employee/", EmployeeView.as_view()),
    path("employee/<int:id>/", EmployeeView.as_view()),

    path("employee_login/", EmployeeLoginAPIView.as_view()),
    path("employee_profile/", EmployeeProfileView.as_view()),
    
    # path("employee-forgot-password/",EmployeeForgotPasswordAPIView.as_view()),
    # path( "employee-reset-password/",EmployeeResetPasswordView.as_view()),

    path('leads/', LeadAPI.as_view()),
    path('leads/<int:pk>/', LeadAPI.as_view()),
    path("employee-lead-monthly-report/", EmployeeLeadMonthlyReportAPI.as_view(), name="employee-lead-monthly-report"),
    path("employee-lead-monthly-report-excel/",EmployeeLeadMonthlyReportAPI.as_view(),name="employee-lead-monthly-report"),

    path('expenses/', ExpenseAPI.as_view()),
    path("expenses/<int:pk>/", ExpenseAPI.as_view()),

    path("blogs/", BlogAPIView.as_view()),
    path("blogs/<int:pk>/", BlogAPIView.as_view()),

    path('visits/', VisitAPI.as_view()),
    path('visits/<int:pk>/', VisitAPI.as_view()),

    # path('distributor/', DistributorAPIView.as_view(), name='distributor-list'),
    # path('distributor/<int:pk>/', DistributorAPIView.as_view(), name='distributor-detail'),

    path("businesslegalinfo/",businessLegalInfoAPIView.as_view()),
    path("businesslegalinfo/<int:pk>/",businessLegalInfoAPIView.as_view()),

    path('distributor-information/', DistributorInformationAPIView.as_view(), name='distributor-list'),        # All distributors
    path('distributor-information/<int:pk>/', DistributorInformationAPIView.as_view(), name='distributor-detail'),

    path('api/distributor/login/', DistributorLoginAPIView.as_view(), name='distributor-login'),
    path("api/distributor/profile/", DistributorProfileAPIView.as_view(), name="distributor-profile"),


    path("serial/",SerialAPIView.as_view()),
    path("serial/<int:pk>/",SerialAPIView.as_view()),

    path('warranty/', WarrantyAPI.as_view()),
    path('warranty/<str:value>/', WarrantyAPI.as_view()),

    path("employee-salary/", EmployeeSalaryAPIView.as_view()),
    path("employee-salary/<int:pk>/", EmployeeSalaryAPIView.as_view()),

    path("Employeepersonaldetails/",employeepersonaldetailsView.as_view()),
    path("Employeepersonaldetails/<int:pk>/",employeepersonaldetailsView.as_view()),

    path("employee-documents/", EmployeeDocumentsAPIView.as_view()),
    path("employee-documents/<int:pk>/", EmployeeDocumentsAPIView.as_view()),

    path('users/', UserAPI.as_view()),           # GET all, POST
    path('users/<int:pk>/', UserAPI.as_view()),

    path("inventory_serials/", InventorySerialAPI.as_view()),
    path("inventory_serials/<int:serial_id>/", InventorySerialAPI.as_view()),
    path("inventory_serial_history/", InventorySerialHistoryAPI.as_view()),
    path("inventory_serials/scan/<str:serial_number>/", InventorySerialScanDetailAPI.as_view()),
    path("product/", ProductScanDetailView.as_view(), name='product-scan-detail'),

    path("employee_attendence/", EmployeeAttendenceAPI.as_view()),
    path("employee_attendence/<int:pk>/", EmployeeAttendenceAPI.as_view()),

    path("purchase-orders/", PurchaseOrderAPIView.as_view(), name="po-list-create"),
    path("purchase-orders/<int:pk>/", PurchaseOrderAPIView.as_view(), name="po-detail"),
    path("purchase-orders/<int:pk>/picked-pdf/", PurchaseOrderPDFView.as_view(), name="po-pdf"),
    path("purchase-orders/<int:pk>/packing-pdf/", PurchaseOrderPackingPDFView.as_view(), name="po-packing-pdf"),
    path("purchase-orders/<int:pk>/invoice-pdf/", PurchaseOrderInvoicePDFView.as_view(), name="po-invoice-pdf"),

    path('holidays/', HolidayAPIView.as_view(), name='holiday-list'),
    path('holidays/<int:pk>/', HolidayAPIView.as_view(), name='holiday-detail'),

    path("leave-balance/", LeaveBalanceAPIView.as_view(),name='leave-balance'),
    path("leave-balance/<int:pk>/", LeaveBalanceAPIView.as_view(),name='leave-balance'),

    path("leave-requests/", LeaveRequestAPI.as_view()),
    path("leave-requests/<int:pk>/", LeaveRequestAPI.as_view()),

    path('expense-claims/',ExpenseClaimsAPIView.as_view(), name='expense-claim'),
    path('expense-claims/<int:pk>/',ExpenseClaimsAPIView.as_view(), name='expense-claim'),

    path('lead_followups/', LeadFollowUpAPIView.as_view(), name='leadfollowup-list'),


    path('lead_followups/<int:pk>/', LeadFollowUpAPIView.as_view(), name='leadfollowup-detail'),
    path("today-followups/<int:employee_id>/", TodayFollowUpAPI.as_view(), name="today-followups"),

    path('warehouses/', WareHouseAPIView.as_view(), name='warehouse-list-create'),
    path('warehouses/<int:pk>/', WareHouseAPIView.as_view(), name='warehouse-detail'),

    path('locations/', LocationAPIView.as_view()),
    path('locations/<int:pk>/', LocationAPIView.as_view()),

    path("distributor_orders/", DistributerOrdersAPIView.as_view(), name="distributor-orders"),
    path("distributor_orders/<int:pk>/", DistributerOrdersAPIView.as_view(), name="distributor-orders-detail"),

    path("pic_products/", PicProductAPIView.as_view()),
    path("pic_products/<int:pk>/", PicProductAPIView.as_view()),

    path('pack_products/', PackProductAPIView.as_view()),
    path('pack_products/<int:pk>/', PackProductAPIView.as_view()),

    path('contacts/', ContactAPIView.as_view(), name='contact_list_create'),
    path('contacts/<int:pk>/', ContactAPIView.as_view(), name='contact_detail'),

    path("po-payments/", PoPaymentAPIView.as_view()),
    path("po-payments/<int:pk>/", PoPaymentAPIView.as_view()),

    path("travel-plan/", TravelPlanAPI.as_view(), name="travel-plan"),
    path("travel-plan/<int:id>/", TravelPlanAPI.as_view(), name="travel-plan"),

    path('daily-plan/', DailyPlanView.as_view(), name='daily-plan-list-create'),
    path('daily-plan/<int:pk>/', DailyPlanView.as_view(), name='daily-plan-detail'),

    path("salary-payment/", SalaryPaymentAPI.as_view(), name="salary-payment-list"),
    path("salary-payment/<int:id>/", SalaryPaymentAPI.as_view(), name="salary-payment-detail"),
    path('bulk-salary-payment/', BulkSalaryPaymentAPI.as_view(), name='bulk-salary-payment'),

    path('distributortargets/', DistributorTargetAPIView.as_view(), name='distributortargets'),
    path('distributortargets/<int:pk>/', DistributorTargetAPIView.as_view(), name='distributortarget-detail'),

    path('producttargets/', ProductTargetAPIView.as_view(), name='producttargets'),
    path('producttargets/<int:pk>/', ProductTargetAPIView.as_view(), name='producttarget-detail'),

    path('categorytargets/', CategoryTargetAPIView.as_view(), name='categorytargets'),
    path('categorytargets/<int:pk>/', CategoryTargetAPIView.as_view(), name='categorytarget-detail'),

    path('company_profile/', CompanyProfileAPIView.as_view()),
    path('company_profile/<int:pk>/', CompanyProfileAPIView.as_view()),

    path("shipment/", ShipmentAPIView.as_view(), name="shipment-list-create"),
    path("shipment/<int:pk>/", ShipmentAPIView.as_view(), name="shipment-detail"),

    path('carbrands/', CarBrandAPIView.as_view(), name='carbrand-list'),
    path('carbrands/<int:pk>/', CarBrandAPIView.as_view(), name='carbrand-detail'),

    path('carmodels/', CarModelAPIView.as_view(), name='carmodel-list'),
    path('carmodels/<int:pk>/', CarModelAPIView.as_view(), name='carmodel-detail'),

    path('quotes/', GetQuoteAPIView.as_view()),
    path('quotes/<int:pk>/', GetQuoteAPIView.as_view()),

    path('regions/', RegionAPIView.as_view()),
    path('regions/<int:pk>/', RegionAPIView.as_view()),

    path('regiontargets/', RegionTargetAPIView.as_view()),
    path('regiontargets/<int:pk>/', RegionTargetAPIView.as_view()),


    path("category-target-report/", CategoryTargetReportAPIView.as_view(), name="category-target-report"),
    path('category-target-report-excel/',CategoryTargetReportExcelAPIView.as_view(),name='category-target-report-excel'),
    path('all-category-target-report-excel/',AllCategoryTargetReportExcelAPIView.as_view(),name='all-category-target-report-excel'),

    path("distributor-target-report/", DistributorTargetReportAPIView.as_view(), name="distributor-target-report"),
    path('distributor-target-report-excel/',DistributorTargetReportExcelAPIView.as_view(),name='distributor-target-report-excel'),
    path('all-distributor-target-report-excel/',AllDistributorTargetReportExcelAPIView.as_view(),name='all-distributor-target-report-excel'),
    
    path("product-target-report/", ProductTargetReportAPIView.as_view(), name="product-target-report"),
    path('product-target-report-excel/',ProductTargetReportExcelAPIView.as_view(),name='product-target-report-excel'),
    path('all-product-target-report-excel/',AllProductTargetReportExcelAPIView.as_view(),name='all-product-target-report-excel'),
    
    path('region-target-report/', RegionTargetReportAPIView.as_view(), name='region-target-report'),
    path("region-target-report-excel/",RegionTargetReportExcelAPIView.as_view(),name="region-target-report-excel" ),
    path('all-region-target-report-excel/',AllRegionTargetReportExcelAPIView.as_view(),name='all-region-target-report-excel'),


    path("warranty-card/<int:serial_id>/pdf/", WarrantyCardPDFView.as_view(), name="warranty-card-pdf"),
    path("warranty-card/bulk-pdf/", WarrantyCardBulkPDFView.as_view(), name="warranty-card-bulk-pdf"),

    path('gallery/', GalleryAPIView.as_view(), name='gallery-list-create'),
    path('gallery/<int:pk>/', GalleryAPIView.as_view(), name='gallery-detail'),
    
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
    
    path("replacement/", ReplacementRequestAPI.as_view()),
    path("replacement/<int:pk>/", ReplacementRequestAPI.as_view()),
    

    path("employee-forgot-password/", EmployeeForgotPasswordAPIView.as_view(), name="employee-forgot-password"),
    path( "employee-reset-password/",EmployeeResetPasswordAPIView.as_view()),
    
    
    path("distributor/forgot-password/",DistributorForgotPasswordAPIView.as_view(),name="distributor-forgot-password"),
    path("distributor/reset-password/",DistributorResetPasswordAPIView.as_view(),name="distributor-reset-password"),

    path('testimonials/', TestimonialView.as_view()),
    path('testimonials/<int:id>/', TestimonialView.as_view()),
    
    path('shipment-product-excel-download/',ShipmentProductExcelDownloadAPI.as_view(),name='shipment-product-excel-download' ),
    
    path("warranty-excel-report/", WarrantyExcelExportAPIView.as_view(), name="warranty-excel-export"),

    

]