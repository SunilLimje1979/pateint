from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from datetime import datetime
from rest_framework.views import APIView
from django.db import models
from medicify_project.models import * 
from medicify_project.serializers import *
import time
######################### Patient Charges ############################   
######################## Post ############################
@api_view(['POST'])
def fi_insert_patient_charges(request):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        data=request.data.copy() 
        data['isdeleted']=0
        current_datetime = datetime.now()
        data['createdon']=int(current_datetime.timestamp())
        serializer = PatientChargesSerializer(data=data)
        

        if serializer.is_valid():
            serializer.save()
            res = {
                'message_code': 1000,
                'message_text': 'Patient charges inserted successfully.',
                'message_data': serializer.data,
                'message_debug': debug if debug else []
            }
        else:
            errors = {field: serializer.errors[field][0] for field in serializer.errors}
            res = {
                'message_code': 999,
                'message_text': errors,
                'message_data': {},
                'message_debug': debug if debug else []
            }
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in inserting Patient charges. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_201_CREATED if res['message_code'] == 1000 else status.HTTP_400_BAD_REQUEST)
######################## Delete ############################
@api_view(['DELETE'])
def fi_soft_delete_patient_charges(request, pateint_charges_id):
    debug = ""
    res = {'message_code': 999, 'message_text': 'Functional part is commented.', 'message_data': {}, 'message_debug': debug}

    try:
        patient_charges = TblpateintCharges.objects.get(pk=pateint_charges_id)
        patient_charges.isdeleted = True
        patient_charges.save()

        if patient_charges.isdeleted:
            response_data = {
                'message': f'Patient charges ID {pateint_charges_id} marked as deleted successfully.',
            }
            res = {
                'message_code': 1000,
                'message_text': 'Success',
                'message_data': response_data,
                'message_debug': debug if debug else []
            }
        else:
            res = {
                'message_code': 999,
                'message_text': 'Patient charges ID not found.',
                'message_data': {},
                'message_debug': debug if debug else []
            }
    except TblpateintCharges.DoesNotExist:
        res = {
            'message_code': 999,
            'message_text': 'Patient charges ID not found.',
            'message_data': {},
            'message_debug': debug if debug else []
        }
    except Exception as e:
        res = {
            'message_code': 999,
            'message_text': f'Error in deleting Patient charges. Error: {str(e)}',
            'message_data': {},
            'message_debug': debug if debug else []
        }

    return Response(res, status=status.HTTP_404_NOT_FOUND if res['message_code'] == 999 else status.HTTP_200_OK)

######################################## Patient Outstanding ##############################################

################################ GET ####################################

@api_view(['GET'])
def fi_get_patient_Outstanding(request, patient_id):
    debug = ""
    res = {'message_code': 999, 'message_text': 'An error occurred.', 'message_data': [], 'message_debug': {'Error': debug}}

    if not patient_id:
        res = {'message_code': 999, 'message_text': 'Patient id is required.'}
    else:
        try:
            # pateint_charges_sum = TblpateintCharges.objects.filter(patient_id=patient_id, isdeleted=0).aggregate(sumofamountPC=models.Sum('charges_amount'))['sumofamountPC']
            # pateint_charges_sumpp = TblpatientPayments.objects.filter(patient_id=patient_id, isdeleted=0).aggregate(sumofamountPP=models.Sum('payment_amount'))['sumofamountPP']

            pateint_charges_sum = TblpateintCharges.objects.filter(patient_id=patient_id).aggregate(sumofamountPC=models.Sum('charges_amount'))['sumofamountPC']
            pateint_charges_sumpp = TblpatientPayments.objects.filter(patient_id=patient_id).aggregate(sumofamountPP=models.Sum('payment_amount'))['sumofamountPP']

            outstanding = pateint_charges_sum - pateint_charges_sumpp if pateint_charges_sum and pateint_charges_sumpp else None

            if outstanding is not None:
                res = {'message_code': 1000, 'message_text': 'Success',
                       'message_data': {'outstanding': outstanding}, 'message_debug': {'Debug': debug} if debug else {}}
            else:
                res = {'message_code': 999, 'message_text': 'Patient information for this patient id not found.',
                       'message_data': [], 'message_debug': {'Debug': debug} if debug else {}}

        except Exception as e:
            res = {'message_code': 999, 'message_text': 'An error occurred.', 'message_data': [], 'message_debug': {'Error': str(e)}}

    return JsonResponse(res, safe=False)



