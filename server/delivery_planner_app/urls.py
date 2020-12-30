from django.urls import path, re_path

from . import views
from .views import ExternalTasksUploadView, PlanDeliveryView

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_external_tasks', ExternalTasksUploadView.as_view(), name='upload_external_tasks'),
    path('plan_delivery', PlanDeliveryView.as_view(), name='plan_delivery')
]