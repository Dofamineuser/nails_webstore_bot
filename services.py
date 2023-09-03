from models import User, Session, Procedure, Addition, Order


session = Session()


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
