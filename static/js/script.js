document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("startRoutine").addEventListener("click", initRoutine);
    document.getElementById("nextTask").addEventListener("click", getNextTask);
    document.getElementById("showUndone").addEventListener("click", showUndoneTasks);
});

function initRoutine() {
    const taskCount = document.getElementById('taskCount').value;
    fetch('/init_routine', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({desired_number_of_tasks: parseInt(taskCount)})
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('messageDisplay').textContent = 'Initialization Error: ' + data.error;
        } else {
            document.getElementById('messageDisplay').textContent = 'Initialization Successful: ' + data.message;
            updateUndoneTasksDisplay(data.undone_tasks);
        }
    })
    .catch(error => {
        console.error('Error initializing the routine:', error);
        document.getElementById('messageDisplay').textContent = 'Failed to initialize the routine.';
    });
}

function getNextTask() {
    fetch('/get_next_task')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('task').textContent = 'Error: ' + data.error;
            } else if (data.task === '') { // Assuming an empty string is returned when no tasks are left
                document.getElementById('notification').textContent = 'No more tasks left.';
            } else {
                document.getElementById('task').textContent = 'Next Task: ' + data.task;
                updateUndoneTasksDisplay(data.undone_tasks);
            }
        })
        .catch(error => {
            console.error('Error fetching the next task:', error);
            document.getElementById('task').textContent = 'Failed to fetch the next task.';
        });
}

function updateUndoneTasksDisplay(undoneTasks) {
    let tasksContent = '<div class="task-list"><strong>Remaining Tasks:</strong> ' +
                       undoneTasks.remaining_tasks.join(', ') + '</div>' +
                       '<div class="task-list"><strong>Not Selected Tasks:</strong> ' +
                       undoneTasks.not_selected_tasks.join(', ') + '</div>';
    document.getElementById('undoneTasksDisplay').innerHTML = tasksContent;
}




