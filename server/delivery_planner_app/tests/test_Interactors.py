from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from Interactors.CopyExternalTasksBetweenRepositories import \
    CopyExternalTasksBetweenRepositories
from Repository.ExternalTaskRepository.DbExternalTaskRepository import DbExternalTaskRepository
from Repository.ExternalTaskRepository.ExcelExternalTaskRepository import ExcelExternalTaskRepository
import pandas as pd


class InteractorsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_convert_excel_external_tasks_to_db_external_tasks(self):
        source_repository = ExcelExternalTaskRepository(
            file_name_or_io='./delivery_planner_app/tests/input_excels/external_tasks.xlsx')
        destination_repository = DbExternalTaskRepository()
        convert_excel_external_tasks_to_db_external_tasks_interactor = CopyExternalTasksBetweenRepositories(
            source_repository=source_repository,
            destination_repository=destination_repository
        )

        convert_excel_external_tasks_to_db_external_tasks_interactor.interact()

        source_external_tasks = source_repository.get_all()
        destination_external_tasks = destination_repository.get_all()

        self.assertTrue(len(source_external_tasks), len(destination_external_tasks))

        for external_task in source_external_tasks:
            self.assertTrue(external_task in destination_external_tasks)

    def test_upload_external_tasks_through_rest_api(self):
        external_tasks_file_name = './delivery_planner_app/tests/input_excels/external_tasks.xlsx'
        with open(external_tasks_file_name, 'rb') as external_tasks_file:
            external_tasks_uploaded_file = SimpleUploadedFile(name="external_tasks.xlsx", content=external_tasks_file.read())
            response = self.client.put(
                path=reverse('upload_external_tasks'),
                data={'external_tasks_file': external_tasks_uploaded_file},
                format='multipart'
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        source_repository = ExcelExternalTaskRepository(file_name_or_io=external_tasks_file_name)
        destination_repository = DbExternalTaskRepository()
        source_external_tasks = source_repository.get_all()
        destination_external_tasks = destination_repository.get_all()

        self.assertTrue(len(source_external_tasks), len(destination_external_tasks))

        for external_task in source_external_tasks:
            self.assertTrue(external_task in destination_external_tasks)

    def test_plan_delivery_through_rest_api(self):
        plan_file_name = './delivery_planner_app/tests/input_excels/plan.xlsx'
        with open(plan_file_name, 'rb') as plan_file:
            plan_uploaded_file = SimpleUploadedFile(name="plan.xlsx", content=plan_file.read())
            response = self.client.post(
                path=reverse('plan_delivery'),
                data={'plan_file': plan_uploaded_file},
                format='multipart'
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        excel_plan_output = response.content

        pd.read_excel(excel_plan_output, sheet_name='out_Ресурсно-календарный план')





