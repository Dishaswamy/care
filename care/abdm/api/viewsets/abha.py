from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from care.abdm.api.serializers.abha import AbhaSerializer
from care.abdm.models import AbhaNumber
from care.abdm.utils.api_call import HealthIdGateway
from care.utils.queryset.patient import get_patient_queryset


class AbhaViewSet(GenericViewSet):
    serializer_class = AbhaSerializer
    model = AbhaNumber
    queryset = AbhaNumber.objects.all()

    def get_abha_object(self):
        queryset = get_patient_queryset(self.request.user)
        print(
            "Finding patient with external_id: ", self.kwargs.get("patient_external_id")
        )
        patient_obj = get_object_or_404(
            queryset.filter(external_id=self.kwargs.get("patient_external_id"))
        )
        return patient_obj.abha_number

    @action(detail=False, methods=["GET"])
    def get_qr_code(self, request, *args, **kwargs):
        obj = self.get_abha_object()
        gateway = HealthIdGateway()
        # Empty Dict as data, obj.access_token as auth
        response = gateway.get_qr_code(obj)
        return Response(response)
