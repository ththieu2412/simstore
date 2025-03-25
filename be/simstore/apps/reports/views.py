from django.utils.timezone import now
from django.db.models import Sum, Count
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.simcards.models import SIM
from rest_framework import status

# Create your views here.
class MonthlyRevenueReport(APIView):
    def get(self, request, *args, **kwargs):
        month = request.query_params.get('month', now().month)
        year = request.query_params.get('year', now().year)

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": "Tháng và năm phải là số nguyên!"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not (1 <= month <= 12):
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": "Tháng phải nằm trong khoảng 1-12!"
            }, status=status.HTTP_400_BAD_REQUEST)

        sold_sims = SIM.objects.filter(
            status=0,
            updated_at__year=year,
            updated_at__month=month
        )

        report = sold_sims.aggregate(
            total_revenue=Sum('export_price'),
            total_sims_sold=Count('id')
        )

        # Lấy danh sách mã SIM đã bán
        sold_sim_codes = sold_sims.values_list('id', flat=True)  

        data = {
            "year": year,
            "month": month,
            "total_revenue": report["total_revenue"] or 0,
            "total_sims_sold": report["total_sims_sold"] or 0,
            "sold_sim_codes": list(sold_sim_codes)  # Chuyển QuerySet thành list
        }

        return Response({
            "statuscode": status.HTTP_200_OK,
            "data": data,
            "status": "success",
            "errorMessage": None
        }, status=status.HTTP_200_OK)
