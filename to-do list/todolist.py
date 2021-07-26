from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

# Write your code here
# print("""Today:
# 1) Do yoga
# 2 ) Make breakfast
# 3) Learn basics of SQL
# 4) Learn what is ORM""")

engine = create_engine("sqlite:///todo.db?check_same_thread=False")

Base = declarative_base()

class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default="NULL")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def get_tasks(deadline_):
    return session.query(Table).filter(Table.deadline == deadline_).all()


def add_task(new_task_, new_deadline_):
    new_row = Table(task=new_task_, deadline=datetime.strptime(new_deadline_, "%Y-%m-%d").date())
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")


def exit():
    print("Bye!")


def print_menu():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
""")


def check_tasks(tasks_):
    if tasks_:
        for i, task in enumerate(tasks_):
            if i != len(tasks_) - 1:
                print(f"{task.id}. {task.task}")
            else:
                print(f"{task.id}. {task.task}\n")
    else:
        print("Nothing to do!\n")

def check_weekday(weekday_):
    if weekday_ == 0:
        return "Monday"
    elif weekday_ == 1:
        return "Tuesday"
    elif weekday_ == 2:
        return "Wednesday"
    elif weekday_ == 3:
        return "Thursday"
    elif weekday_ == 4:
        return "Friday"
    elif weekday_ == 5:
        return "Saturday"
    elif weekday_ == 6:
        return "Sunday"
    return weekday_

def delete_task(rows_, idx):
    session.delete(rows_[idx])
    session.commit()
    print("The task has been deleted!")


def get_command(command_):
    today = datetime.today()
    rows = session.query(Table).all()

    if command_ == 1:
        todays_tasks = get_tasks(today)
        print("Today {} {}:".format(today.day, today.strftime('%b')))
        check_tasks(todays_tasks)
        print_menu()
        get_command(int(input()))

    elif command_ == 2:
        for i in range(0, 7):
            day = today + timedelta(days=i)
            days_tasks = get_tasks(day.date())
            weekday = check_weekday(day.weekday())
            print(f"{weekday} {day.day} {day.strftime('%b')}:")
            check_tasks(days_tasks)
        print_menu()
        get_command(int(input()))

    elif command_ == 3:
        print("All tasks:")
        for row in rows:
            print(f"{row.id}. {row.task} {row.deadline.day} {row.deadline.strftime('%b')}")
        print_menu()
        get_command(int(input()))

    elif command_ == 4:
        missed = session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
        if missed:
            print("Missed tasks:")
            for i, missed_task in enumerate(missed):
                if i != len(missed) - 1:
                    print(f"{missed_task.id}. {missed_task.task} {missed_task.deadline.day} "
                        f"{missed_task.deadline.strftime('%b')}")
                else:
                    print(f"{missed_task.id}. {missed_task.task} {missed_task.deadline.day} "
                          f"{missed_task.deadline.strftime('%b')}\n")
        else:
            print("Nothing is missed!")
        print_menu()
        get_command(int(input()))

    elif command_ == 5:
        new_task = input("Enter task: ")
        new_deadline = input("Enter deadline: ")
        add_task(new_task, new_deadline)
        print_menu()
        get_command(int(input()))

    elif command_ == 6:
        all_tasks = session.query(Table).order_by(Table.deadline).all()
        for task in all_tasks:
            print(f"{task.id}. {task.task} {task.deadline.day} {task.deadline.strftime('%b')}")
        print("Chose the number of the task you want to delete:")
        idx = int(input())
        delete_task(rows, idx)
        print_menu()
        get_command(int(input()))

    elif command_ == 0:
        exit()


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

print_menu()
get_command(int(input()))

