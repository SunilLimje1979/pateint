# from rest_framework import serializers
# from .models import TblpateintCharges, TblpatientPayments

# from .models import TblpatientPayments,Tblpatients

# ######################### Patient Charges ############################   
# class PatientChargesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TblpateintCharges
#         fields = '__all__'
        
# ######################### Patient Charges ############################           
# class TblpatientPaymentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TblpatientPayments
#         fields = '__all__'


# class TblpatientsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tblpatients
#         fields = '__all__'

# class TblpatientPaymentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TblpatientPayments
#         fields = ['doctor_id', 'patient_id', 'patient_status', 'payment_mode', 'payment_amount', 'payment_transaction_no','isdeleted']
