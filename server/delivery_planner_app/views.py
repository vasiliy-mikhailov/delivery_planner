import io
from wsgiref.util import FileWrapper

from django.http import HttpResponse

# Create your views here.
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from Interactors.CopyExternalTasksBetweenRepositories import CopyExternalTasksBetweenRepositories
from Interactors.PlannerInteractor.PlannerInteractor import PlannerInteractor
from Presenters.ExcelPlanPresenter.ExcelPlanPresenter import ExcelPlanPresenter
from Repository.ExcelPlanReader import ExcelPlanReader
from Repository.ExternalTaskRepository.DbExternalTaskRepository import DbExternalTaskRepository
from Repository.ExternalTaskRepository.ExcelExternalTaskRepository import ExcelExternalTaskRepository


def index(request):
    return HttpResponse("Hello, world. You're at the delivery planner index.")

class ExternalTasksUploadView(APIView):
    parser_classes = [MultiPartParser]

    def put(self, request):
        external_tasks_file = request.data['external_tasks_file']

        source_repository = ExcelExternalTaskRepository(
            file_name_or_io=external_tasks_file
        )
        destination_repository = DbExternalTaskRepository()
        convert_excel_external_tasks_to_db_external_tasks_interactor = CopyExternalTasksBetweenRepositories(
            source_repository=source_repository,
            destination_repository=destination_repository
        )

        convert_excel_external_tasks_to_db_external_tasks_interactor.interact()

        return Response(status=200)

class PlanDeliveryView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        plan_file = request.data['plan_file']
        reader = ExcelPlanReader(file_name_or_io=plan_file)
        plan_input = reader.read()
        external_task_repository = DbExternalTaskRepository()
        planner = PlannerInteractor(plan_input=plan_input, external_task_repository=external_task_repository)
        plan_output = planner.interact()

        output = io.BytesIO()
        presenter = ExcelPlanPresenter(report_file_name_or_io=output, plan_output=plan_output)
        _ = presenter.present()
        output.seek(0)

        response = HttpResponse(FileWrapper(output))
        response['Content-Disposition'] = 'attachment; filename="plan_output.xlsx"'
        return response