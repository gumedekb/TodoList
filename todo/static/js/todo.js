function changeColor(clickedDiv) {
    clickedDiv.style.backgroundColor = 'green'; // Change the color of the clicked div to red
}


// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Attach an event listener to each checkbox
    document.querySelectorAll('.todo-status-checkbox').forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            let todoId = this.closest('form').getAttribute('data-todo-id');
            let status = this.checked ? 'on' : 'off';  // Get the status of the checkbox

            // Send an AJAX request to update the task's status
            let formData = new FormData();
            formData.append('srno', todoId);
            formData.append('status', status);
            formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
            console.log("Update Task URL: ", updateTaskUrl);

            // Make the AJAX request
            fetch(updateTaskUrl, {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        console.log('Status update success:', data);
                        // Optionally, update the task's visual status (color changes)
                        let taskDiv = checkbox.closest('.Todo');
                        console.log(taskDiv);

                        if (data.new_status) {
                            console.log('Setting to green');
                            taskDiv.classList.add('todo-green');
                            taskDiv.classList.remove('todo-red');
                        } else {
                            console.log('Setting to red');
                            taskDiv.classList.add('todo-red');
                            taskDiv.classList.remove('todo-green');
                        }
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });
});