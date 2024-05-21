from django.urls import path
from .views import (fi_insert_patient_charges,fi_soft_delete_patient_charges)
from .views import fi_get_patient_Outstanding
from django.urls import path
from .views import *
urlpatterns = [    
        
    ######################### Patient Charges  ############################  
    path('insert_patient_charges/', fi_insert_patient_charges, name='insert_patient_charges'),
    path('delete_patient_charges/<int:pateint_charges_id>/', fi_soft_delete_patient_charges, name='delete_patient_charges'),

    ######################### Patient Outstanding  ############################  
    path('get_patient_outstanding/<int:patient_id>/', fi_get_patient_Outstanding, name='get_patient_outstanding'),

    
     path("insert_patient_payments/",insert_patient_payments),
     path("delete_patient_payments/",delete_patient_payments),
     path("insert_patient/",insert_patient),
     path("delete_patient/",delete_patient),
     path("get_patient_byid/",get_patient_byid),
     path("get_patient_details_by_phone/",get_patient_details_by_phone),
     path("get_patients_by_mobile_number/",get_patients_by_mobile_number),
]