@api_view(["POST"])
def insert_patient_payments(request):
        debug = []
        response_data = {
            'message_code': 999,
            'message_text': 'Functional part is commented.',
            'message_data': [],
            'message_debug': debug
        }

        try:
            # Extract only allowed fields from the request body
            # allowed_fields = ['doctor_id', 'patient_id', 'patient_status', 'payment_mode', 'payment_amount', 'payment_transaction_no','isdeleted']
            # body = {key: request.data[key] for key in allowed_fields if key in request.data}
            data=request.data.copy() 
            data['isdeleted']=0
            current_datetime = datetime.now()
            data['createdon']=int(current_datetime.timestamp())

            serializer = TblpatientPaymentsSerializer(data=data)

            # Validate the data using the serializer
            if serializer.is_valid():
                # Save the validated data to the database
                patient_payment = serializer.save()

                response_data = {
                    'message_code': 1000,
                    'message_text': 'Patient payments inserted successfully.',
                    'message_data': [{'Patient_Payment_Id': patient_payment.patient_payment_id}],
                    'message_debug': debug
                }
            else:
                response_data = {
                    'message_code': 999,
                    'message_text': 'Validation error',
                    'message_data': serializer.errors,
                    'message_debug': debug
                }

        except Exception as e:
            response_data = {'message_code': 999, 'message_text': f"Error: {str(e)}"}

        return Response(response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def delete_patient_payments(request):
        debug = []
        response_data = {
            'message_code': 999,
            'message_text': 'Functional part is commented.',
            'message_data': [],
            'message_debug': debug
        }

        try:
            # Extract Patient_Payment_Id from the request body
            patient_payment_id = request.data.get('Patient_Payment_Id', None)

            # Check if Patient_Payment_Id is provided
            if not patient_payment_id:
                response_data = {'message_code': 999, 'message_text': 'Patient payment id is required.'}
            else:
                # Get the patient payment instance
                patient_payment = TblpatientPayments.objects.get(patient_payment_id=patient_payment_id,isdeleted=0)

                # Mark the instance as deleted
                patient_payment.isdeleted = 1
                patient_payment.save()

                response_data = {
                    'message_code': 1000,
                    'message_text': 'Patient payment deleted successfully.',
                    'message_data': [{'Patient_Payment_Id': patient_payment_id}],
                    'message_debug': debug
                }

        except TblpatientPayments.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'Patient payment not found.'}

        except Exception as e:
            response_data = {'message_code': 999, 'message_text': f"Error: {str(e)}"}

        return Response(response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def insert_patient(request):
    debug = ""
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    try:
        # Ensure 'isdeleted' is set to 0 before using the serializer
        request.data['isdeleted'] = 0
        request.data['istestpatient'] = 0

        # Calculate Patient_Level based on the provided logic
        patient_mobile_no = request.data.get('patient_mobileno', '')
        cnt = Tblpatients.objects.filter(isdeleted=0, patient_mobileno=patient_mobile_no).count()
        request.data['follower']=cnt

        if cnt >= 1:
            request.data['patient_level'] = 'C'
        else:
            request.data['patient_level'] = 'R'

        # Convert Date of Birth to epoch time value
        dob_str = request.data.get('patient_dateofbirth', '')
        dob_datetime = datetime.strptime(dob_str, '%Y-%m-%d')
        request.data['patient_dateofbirth'] = int(dob_datetime.timestamp())

        # Use the serializer to validate and save the data
        serializer = TblpatientsSerializer(data=request.data)

        if serializer.is_valid():
            patient = serializer.save()

            response_data = {
                'message_code': 1000,
                'message_text': 'Patient information inserted successfully.',
                'message_data': [{'Patient_Id': patient.patient_id}],
                'message_debug': debug
            }
        else:
            response_data = {
                'message_code': 999,
                'message_text': 'Validation error',
                'message_data': serializer.errors,
                'message_debug': debug
            }

    except Exception as e:
        response_data = {'message_code': 999, 'message_text': f"Error: {str(e)}"}

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def delete_patient(request):
        debug = []
        response_data = {
            'message_code': 999,
            'message_text': 'Functional part is commented.',
            'message_data': [],
            'message_debug': debug
        }

        # Extract Patient_Id from the request body
        patient_id = request.data.get('Patient_Id', None)

        if not patient_id:
            response_data = {'message_code': 999, 'message_text': 'Patient id is required.'}
        else:
            try:
                # Get the patient instance
                patient = Tblpatients.objects.get(patient_id=patient_id,isdeleted=0)

                # Set IsDeleted to True
                patient.isdeleted = 1
                patient.save()

                response_data = {
                    'message_code': 1000,
                    'message_text': 'Patient deleted successfully.',
                    'message_data': [{'Patient_Id': patient_id}],
                    'message_debug': debug
                }

            except Tblpatients.DoesNotExist:
                response_data = {'message_code': 999, 'message_text': 'Patient not found.', 'message_debug': debug}

        return Response(response_data,status=status.HTTP_200_OK)

@api_view(["POST"])
def get_patient_byid(request):
        debug = []
        response_data = {
            'message_code': 999,
            'message_text': 'Functional part is commented.',
            'message_data': [],
            'message_debug': debug
        }

        # Extract patient_id from the request body
        patient_id = request.data.get('patient_id', None)

        if not patient_id:
            response_data = {'message_code': 999, 'message_text': 'Patient id is required in the request body.'}
        else:
            try:
                # Get the patient instance
                patient = Tblpatients.objects.get(patient_id=patient_id, isdeleted=0)

                # Serialize the patient data
                serializer = TblpatientsSerializer(patient)
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Patient information retrieved successfully.',
                    'message_data': serializer.data,
                    'message_debug': debug
                }

            except Tblpatients.DoesNotExist:
                response_data = {'message_code': 999, 'message_text': 'Patient not found.', 'message_debug': debug}

        return Response(response_data,status=status.HTTP_200_OK)

