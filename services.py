import re
import random
from datetime import datetime, timedelta

from models import User, Session, Procedure, Addition, Order
from configs import ADMIN_ID


session = Session()
visiting_time = {}

calendar = {"1": "Січня",
            "2": "Лютого",
            "3": "Березня",
            "4": "Квітня",
            "5": "Травня",
            "6": "Червня",
            "7": "Липня",
            "8": "Серпня",
            "9": "Вересня",
            "10": "Жовтня",
            "11": "Листопада",
            "12": "Грудня",}


def add_user(user: User):
    session.add(user)
    session.commit()
    session.close()


def add_procedure(procedure: Procedure):
    session.add(procedure)
    session.commit()
    session.close()


def add_addition(addition: Addition):
    session.add(addition)
    session.commit()
    session.close()


def add_order(order: Order):
    session.add(order)
    session.commit()
    session.close()


def user_exist(user_id: int) -> bool:
    users = []
    all_users = session.query(User).all()
    for record in all_users:
        users.append(record.user_id)
    if user_id in users:
        session.close()
        return True
    else:
        session.close()
        return False


def get_user_info(user_id: int) -> User:
    # Query the User table by user_id
    user_info = session.query(User).filter_by(user_id=user_id).first()
    return user_info


def add_procedure(new_services: dict, user_id: int, time):
    """ADD PROCEDURE RECORD HAVE DIFFERENT COUNT OF PARAMETERS"""

    # create fake user_id for admin order
    if user_id == int(ADMIN_ID):
        random_number = random.randint(100000, 999999)
        exist = get_user_procedure(random_number)
        if exist:
            random_number2 = random.randint(100000, 999999)
            user_id = random_number2
        else:
            user_id = random_number
        user = User(user_id=user_id,
                    username="fakeuser",
                    first_name="fakeuser",
                    last_name="fakeuser",
                    mobile="067576767")
        add_user(user)

    if len(new_services["services"]) + len(new_services["additions"]) == 2:
        order = Order(
            user_id=user_id,
            meeting_time=time,
            kind_nails_service=["kind_nails_procedure"][:5],
            procedure1=new_services["services"][0],
            procedure2=new_services["additions"][0],
        )
    elif len(new_services["services"]) + len(new_services["additions"]) == 3:
        order = Order(
            user_id=user_id,
            kind_nails_service=time,
            procedure1=new_services["services"][0],
            procedure2=new_services["services"][1],
            procedure3=new_services["additions"][0],
        )
    elif len(new_services["services"]) + len(new_services["additions"]) == 4:
        order = Order(
            user_id=user_id,
            kind_nails_service=time,
            procedure1=new_services["services"][0],
            procedure2=new_services["services"][1],
            procedure3=new_services["additions"][0],
            procedure4=new_services["additions"][1],
        )
    else:
        order = Order(
            user_id=user_id,
            kind_nails_service=time,
            procedure1=new_services["services"][0],
            procedure2=new_services["services"][1],
            procedure3=new_services["services"][2],
            procedure4=new_services["additions"][0],
            additions=new_services["additions"][1]
        )
    add_order(order)


def get_user_procedure(user_id: int) -> Order:
    user_procedure = session.query(Order).filter_by(user_id=user_id).first()
    return user_procedure


def remove_order_record(user_id: int):
    order_to_delete = session.query(Order).filter(Order.user_id == user_id).first()
    session.delete(order_to_delete)
    session.commit()
    session.close()
    print(f"RECORD USER {user_id} WAS DELETE")


def change_order_time(order: Order, meeting_time):
    order.update_meeting_time(meeting_time)
    print(f"Дату процедури користувача {order.user_id} Змінено на {meeting_time}")


def add_test_user():
    user = User(user_id=1587874848,
                username="username",
                first_name="first_name",
                last_name="last_name",
                mobile="986785474")
    add_user(user)


def get_all_events() -> list:
    # return list of all created events dicts
    all_events = session.query(Order).all()
    order_dicts = []
    for event in all_events:
        usr_first_name = get_user_info(event.user_id).user_first_name
        if event.procedure3 is None:
            order_dicts.append({"user_id": event.user_id,
                                "user_first_name": usr_first_name,
                                "date": event.meeting_time,
                                "procedure1": event.procedure1,
                                "procedure2": event.procedure2}
                               )

        elif event.procedure3:
            order_dicts.append({"user_id": event.user_id,
                                "user_first_name": usr_first_name,
                                "date": event.meeting_time,
                                "procedure1": event.procedure1,
                                "procedure2": event.procedure2,
                                "procedure3": event.procedure3}
                               )
        elif event.procedure4:
            order_dicts.append({"user_id": event.user_id,
                                "user_first_name": usr_first_name,
                                "date": event.meeting_time,
                                "procedure1": event.procedure1,
                                "procedure2": event.procedure2,
                                "procedure3": event.procedure3,
                                "procedure4": event.procedure4}
                               )
        else:
            order_dicts.append({"user_id": event.user_id,
                                "user_first_name": usr_first_name,
                                "date": event.meeting_time,
                                "procedure1": event.procedure1,
                                "procedure2": event.procedure2,
                                "procedure3": event.procedure3,
                                "procedure4": event.procedure4,
                                "additions": event.additions}
                               )

    return [order_dicts]


def rem_selected_order(message):
    user_id = re.findall(r'\d+', message.text[3:15])
    try:
        remove_order_record(user_id[0])
    except IndexError:
        print("Record was not deleted")


def get_next_7days() -> list:
    today = datetime.today()
    next_days = []
    for i in range(1, 8):
        next_date = today + timedelta(days=i)
        next_days.append(next_date.strftime("%d.%m.%y"))

    return next_days


def create_visiting_time() -> list:
    start_time = datetime.strptime("15:00", "%H:%M")
    time_points = []
    # will generate 4 time points at intervals of hour
    for i in range(4):
        time_points.append(start_time.strftime("%H:%M"))
        start_time += timedelta(hours=1)

    return time_points


def create_datetime() -> datetime:
    date_string = f"{visiting_time['day']} {visiting_time['hour']}"
    format_string = '%d.%m.%y %H:%M'
    datetime_object = datetime.strptime(date_string, format_string)
    return datetime_object
