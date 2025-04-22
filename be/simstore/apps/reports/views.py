from django.utils.timezone import now
from django.db.models import Sum, Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from apps.simcards.models import SIM
from apps.suppliers.models import ImportReceiptDetail
from apps.orders.models import DetailUpdateOrder
from datetime import datetime
from apps.orders.constants import ORDER_STATUS_COMPLETED


class MonthlyRevenueReportViewSet(ViewSet):
    @action(detail=False, methods=['get'], url_path='revenue')
    def revenue(self, request):
        return self._process_report(request, 'revenue')

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        return self._process_report(request, 'summary')

    def _process_report(self, request, action):
        try:
            month = request.query_params.get('month', str(now().month))
            year = request.query_params.get('year', str(now().year))
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')

            if start_date and end_date:
                try:
                    start = datetime.strptime(start_date, '%Y-%m-%d')
                    end = datetime.strptime(end_date, '%Y-%m-%d')
                    if start > end:
                        return self._error_response(
                            status.HTTP_400_BAD_REQUEST,
                            "Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc!"
                        )
                except ValueError:
                    return self._error_response(
                        status.HTTP_400_BAD_REQUEST,
                        "Định dạng ngày không hợp lệ! Sử dụng YYYY-MM-DD"
                    )
                sold_sims = SIM.objects.filter(
                    orders__detailupdateorder__status_updated= ORDER_STATUS_COMPLETED,
                    orders__detailupdateorder__updated_at__range=(start, end)
                ).prefetch_related('importReceiptDetail').distinct()
                period_label = f"{start.strftime('%d-%m-%Y')} to {end.strftime('%d-%m-%Y')}"
            else:
                try:
                    month = int(month)
                    year = int(year)
                    if not (1 <= month <= 12):
                        return self._error_response(
                            status.HTTP_400_BAD_REQUEST,
                            "Tháng phải nằm trong khoảng 1-12!"
                        )
                except ValueError:
                    return self._error_response(
                        status.HTTP_400_BAD_REQUEST,
                        "Tháng và năm phải là số nguyên!"
                    )
                sold_sims = SIM.objects.filter(
                    orders__detailupdateorder__status_updated=ORDER_STATUS_COMPLETED,
                    orders__detailupdateorder__updated_at__year=year,
                    orders__detailupdateorder__updated_at__month=month
                ).prefetch_related('importReceiptDetail').distinct()
                period_label = f"{month:02d}-{year}"

            if not sold_sims.exists():
                data = self._empty_data(period_label)
                return self._success_response(data)

            if action == 'revenue':
                data = self._get_revenue_report(sold_sims, period_label)
            elif action == 'summary':
                data = self._get_summary_report(sold_sims, period_label)
            return self._success_response(data)

        except Exception as e:
            return self._error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                str(e)
            )

    def _error_response(self, status_code, message):
        """Helper method để tạo response lỗi"""
        return Response({
            "statuscode": status_code,
            "data": None,
            "status": "error",
            "errorMessage": message
        }, status=status_code)

    def _success_response(self, data):
        """Helper method để tạo response thành công"""
        return Response({
            "statuscode": status.HTTP_200_OK,
            "data": data,
            "status": "success",
            "errorMessage": None
        }, status=status.HTTP_200_OK)

    def _empty_data(self, period_label):
        """Trả về dữ liệu mặc định khi không có SIM nào"""
        return {
            "period": period_label,
            "total_revenue": 0.0,
            "total_sims_sold": 0,
            "sold_sim_codes": [],
            "total_cost": 0.0,
            "total_profit": 0.0,
            "details": []
        }

    def _get_revenue_report(self, sold_sims, period_label):
        """Xử lý báo cáo doanh thu chi tiết"""
        report = sold_sims.aggregate(
            total_revenue=Sum('export_price'),
            total_cost=Sum('importReceiptDetail__import_price'), 
            total_sims_sold=Count('id')
        )

        details = []
        for sim in sold_sims:
            print(f"=========================================")  # Debugging line
            print(f"Processing SIM: {sim.phone_number}")  # Debugging line
            import_receipt_detail = sim.importReceiptDetail.first() 
            detail_update_order = DetailUpdateOrder.objects.filter(
                order__in=sim.orders.all(),
                status_updated=3
            ).first()  #
            print(f"DetailUpdateOrder: {detail_update_order}")  # Debugging line
            print(f"ImportReceiptDetail: {import_receipt_detail}")  # Debugging line
            if import_receipt_detail:
                details.append({
                    'phone_number': sim.phone_number,
                    'import_price': float(import_receipt_detail.import_price),
                    'export_price': float(sim.export_price),
                    'profit': float(sim.export_price - import_receipt_detail.import_price),
                    'sold_date': detail_update_order.updated_at.strftime('%d-%m-%Y %H:%M:%S') if detail_update_order else None
                })

        return {
            "period": period_label,
            "total_revenue": float(report["total_revenue"] or 0),
            "total_cost": float(report["total_cost"] or 0),
            "total_profit": float((report["total_revenue"] or 0) - (report["total_cost"] or 0)),
            "total_sims_sold": report["total_sims_sold"] or 0,
            "sold_sim_codes": list(sold_sims.values_list('id', flat=True)),
            "details": details
        }

    def _get_summary_report(self, sold_sims, period_label):
        """Xử lý báo cáo tổng hợp"""
        report = sold_sims.aggregate(
            total_revenue=Sum('export_price'),
            total_sims_sold=Count('id')
        )

        return {
            "period": period_label,
            "total_revenue": float(report["total_revenue"] or 0),
            "total_sims_sold": report["total_sims_sold"] or 0,
            "sold_sim_codes": list(sold_sims.values_list('id', flat=True))
        }

