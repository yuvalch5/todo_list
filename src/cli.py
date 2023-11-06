import typer
from src.sqlite_manage import TasksNew, session
from datetime import datetime
from sqlalchemy import and_
from tabulate import tabulate

# Valid priority levels: 1 - Low, 2 - Medium, 3- High
valid_priorities = [1, 2, 3]

app = typer.Typer()


# Add a new task to the DB by running in the command line (from venv): 'python3 main.py add'
@app.command()
def add():
    task_name = typer.prompt("Enter task name")
    task_priority = 0
    while task_priority < 1 or task_priority > 3:
        task_priority = int(typer.prompt("Enter task priority (1 - Low, 2 - Medium, 3 - High)"))
        if task_priority < 1 or task_priority > 3:
            print(f"{task_priority} is an invalid priority, try again.")
    new_task = TasksNew(name=task_name, created_time=datetime.now(), priority=task_priority, completed=0)
    session.add(new_task)
    session.commit()
    session.close()


# Mark the task as completed in the DB by running in the command line (from venv): 'python3 main.py complete'
@app.command()
def complete():
    keep_prompt = True
    all_id = [task.id for task in session.query(TasksNew)]
    while keep_prompt:
        completed_id = typer.prompt("Enter the ID number of the task you completed")
        if completed_id not in all_id and not completed_id.isdigit():
            typer.echo("Task ID does not exist.")
        else:
            keep_prompt = False
    task_to_complete = session.query(TasksNew).filter(TasksNew.id == completed_id).first()
    task_to_complete.completed_time = datetime.now()
    task_to_complete.completed = 1
    session.commit()
    session.close()


# Print a list of uncompleted tasks from a priority group by running in the command line (from venv):
# 'python3 main.py printpri <priority_number>'
@app.command()
def printpri(priority_num: int):
    if priority_num not in valid_priorities:
        typer.echo(f"{priority_num} is an invalid priority level. Valid priority levels: 1 - Low, 2 - Medium, 3 - High")
        return

    if priority_num == 1:
        priority_name = "LOW"
    elif priority_num == 2:
        priority_name = "MEDIUM"
    elif priority_num == 3:
        priority_name = "HIGH"

    priority_condition = TasksNew.priority == priority_num
    completed_condition = TasksNew.completed == 0
    combined_conditions = and_(completed_condition, priority_condition)
    # Filter out all the unmatching priorities
    pri_tasks = session.query(TasksNew).filter(combined_conditions)
    pri_tasks_list = list(pri_tasks)
    # Create a list for tabulate that does not include the 'priority column'
    list_for_tabulate = []
    for task in pri_tasks_list:
        list_for_tabulate.append([task.id, task.name, task.created_time])
    table_style = "grid"
    pri_table = tabulate(list_for_tabulate,
                         headers=["TASK ID", "NAME", "CREATION DATE"],
                         tablefmt=table_style,
                         colalign=("center", "center", "center"))
    typer.echo(f"{priority_name} PRIORITY TABLE:\n{pri_table}")


# Changes the priority level of a task
# Use it this way: python3 main.py <id_of_task_to_change> <new_priority_level>
@app.command()
def mvpri(id_for_change: int, new_pri: int):
    pri_tasks = [task_id[0] for task_id in session.query(TasksNew.id).all()]
    if id_for_change not in pri_tasks:
        print(f"There is no task with ID: {id_for_change}")
        return
    if new_pri not in valid_priorities:
        typer.echo(f"{new_pri} is an invalid priority level. Valid priority levels: 1 - Low, 2 - Medium, 3 - High")
        return

    if new_pri == 1:
        priority_name = "LOW"
    elif new_pri == 2:
        priority_name = "MEDIUM"
    elif new_pri == 3:
        priority_name = "HIGH"

    task_to_update = session.query(TasksNew).filter(TasksNew.id == id_for_change).first()
    task_to_update.priority = new_pri
    print(f"The priority of task: '{task_to_update.name}' was successfully set to '{priority_name}'")
    session.commit()
    session.close()


# Changes the name of a task
@app.command()
def mvname(id_for_change: int):
    name_ids = [task_id[0] for task_id in session.query(TasksNew.id).all()]
    if id_for_change not in name_ids:
        print(f"There is no task with ID: {id_for_change}")
        return
    task_to_update = session.query(TasksNew).filter(TasksNew.id == id_for_change).first()
    new_name = typer.prompt("Enter your tasks new name")
    old_name = task_to_update.name
    task_to_update.name = new_name
    print(f"Task '{old_name}' was changed successfully to '{new_name}'")
    session.commit()
    session.close()


@app.command()
def printdate():
    valid_time_periods = [1, 2]
    cont_prompt = True
    while cont_prompt:
        time_period = int(typer.prompt("Select a time period: 1 - Daily, 2 - Weekly"))
        if time_period not in valid_time_periods:
            typer.echo(f"{time_period} is an invalid time period. Valid time periods: 1 - Daily, 2 - Weekly")
        else:
            cont_prompt = False

        from datetime import datetime, time, timedelta

        # Get today's date (today at midnight)
        today = datetime.today()
        midnight = time(0, 0, 0)
        end_of_day = time(23, 59, 59)

        beginning_of_today = datetime.combine(today, midnight)
        ending_of_today = datetime.combine(today, end_of_day)

        # Calc the beginning of the week (Monday at midnight) and the end of the month (last day of month at 23:59:59)
        day_of_week = today.weekday()
        beginning_of_week_date = today - timedelta(days=day_of_week)
        beginning_of_week = datetime.combine(beginning_of_week_date, midnight)
        days_to_add = 6 - day_of_week
        ending_of_week_date = today + timedelta(days=days_to_add)
        ending_of_week = datetime.combine(ending_of_week_date, end_of_day)

        # Calculate the end of the month
        # next_month = today.replace(day=28) + timedelta(days=4)  # Move to the 28th of this month and add 4 days
        # end_of_month = next_month - timedelta(days=next_month.day)
        # end_of_month = datetime.combine(end_of_month, end_of_day)

        # print("Beginning of Today:", beginning_of_today)
        # print("Ending of Today:", ending_of_today)
        # print("Beginning of Week:", beginning_of_week)
        # print("Ending of Week:", ending_of_week)

        if time_period == 1:
            time_period_text = "DAILY"
            first_condition = TasksNew.created_time >= beginning_of_today
            second_condition = TasksNew.created_time <= ending_of_today
        elif time_period == 2:
            time_period_text = "WEEKLY"
            first_condition = TasksNew.created_time >= beginning_of_week
            second_condition = TasksNew.created_time <= ending_of_week

        combined_conditions = and_(first_condition, second_condition)
        time_period_tasks = session.query(TasksNew).filter(combined_conditions)
        time_period_tasks_list = list(time_period_tasks)
        list_for_tabulate = []
        for task in time_period_tasks_list:
            if task.completed == 0:
                completed_status = "FALSE"
            elif task.completed == 1:
                completed_status = "TRUE"
            list_for_tabulate.append([task.id, task.name, task.created_time, task.priority, completed_status])
        # Set parameters for tabulate:
        table_style = "grid"
        time_period_table = tabulate(list_for_tabulate,
                                     headers=["TASK ID", "NAME", "CREATION DATE", "PRIORITY", "COMPLETED"],
                                     tablefmt=table_style,
                                     colalign=("center", "center", "center", "center", "center"))
        typer.echo(f"{time_period_text} TASKS TABLE:\n{time_period_table}")