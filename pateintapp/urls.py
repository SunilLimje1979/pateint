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
     path("update_patient_by_id/",update_patient_by_id),
     path("insert_disease/",insert_disease),
     path("get_diseases_by_doctorid/",get_diseases_by_doctorid),
     path("get_diseases_by_diseaseid/",get_diseases_by_diseaseid),
     path("update_disease_by_diseaseid/",update_disease_by_diseaseid),
     path("insert_allergy/",insert_allergy),
     path("get_allergies_by_doctorid/",get_allergies_by_doctorid),
     path("get_allergy_by_allergyid/",get_allergy_by_allergyid),
     path("update_allergy_by_allergyid/",update_allergy_by_allergyid),
     path("insert_patient_doctor_link/",insert_patient_doctor_link),
     path("get_patient_doctor_links_by_doctor_id/",get_patient_doctor_links_by_doctor_id),
     path("get_patients_by_doctor_id/",get_patients_by_doctor_id),
     path("get_patient_doctor_links_by_doctorid_patientid/",get_patient_doctor_links_by_doctorid_patientid),
     path("update_patient_doctor_link_by_doctorid_patientid/",update_patient_doctor_link_by_doctorid_patientid),
     path("insert_patient_allergies/",insert_patient_allergies),
     path("get_patient_allergies_by_patientid/",get_patient_allergies_by_patientid),
     path("insert_patient_diseases/",insert_patient_diseases),
     path("get_patient_diseases_by_patientid/",get_patient_diseases_by_patientid),
     path("delete_patient_allergy/",delete_patient_allergy),
     path("delete_patient_disease/",delete_patient_disease),
     path('get_patient_details_by_appointment_id/',get_patient_details_by_appointment_id,name='get_patient_details_by_appointment_id'),
     path('get_doctors_by_patient_id/',get_doctors_by_patient_id,name='get_doctors_by_patient_id'),
]

