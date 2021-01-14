import './App.css';
import React from "react";
import * as Sentry from '@sentry/react';
import { ToastContainer, toast } from 'react-toastify';

  import 'react-toastify/dist/ReactToastify.css';

function FallbackComponent() {
  return (
    <div>An error has occured</div>
  )
}

function App() {

    const deliveryPlannerAppUrl = `${process.env.REACT_APP_DELIVERY_PLANNER_APP_URL}`;

    const uploadExternalTasksUrl = `${deliveryPlannerAppUrl}/upload_external_tasks`

    const uploadExternalTasks = (params: {externalTasksFile: File}) => {
        const externalTasksFormData = new FormData()
        externalTasksFormData.append('external_tasks_file', params.externalTasksFile)

        fetch(uploadExternalTasksUrl, {
            method: 'PUT',
            body: externalTasksFormData
        })
            .then((response) => {
                if (response.ok) {
                    alert('Загружено')
                } else {
                    alert('Ошибка')
                    throw new Error('Error uploading external tasks file')
                }
            })
            .then((data) => {
            })
            .catch(error => {
                Sentry.captureException(error);
            })
    }

    const planDeliveryUrl = `${deliveryPlannerAppUrl}/plan_delivery`

    const makeBrowserDownloadPlan = (params: {fileContents: Blob}) => {
        const url = window.URL.createObjectURL(params.fileContents)
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'plan_output.xlsx')
        document.body.appendChild(link)
        link.click()
        link.parentNode.removeChild(link)
    }

    const planDelivery = (params: {deliveryPlanFile: File}) => {
        const deliveryPlanFormData = new FormData()
        deliveryPlanFormData.append('plan_file', params.deliveryPlanFile)

        fetch(planDeliveryUrl, {
            method: 'POST',
            body: deliveryPlanFormData
        })
            .then((response) => {
                if (response.ok) {
                    return response.blob()
                }

                throw response
            }
        )
            .then((blob) => {
                makeBrowserDownloadPlan({fileContents: blob})
            })
            .catch(error => {
                console.error(error)

                error.json().then (
                    (json) => {
                        console.log(json.detail)
                        toast.error(json.detail)
                    }
                )
            })
    }

    const prepareInputForNextUpload= (params: {input: any}) => {
        params.input.value = null
    }

    return (
        <Sentry.ErrorBoundary fallback={FallbackComponent} showDialog>
            <div className="App">
                {/* <input type="file" id="externalTasksFileInput" onChange={(e) => uploadExternalTasks({externalTasksFile: e.target.files[0]})}/> */}

                Загрузите файл
                <input
                    style={{marginTop: 100}}
                    type="file"
                    id="deliveryPlanFileInput"
                    onChange={
                        (e) => {
                            planDelivery({deliveryPlanFile: e.target.files[0]})
                            prepareInputForNextUpload({input: e.target})
                        }
                    }
                />
                <ToastContainer />
            </div>
        </Sentry.ErrorBoundary>
    );
}

export default App;