@api_view(["POST"])
def get_patient_details_by_phone(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    phone_number = request.data.get('phone_number', None)

    if not phone_number:
        response_data = {'message_code': 999, 'message_text': 'Phone number is required.'}
    else:
        try:
            patient = Tblpatients.objects.get(patient_mobileno=phone_number)
            serializer = TblPatientsSerializer(patient)
            response_data = {
                'message_code': 1000,
                'message_text': 'Patient details fetched successfully.',
                'message_data': serializer.data,
                'message_debug': debug
            }
        except Tblpatients.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'Patient not found.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


##########################patient selection##########################
@api_view(["POST"])
def get_patients_by_mobile_number(request):
    # Retrieve the mobile number from the request data
    mobile_number = request.data.get('mobile_number', None)

    # Check if mobile number is provided
    if not mobile_number:
        return Response({'message_code': 999, 'message_text': 'Mobile number is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Query all patients matching the given mobile number
        patients = Tblpatients.objects.filter(patient_mobileno=mobile_number)

        if not patients.exists():
            return Response({'message_code': 999, 'message_text': 'No patient details found for the given mobile number.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize patient data for all matching patients
        serializer = TblpatientsSerializer(patients, many=True)

        # Prepare response data
        response_data = {
            'message_code': 1000,
            'message_text': 'Patient details fetched successfully.',
            'patients_data': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions or errors
        return Response({'message_code': 999, 'message_text': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# def update_patient_by_id(request):
#     debug = []
#     response_data = {
#         'message_code': 999,
#         'message_text': 'Functional part is commented.',
#         'message_data': [],
#         'message_debug': debug
#     }

#     patient_id = request.data.get('patient_id', None)

#     if not patient_id:
#         response_data['message_text'] = 'Patient ID is required.'
#         return Response(response_data, status=status.HTTP_200_OK)

#     try:
#         # Get the patient instance
#         patient = Tblpatients.objects.get(patient_id=patient_id)
#     except Tblpatients.DoesNotExist:
#         response_data['message_text'] = 'Patient not found.'
#         return Response(response_data, status=status.HTTP_200_OK)

#     # Serialize the data
#     serializer = TblPatientsSerializer(patient, data=request.data, partial=True)

#     if serializer.is_valid():
#         serializer.save()
#         response_data['message_code'] = 1000
#         response_data['message_text'] = 'Patient details updated successfully'
#         response_data['message_data'] = {'patient_details': serializer.data}
#     else:
#         response_data['message_text'] = 'Invalid data provided.'
#         response_data['message_data'] = serializer.errors

#     return Response(response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def update_patient_by_id(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    patient_id = request.data.get('patient_id', None)
    updated_data = request.data

    if not patient_id:
        response_data['message_text'] = 'Patient ID is required.'
        return Response(response_data, status=status.HTTP_200_OK)

    try:
        # Get the patient instance
        patient = Tblpatients.objects.get(patient_id=patient_id)
    except Tblpatients.DoesNotExist:
        response_data['message_text'] = 'Patient not found.'
        return Response(response_data, status=status.HTTP_200_OK)

    # Convert the DOB string to epoch timestamp if provided
    dob_str = updated_data.get('patient_dateofbirth', None)
    if dob_str:
        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d')
            epoch_time = int(dob.timestamp())
            updated_data['patient_dateofbirth'] = epoch_time
        except ValueError:
            response_data['message_text'] = 'Invalid date format. Use YYYY-MM-DD.'
            return Response(response_data, status=status.HTTP_200_OK)

    # Serialize the data
    serializer = TblPatientsSerializer(patient, data=updated_data, partial=True)

    if serializer.is_valid():
        serializer.save()
        response_data['message_code'] = 1000
        response_data['message_text'] = 'Patient details updated successfully'
        response_data['message_data'] = {'patient_details': serializer.data}
    else:
        response_data['message_text'] = 'Invalid data provided.'
        response_data['message_data'] = serializer.errors

    return Response(response_data, status=status.HTTP_200_OK)


##################NEW API###################################
@api_view(["POST"])
def insert_disease(request):
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': []
    }

    disease_data = request.data

    disease_serializer = TblMasterDiseaseSerializer(data=disease_data)

    if disease_serializer.is_valid():
        disease_instance = disease_serializer.save()
        response_data['message_code'] = 1000
        response_data['message_text'] = 'Data successfully saved!'
        response_data['message_data'] = {'disease_id': disease_instance.disease_id}
    else:
        errors = {
            'doctor_leave_errors': disease_serializer.errors,
        }
        response_data['message_text'] = 'Failed to save data. Please check the errors.'
        response_data['errors'] = errors

    return Response(response_data, status=status.HTTP_200_OK)


# @api_view(["POST"])
# def get_diseases_by_doctorid(request):
#     debug = []
#     response_data = {
#         'message_code': 999,
#         'message_text': 'Functional part is commented.',
#         'message_data': [],
#         'message_debug': debug
#     }

#     doctor_id = request.data.get('doctor_id', None)

#     if not doctor_id:
#         response_data = {'message_code': 999, 'message_text': 'Doctor id is required.'}
#     else:
#         try:
#             disease = tblMasterDisease.objects.filter(doctor_id=doctor_id)
#             if disease.exists():
#                 serializer = TblMasterDiseaseSerializer(disease, many=True)
#                 response_data = {
#                     'message_code': 1000,
#                     'message_text': 'Disease details fetched successfully.',
#                     'message_data': serializer.data,
#                     'message_debug': debug
#                 }

#             else:
#                 response_data = {'message_code': 999, 'message_text': 'No diseases found for the given doctor ID.', 'message_data': [], 'message_debug': debug}
#         except tblMasterDisease.DoesNotExist:
#             response_data = {'message_code': 999, 'message_text': 'An error occurred while fetching diseases.', 'message_debug': debug}

#     return Response(response_data, status=status.HTTP_200_OK)
from django.db.models import Q
@api_view(["POST"])
def get_diseases_by_doctorid(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    doctor_id = request.data.get('doctor_id', None)

    if not doctor_id:
        response_data = {'message_code': 999, 'message_text': 'Doctor id is required.'}
    else:
        try:
            # Filter records where doctor_id matches or is None
            disease = tblMasterDisease.objects.filter((Q(doctor_id=doctor_id) | Q(doctor_id__isnull=True)) & Q(is_deleted=0))
            if disease.exists():
                serializer = TblMasterDiseaseSerializer(disease, many=True)
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Disease details fetched successfully.',
                    'message_data': serializer.data,
                    'message_debug': debug
                }
            else:
                response_data = {
                    'message_code': 999,
                    'message_text': 'No diseases found for the given doctor ID.',
                    'message_data': [],
                    'message_debug': debug
                }
        except tblMasterDisease.DoesNotExist:
            response_data = {
                'message_code': 999,
                'message_text': 'An error occurred while fetching diseases.',
                'message_debug': debug
            }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def get_diseases_by_diseaseid(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    disease_id = request.data.get('disease_id', None)

    if not disease_id:
        response_data = {'message_code': 999, 'message_text': 'Disease id is required.'}
    else:
        try:
            disease = tblMasterDisease.objects.filter(disease_id=disease_id)
            if disease.exists():
                serializer = TblMasterDiseaseSerializer(disease,many=True)
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Disease details fetched successfully.',
                    'message_data': serializer.data,
                    'message_debug': debug
                }

            else:
                response_data = {'message_code': 999, 'message_text': 'No diseases found for the given disease ID.', 'message_data': [], 'message_debug': debug}
        except tblMasterDisease.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'An error occurred while fetching diseases.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def update_disease_by_diseaseid(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    disease_id = request.data.get('disease_id', None)
    disease_data = request.data

    if not disease_id:
        response_data = {'message_code': 999, 'message_text': 'Disease id is required.'}
    elif not disease_data:
        response_data = {'message_code': 999, 'message_text': 'Disease data is required to update.'}
    else:
        try:
            disease = tblMasterDisease.objects.get(disease_id=disease_id)
            serializer = TblMasterDiseaseSerializer(disease, data=disease_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Disease details updated successfully.',
                    'message_data': serializer.data,
                    'message_debug': debug
                }
            else:
                response_data = {
                    'message_code': 999,
                    'message_text': 'Invalid data.',
                    'message_data': serializer.errors,
                    'message_debug': debug
                }
        except tblMasterDisease.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'Disease not found for the given disease ID.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def insert_allergy(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    allergy_data = request.data

    if not allergy_data:
        response_data = {'message_code': 999, 'message_text': 'Allergy data is required.'}
    else:
        try:
            serializer = TblMasterAllergySerializer(data=allergy_data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Allergy details inserted successfully.',
                    'message_data': serializer.data,
                    'message_debug': debug
                }
            else:
                response_data = {
                    'message_code': 999,
                    'message_text': 'Invalid data.',
                    'message_data': serializer.errors,
                    'message_debug': debug
                }
        except Exception as e:
            debug.append(str(e))
            response_data = {'message_code': 999, 'message_text': 'An error occurred while inserting allergy.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_allergies_by_doctorid(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    doctor_id = request.data.get('doctor_id', None)

    if not doctor_id:
        response_data = {'message_code': 999, 'message_text': 'Doctor ID is required.'}
    else:
        try:
            # allergies = tblMasterAllergies.objects.filter(Q(doctor_id=doctor_id) | Q(doctor_id__isnull=True))
            allergies = tblMasterAllergies.objects.filter((Q(doctor_id=doctor_id) | Q(doctor_id__isnull=True)) & Q(is_deleted=0)).order_by('-doctor_id')

            if allergies.exists():
                serializer = TblMasterAllergySerializer(allergies, many=True)
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Allergy details fetched successfully.',
                    'message_data': serializer.data,
                    'message_debug': debug
                }
            else:
                response_data = {'message_code': 999, 'message_text': 'No allergies found for the given doctor ID.', 'message_data': [], 'message_debug': debug}
        except Exception as e:
            debug.append(str(e))
            response_data = {'message_code': 999, 'message_text': 'An error occurred while fetching allergies.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_allergy_by_allergyid(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    allergy_id = request.data.get('allergy_id', None)

    if not allergy_id:
        response_data = {'message_code': 999, 'message_text': 'Allergy ID is required.'}
    else:
        try:
            allergy = tblMasterAllergies.objects.get(allergy_id=allergy_id, is_deleted=0)
            serializer = TblMasterAllergySerializer(allergy)
            response_data = {
                'message_code': 1000,
                'message_text': 'Allergy details fetched successfully.',
                'message_data': serializer.data,
                'message_debug': debug
            }
        except tblMasterAllergies.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'No allergy found for the given allergy ID.', 'message_data': [], 'message_debug': debug}
        except Exception as e:
            debug.append(str(e))
            response_data = {'message_code': 999, 'message_text': 'An error occurred while fetching allergy details.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def update_allergy_by_allergyid(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    allergy_id = request.data.get('allergy_id', None)
    allergy_data = request.data

    if not allergy_id:
        response_data = {'message_code': 999, 'message_text': 'Allergy ID is required.'}
    elif not allergy_data:
        response_data = {'message_code': 999, 'message_text': 'Allergy data is required to update.'}
    else:
        try:
            allergy = tblMasterAllergies.objects.get(allergy_id=allergy_id, is_deleted=0)
            serializer = TblMasterAllergySerializer(allergy, data=allergy_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Allergy details updated successfully.',
                    'message_data': serializer.data,
                    'message_debug': debug
                }
            else:
                response_data = {
                    'message_code': 999,
                    'message_text': 'Invalid data.',
                    'message_data': serializer.errors,
                    'message_debug': debug
                }
        except tblMasterAllergies.DoesNotExist:
            response_data = {'message_code': 999, 'message_text': 'Allergy not found for the given allergy ID.', 'message_debug': debug}
        except Exception as e:
            debug.append(str(e))
            response_data = {'message_code': 999, 'message_text': 'An error occurred while updating allergy details.', 'message_debug': debug}

    return Response(response_data, status=status.HTTP_200_OK)


# @api_view(["POST"])
# def insert_patient_doctor_link(request):
#     debug = []
#     response_data = {
#         'message_code': 999,
#         'message_text': 'Functional part is commented.',
#         'message_data': [],
#         'message_debug': debug
#     }

#     data = request.data

#     # Check for compulsory fields (doctor_id and patient_id)
#     doctor_id = data.get('doctor_id')
#     patient_id = data.get('patient_id')

#     if not doctor_id:
#         response_data = {'message_code': 999, 'message_text': 'Doctor ID is required.'}
#     elif not patient_id:
#         response_data = {'message_code': 999, 'message_text': 'Patient ID is required.'}
#     else:
#         # Create the PatientDoctorLink record
#         serializer = TblPatientDoctorLinkSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response_data = {
#                 'message_code': 1000,
#                 'message_text': 'Patient doctor link created successfully.',
#                 'message_data': serializer.data,
#                 'message_debug': debug
#             }

#         else:
#             response_data = {
#                 'message_code': 999,
#                 'message_text': 'Invalid data.',
#                 'message_data': serializer.errors,
#                 'message_debug': debug
#             }
        
#     return Response(response_data, status=status.HTTP_200_OK)
@api_view(["POST"])
def insert_patient_doctor_link(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    data = request.data

    # Check for compulsory fields (doctor_id and patient_id)
    doctor_id = data.get('doctor_id')
    patient_id = data.get('patient_id')

    if not doctor_id:
        response_data = {'message_code': 999, 'message_text': 'Doctor ID is required.'}
    elif not patient_id:
        response_data = {'message_code': 999, 'message_text': 'Patient ID is required.'}
    else:
        # Check if the doctor_id and patient_id combination already exists
        if tblPatientDoctorLink.objects.filter(doctor_id=doctor_id, patient_id=patient_id, is_deleted=0).exists():
            response_data = {
                'message_code': 1001,
                'message_text': 'Patient ID and Doctor ID are already linked.',
                'message_data': [],
                'message_debug': debug
            }
        else:
            # Create the PatientDoctorLink record
            serializer = TblPatientDoctorLinkSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Patient doctor link created successfully.',
                    'message_data': serializer.data,
                    'message_debug': debug
                }
            else:
                response_data = {
                    'message_code': 999,
                    'message_text': 'Invalid data.',
                    'message_data': serializer.errors,
                    'message_debug': debug
                }
        
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def get_patient_doctor_links_by_doctor_id(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    doctor_id = request.data.get('doctor_id')

    if not doctor_id:
        response_data = {'message_code': 999, 'message_text': 'Doctor ID is required.'}
    else:
        try:
            # Fetch all PatientDoctorLink records with the given doctor_id
            links = tblPatientDoctorLink.objects.filter(doctor_id=doctor_id, is_deleted=0)
            if links.exists():
                serializer = TblPatientDoctorLinkSerializer(links, many=True)
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Patient doctor links fetched successfully.',
                    'message_data': serializer.data,
                    'message_debug': debug
                }
            else:
                response_data = {
                    'message_code': 999,
                    'message_text': 'No patient doctor links found for the given doctor ID.',
                    'message_data': [],
                    'message_debug': debug
                }
        except Exception as e:
            response_data = {
                'message_code': 999,
                'message_text': 'An error occurred while fetching patient doctor links.',
                'message_debug': str(e)
            }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_patients_by_doctor_id(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    doctor_id = request.data.get('doctor_id')

    if not doctor_id:
        response_data = {'message_code': 999, 'message_text': 'Doctor ID is required.'}
    else:
        try:
            # Fetch all PatientDoctorLink records with the given doctor_id
            links = tblPatientDoctorLink.objects.filter(doctor_id=doctor_id, is_deleted=0)
            if links.exists():
                patient_ids = links.values_list('patient_id', flat=True)
                patients = Tblpatients.objects.filter(patient_id__in=patient_ids)
                serializer = TblpatientsSerializer(patients, many=True)
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Patient details fetched successfully.',
                    'message_data': serializer.data,
                    'message_debug': debug
                }
            else:
                response_data = {
                    'message_code': 999,
                    'message_text': 'No patients found for the given doctor ID.',
                    'message_data': [],
                    'message_debug': debug
                }
        except Exception as e:
            response_data = {
                'message_code': 999,
                'message_text': 'An error occurred while fetching patient details.',
                'message_debug': str(e)
            }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_patient_doctor_links_by_doctorid_patientid(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    doctor_id = request.data.get('doctor_id')
    patient_id = request.data.get('patient_id')

    if not doctor_id and not patient_id:
        response_data = {'message_code': 999, 'message_text': 'Doctor ID or Patient ID is required.'}
    else:
        try:
            
            # Fetch PatientDoctorLink records with the given filters
            links = tblPatientDoctorLink.objects.filter(patient_id=patient_id,doctor_id=doctor_id)
            if links.exists():
                serializer = TblPatientDoctorLinkSerializer(links, many=True)
                response_data = {
                    'message_code': 1000,
                    'message_text': 'Patient doctor links fetched successfully.',
                    'message_data': serializer.data,
                    'message_debug': debug
                }
            else:
                response_data = {
                    'message_code': 999,
                    'message_text': 'No patient doctor links found for the given IDs.',
                    'message_data': [],
                    'message_debug': debug
                }
        except Exception as e:
            response_data = {
                'message_code': 999,
                'message_text': 'An error occurred while fetching patient doctor links.',
                'message_debug': str(e)
            }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def update_patient_doctor_link_by_doctorid_patientid(request):
    # Initialize the response dictionary
    response_data = {
        'message_code': 999,
        'message_text': 'Something went wrong.',
        'message_data': [],
        'message_debug': []
    }
    
    # Extract patient_id and doctor_id from the request data
    patient_id = request.data.get('patient_id')
    doctor_id = request.data.get('doctor_id')

    if not patient_id or not doctor_id:
        response_data['message_text'] = 'Patient ID and Doctor ID are required.'
    else:
        try:
            # Fetch the PatientDoctorLink record
            link = tblPatientDoctorLink.objects.get(patient_id=patient_id, doctor_id=doctor_id)
            # Deserialize and validate the incoming data
            serializer = TblPatientDoctorLinkSerializer(link, data=request.data, partial=True)
            
            if serializer.is_valid():
                # Save the updated record
                serializer.save()
                response_data['message_code'] = 1000
                response_data['message_text'] = 'PatientDoctorLink updated successfully.'
                response_data['message_data'] = serializer.data
            else:
                response_data['message_text'] = 'Invalid data.'
                response_data['message_debug'] = serializer.errors
        except tblPatientDoctorLink.DoesNotExist:
            response_data['message_text'] = 'PatientDoctorLink not found.'
        except Exception as e:
            response_data['message_text'] = 'An error occurred while updating the PatientDoctorLink.'
            response_data['message_debug'] = str(e)

    return Response(response_data, status=status.HTTP_200_OK)


# @api_view(["POST"])
# def insert_patient_allergies(request):
#     debug = []
#     response_data = {
#         'message_code': 999,
#         'message_text': 'Functional part is commented.',
#         'message_data': [],
#         'message_debug': debug
#     }

#     data = request.data

#     # Check for compulsory fields (patient_id and allergy_id)
#     patient_id = data.get('patient_id')
#     allergy_id = data.get('allergy_id')

#     if not patient_id:
#         response_data = {'message_code': 999, 'message_text': 'Patient ID is required.'}
#     elif not allergy_id:
#         response_data = {'message_code': 999, 'message_text': 'Allergy ID is required.'}
#     else:
#         # Create the PatientAllergies record
#         serializer = TblPatientAllergySerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response_data = {
#                 'message_code': 1000,
#                 'message_text': 'Patient allergy details inserted successfully.',
#                 'message_data': serializer.data,
#                 'message_debug': debug
#             }
#         else:
#             response_data = {
#                 'message_code': 999,
#                 'message_text': 'Invalid data.',
#                 'message_data': serializer.errors,
#                 'message_debug': debug
#             }
        
#     return Response(response_data, status=status.HTTP_200_OK)
@api_view(["POST"])
def insert_patient_allergies(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    data = request.data

    # Check for compulsory fields (patient_id and allergy_id)
    patient_id = data.get('patient_id')
    allergy_id = data.get('allergy_id')

    if not patient_id:
        response_data = {'message_code': 999, 'message_text': 'Patient ID is required.'}
    elif not allergy_id:
        response_data = {'message_code': 999, 'message_text': 'Allergy ID is required.'}
    else:
        # Set the current epoch time as allergy_entry_date
        data['allergy_entry_date'] = int(time.time())

        # Create the PatientAllergies record
        serializer = TblPatientAllergySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message_code': 1000,
                'message_text': 'Patient allergy details inserted successfully.',
                'message_data': serializer.data,
                'message_debug': debug
            }
        else:
            response_data = {
                'message_code': 999,
                'message_text': 'Invalid data.',
                'message_data': serializer.errors,
                'message_debug': debug
            }
        
    return Response(response_data, status=status.HTTP_200_OK)


# @api_view(["POST"])
# def get_patient_allergies_by_patientid(request):
#     debug = []
#     response_data = {
#         'message_code': 999,
#         'message_text': 'Functional part is commented.',
#         'message_data': [],
#         'message_debug': debug
#     }

#     patient_id = request.data.get('patient_id')

#     if not patient_id:
#         response_data = {'message_code': 999, 'message_text': 'Patient ID is required in the request body.'}
#         return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

#     allergies = tblPatientAllergies.objects.filter(patient_id=patient_id, is_deleted=0)

#     if allergies.exists():
#         serializer = TblPatientAllergySerializer(allergies, many=True)
#         response_data = {
#             'message_code': 1000,
#             'message_text': 'Patient allergies details retrieved successfully.',
#             'message_data': serializer.data,
#             'message_debug': debug
#         }
#     else:
#         response_data = {
#             'message_code': 999,
#             'message_text': 'Patient allergies not found for the given ID.',
#             'message_data': [],
#             'message_debug': debug
#         }

#     return Response(response_data, status=status.HTTP_200_OK)
@api_view(["POST"])
def get_patient_allergies_by_patientid(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    patient_id = request.data.get('patient_id')

    if not patient_id:
        response_data = {'message_code': 999, 'message_text': 'Patient ID is required in the request body.'}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    allergies = tblPatientAllergies.objects.filter(patient_id=patient_id, is_deleted=0)

    if allergies.exists():
        serializer = TblPatientAllergySerializer(allergies, many=True)
        allergies_data = serializer.data

        # Add allergy name to each record
        for allergy in allergies_data:
            allergy_id = allergy.get('allergy_id')
            try:
                allergy_name = tblMasterAllergies.objects.get(allergy_id=allergy_id).allergy_name
            except tblMasterAllergies.DoesNotExist:
                allergy_name = None
            allergy['allergy_name'] = allergy_name

        response_data = {
            'message_code': 1000,
            'message_text': 'Patient allergies details retrieved successfully.',
            'message_data': allergies_data,
            'message_debug': debug
        }
    else:
        response_data = {
            'message_code': 999,
            'message_text': 'Patient allergies not found for the given ID.',
            'message_data': [],
            'message_debug': debug
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def insert_patient_diseases(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    data = request.data

    # Check for compulsory fields (patient_id and disease_id)
    patient_id = data.get('patient_id')
    disease_id = data.get('disease_id')

    if not patient_id:
        response_data = {'message_code': 999, 'message_text': 'Patient ID is required.'}
    elif not disease_id:
        response_data = {'message_code': 999, 'message_text': 'Disease ID is required.'}
    else:
        # Set the current epoch time as disease_entry_date
        data['disease_entry_date'] = int(time.time())

        # Create the PatientDisease record
        serializer = TblPatientDiseaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message_code': 1000,
                'message_text': 'Patient disease details inserted successfully.',
                'message_data': serializer.data,
                'message_debug': debug
            }
        else:
            response_data = {
                'message_code': 999,
                'message_text': 'Invalid data.',
                'message_data': serializer.errors,
                'message_debug': debug
            }
        
    return Response(response_data, status=status.HTTP_200_OK)

# @api_view(["POST"])
# def get_patient_diseases_by_patientid(request):
#     debug = []
#     response_data = {
#         'message_code': 999,
#         'message_text': 'Functional part is commented.',
#         'message_data': [],
#         'message_debug': debug
#     }

#     patient_id = request.data.get('patient_id')

#     if not patient_id:
#         response_data = {'message_code': 999, 'message_text': 'Patient ID is required in the request body.'}
#         return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

#     diseases = tblPatientDisease.objects.filter(patient_id=patient_id, is_deleted=0)

#     if diseases.exists():
#         serializer = TblPatientDiseaseSerializer(diseases, many=True)
#         response_data = {
#             'message_code': 1000,
#             'message_text': 'Patient diseases details retrieved successfully.',
#             'message_data': serializer.data,
#             'message_debug': debug
#         }
#     else:
#         response_data = {
#             'message_code': 999,
#             'message_text': 'Patient diseases not found for the given ID.',
#             'message_data': [],
#             'message_debug': debug
#         }

#     return Response(response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def get_patient_diseases_by_patientid(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    patient_id = request.data.get('patient_id')

    if not patient_id:
        response_data = {'message_code': 999, 'message_text': 'Patient ID is required in the request body.'}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    diseases = tblPatientDisease.objects.filter(patient_id=patient_id, is_deleted=0)

    if diseases.exists():
        serializer = TblPatientDiseaseSerializer(diseases, many=True)
        diseases_data = serializer.data

        # Add disease name to each record
        for disease in diseases_data:
            disease_id = disease.get('disease_id')
            try:
                disease_name = tblMasterDisease.objects.get(disease_id=disease_id).disease_name
            except tblMasterDisease.DoesNotExist:
                disease_name = None
            disease['disease_name'] = disease_name

        response_data = {
            'message_code': 1000,
            'message_text': 'Patient diseases details retrieved successfully.',
            'message_data': diseases_data,
            'message_debug': debug
        }
    else:
        response_data = {
            'message_code': 999,
            'message_text': 'Patient diseases not found for the given ID.',
            'message_data': [],
            'message_debug': debug
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def delete_patient_allergy(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    patient_allergy_id = request.data.get('patient_allergy_id')

    if not patient_allergy_id:
        response_data['message_text'] = 'patient_allergy_id is required in the request body.'
        response_data['message_code'] = 999
    else:
        try:
            allergy = tblPatientAllergies.objects.get(patient_allergy_id=patient_allergy_id)
            allergy.is_deleted = 1
            allergy.save()
            response_data['message_code'] = 1000
            response_data['message_text'] = 'Allergy marked as deleted successfully.'
        except tblPatientAllergies.DoesNotExist:
            response_data['message_code'] = 999
            response_data['message_text'] = 'Allergy not found for the given ID.'
        except Exception as e:
            response_data['message_code'] = 999
            response_data['message_text'] = str(e)

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def delete_patient_disease(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    patient_disease_id = request.data.get('patient_disease_id')

    if not patient_disease_id:
        response_data['message_text'] = 'patient_disease_id is required in the request body.'
        response_data['message_code'] = 999
    else:
        try:
            disease = tblPatientDisease.objects.get(patient_disease_id=patient_disease_id)
            disease.is_deleted = 1
            disease.save()
            response_data['message_code'] = 1000
            response_data['message_text'] = 'Disease marked as deleted successfully.'
        except tblPatientDisease.DoesNotExist:
            response_data['message_code'] = 999
            response_data['message_text'] = 'Disease not found for the given ID.'
        except Exception as e:
            response_data['message_code'] = 999
            response_data['message_text'] = str(e)

    return Response(response_data, status=status.HTTP_200_OK)



#################Api to get patient details through appointment id
@api_view(['POST'])
def get_patient_details_by_appointment_id(request):
    debug = []
    response_data = {
        'message_code': 999,
        'message_text': 'Functional part is commented.',
        'message_data': [],
        'message_debug': debug
    }

    appointment_id = request.data.get('appointment_id')

    if not appointment_id:
        response_data['message_text'] = 'appointment_id is required in the request body.'
        response_data['message_code'] = 999
    else:
        try:
            # Fetch the patient vitals record associated with the appointment ID
            patient_vitals = Tblpatientvitals.objects.get(appointment_id=appointment_id, isdeleted=0)
            patient_id = patient_vitals.patient_id
            
            # Fetch the patient details
            patient = Tblpatients.objects.get(patient_id=patient_id.patient_id, isdeleted=0)
            
            # Serialize the patient details
            serializer = TblPatientsSerializer(patient)
            response_data['message_code'] = 1000
            response_data['message_text'] = 'Patient details fetched successfully.'
            response_data['message_data'] = serializer.data
            
        except Tblpatientvitals.DoesNotExist:
            response_data['message_code'] = 999
            response_data['message_text'] = 'No patient vitals found for the given appointment ID.'
        except Tblpatients.DoesNotExist:
            response_data['message_code'] = 999
            response_data['message_text'] = 'No patient found for the given patient ID.'
        except Exception as e:
            response_data['message_code'] = 999
            response_data['message_text'] = str(e)
            debug.append(str(e))

    return Response(response_data, status=status.HTTP_200_OK)