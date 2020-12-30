import './App.css';

function App() {
    const uploadExternalTasks = (external_tasks_files: FileList) => {
        const externalTasksFormData = new FormData()
        const externalTasksFile = external_tasks_files[0]
        externalTasksFormData.append('external_tasks_file', externalTasksFile)
        fetch('http://localhost:8000/delivery_planner_app/upload_external_tasks', {
            method: 'PUT',
            body: externalTasksFormData
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
            })
            .catch(error => {
                console.error(error)
            })
    }

    return (
        <div className="App">
            <input type="file" id="externalTasksFileInput" onChange={(e) => uploadExternalTasks(e.target.files)}/>
        </div>
    );
}

export default App;
