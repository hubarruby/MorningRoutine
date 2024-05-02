from flask import Blueprint, jsonify, request, session, render_template, current_app
from .random_morning_routine import RandomMorningRoutine

main = Blueprint('main', __name__)

# Initialize with default values
tasks = ['Shower', 'Make Breakfast', 'Tracking Sheet', 'Journal', 'Pullups', 'Read', '5-10 Mins Cleaning', 'Pushups (1)', 'Pushups (2)', 'Brush Teeth', 'Go for a Walk', 'Pack Bag/Lunch', 'Meditate Outside', 'Quick Yoga Session', "Stretch"]
required_tasks = ['Tracking Sheet', 'Brush Teeth', 'Make Breakfast', 'Pack Bag/Lunch', 'Pushups (1)', 'Pushups (2)', 'Shower', 'Journal']


@main.route('/')
def home():
    min_tasks = len(required_tasks)
    max_tasks = len(tasks)
    return render_template('index.html', min_tasks=min_tasks, max_tasks=max_tasks)


@main.route('/init_routine', methods=['POST'])
def init_routine():
    data = request.get_json()
    desired_number_of_tasks = data.get('desired_number_of_tasks', len(required_tasks))
    if desired_number_of_tasks < len(required_tasks) or desired_number_of_tasks > len(tasks):
        return jsonify({'error': 'Invalid number of tasks requested'}), 400
    routine = RandomMorningRoutine(tasks, desired_number_of_tasks, required_tasks)
    session['routine'] = routine.to_dict()  # Store the routine as a dictionary
    undone_tasks = routine.get_undone_tasks()  # Fetch undone tasks right after initialization
    return jsonify({'message': 'Routine initialized', 'undone_tasks': undone_tasks}), 200

@main.route('/get_next_task', methods=['GET'])
def get_next_task():
    routine_data = session.get('routine')
    if routine_data is None:
        return jsonify({'error': 'Routine not initialized'}), 400
    routine = RandomMorningRoutine.from_dict(routine_data)
    if routine.index >= len(routine.selected_tasks):
        undone_tasks = routine.get_undone_tasks()  # Fetch undone tasks if no more tasks available
        return jsonify({'task': '', 'undone_tasks': undone_tasks})
    task = routine.get_next_task()
    session['routine'] = routine.to_dict()
    undone_tasks = routine.get_undone_tasks()  # Also include undone tasks with each task fetch
    return jsonify({'task': task, 'undone_tasks': undone_tasks})


@main.route('/undone_tasks', methods=['GET'])
def undone_tasks():
    routine_data = session.get('routine')
    if routine_data is None:
        return jsonify({'error': 'Routine not initialized'}), 400

    routine = RandomMorningRoutine.from_dict(routine_data)
    undone_tasks_info = routine.get_undone_tasks()

    return jsonify(undone_tasks=undone_tasks_info)


