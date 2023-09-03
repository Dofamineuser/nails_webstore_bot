import telebot
from telebot import types
from configs import TOKEN, ADMIN_ID, INSTA_MESSAGE_PART, INSTA_LINK, ADDITIVES_LIST
from models import User
from services import add_user, user_exist, get_user_info, add_procedure,\
    get_user_procedure, remove_order_record, change_order_time
from datetime import datetime


bot = telebot.TeleBot(TOKEN)
admin_id = ADMIN_ID

new_services = {"services": [],
                "additions": []}


@bot.message_handler(commands=["start"])
def start(message):
    user = message.from_user
    first_name = user.first_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    if user_exist(message.from_user.id):
        # welcome letter if user already exist
        bot.send_message(message.from_user.id, f"Рада знову вас бачити, {first_name} ! 🖐\n"
                                               f"{INSTA_MESSAGE_PART}{INSTA_LINK}",
                         parse_mode="markdown")

    else:
        # welcome letter if user not exist
        bot.send_message(message.from_user.id, f"Вітаю, {first_name} ! 🖐\n"
                                               f"Я бот для запису до [anastasiya_nails_dnipro_](https://instagram.com/anastasiya_nails_dnipro_?igshid=MzRlODBiNWFlZA==)",
                                                 parse_mode="markdown")

    """CREATING START BUTTONS"""
    check_me_in = types.KeyboardButton("Записатися")
    check_me_time = types.KeyboardButton("Нагадати про запис")
    check_me_replace = types.KeyboardButton("Перенести запис")
    cancel_order = types.KeyboardButton("Скасувати запис")
    contacts = types.KeyboardButton("Мої контакти")
    markup.add(check_me_in, check_me_time, check_me_replace, cancel_order, contacts)

    bot.send_message(message.from_user.id, text="Чим можу допомогти?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == "записатися")
def create_task(message):
    """START OF CREATING ORDER"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    order = get_user_procedure(message.from_user.id)
    if order:
        bot.send_message(message.from_user.id, f"{order.meeting_time} \n {order.procedure1} \n {order.procedure2}")
        cancel_order = types.KeyboardButton("Скасувати запис")
        check_me_replace = types.KeyboardButton("Перенести запис")
        markup.add(cancel_order, check_me_replace)
        bot.send_message(message.from_user.id,
                         text="Вибачете але у вас вже є активний запис \n"
                              "Ви можете змінити час або видалити і створити новий запис",
                         reply_markup=markup)
    else:
        manikyr = types.KeyboardButton("Ручки 💅")
        pedik = types.KeyboardButton("Ніжки 👣")
        markup.add(manikyr, pedik)
        bot.send_message(message.from_user.id, text="Оберіть процедуру", reply_markup=markup)
        bot.register_next_step_handler(message, hands_or_foots)


@bot.message_handler(func=lambda message: message.text.lower() == "скасувати запис")
def cancel_task(message):
    """REMOVE ORDER IF EXISTS"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    check_me_in = types.KeyboardButton("Записатися")
    markup.add(check_me_in)
    order = get_user_procedure(message.from_user.id)
    if order:
        bot.send_message(message.from_user.id, f"{order.meeting_time} \n {order.procedure1} \n {order.procedure2}")
        remove_order_record(message.from_user.id)
        bot.send_message(message.from_user.id,
                         text="Ваш запис скасовано, Якщо бажаєте створити новий натисніть на кнопку 'Створити запис'",
                         reply_markup=markup)
    else:
        bot.send_message(message.from_user.id,
                         text="У вас не знайдено активних записів, Бажаєте створити?",
                         reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == "перенести запис")
def transfer_task(message):
    """CHANGE ORDER TIME"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    order = get_user_procedure(message.from_user.id)
    if order:
        bot.send_message(message.from_user.id, text="Добре, на який день перенести запис?")
        new_meeting_time = datetime(2023, 9, 10, 14, 30)
        change_order_time(order=order, meeting_time=new_meeting_time)
        bot.send_message(message.from_user.id, text="Ваш запис перенесено")
    else:
        check_me_in = types.KeyboardButton("Записатися")
        markup.add(check_me_in)
        bot.send_message(message.from_user.id, text="У вас немає активного запису який можна перенести",
                         reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == "нагадати про запис")
def recall(message):
    bot.send_message(message.from_user.id,
                     text="Конечно дорогая сучка\n"
                          "Сейчас сверю есть ли ты в записях и проверю на когда можно\n"
                          "Допилю только базу данных сюда")


def hands_or_foots(message):
    """USER SELECTED KIND OF NAILS PROCEDURE"""
    new_services["kind_nails_procedure"] = message.text[:5]

    if message.text.lower() == "ручки 💅":
        hands(message)
    elif message.text.lower() == "ніжки 👣":
        foots(message)


def hands(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    manik1 = types.KeyboardButton("Манікюр гігієнічний")
    manik2 = types.KeyboardButton("Манікюр з покриттям")
    manik3 = types.KeyboardButton("Манікюр з покр + укріплення")
    manik4 = types.KeyboardButton("Нарощення")
    markup.add(manik1, manik2, manik3, manik4)
    bot.send_message(message.from_user.id, text="Оберіть, що саме вас цікавить ⬇️", reply_markup=markup)
    bot.register_next_step_handler(message, additions)


def foots(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    pedik1 = types.KeyboardButton("Педикюр гігієнічний")
    pedik2 = types.KeyboardButton("Педикюр з покриттям")
    markup.add(pedik1, pedik2)
    bot.send_message(message.from_user.id, text="Оберіть, що саме вас цікавить ⬇️", reply_markup=markup)
    bot.register_next_step_handler(message, kind_of_foots_service)


def kind_of_foots_service(message):
    new_services["services"].append(message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if message.text.lower() == "педикюр гігієнічний" or message.text.lower() == "педикюр з покриттям":
        foots_gigiena1 = types.KeyboardButton("Тільки пальчики")
        foots_gigiena2 = types.KeyboardButton("Пальчики + стопа")
        markup.add(foots_gigiena1, foots_gigiena2)
    bot.send_message(message.from_user.id, text="Оберіть, що саме вас цікавить ⬇️", reply_markup=markup)
    bot.register_next_step_handler(message, additions)


def additions(message):
    new_services["services"].append(message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    additions1 = types.KeyboardButton("Френч")
    additions2 = types.KeyboardButton("Слайдери")
    additions3 = types.KeyboardButton("Стемпінг")
    additions4 = types.KeyboardButton("Фольга")
    additions5 = types.KeyboardButton("Роспис")
    additions6 = types.KeyboardButton("Камінчики")
    additions7 = types.KeyboardButton("Не потребую")
    markup.add(additions1, additions2, additions3, additions4, additions5, additions6, additions7)
    bot.send_message(message.from_user.id, text="Оберіть додаткові послуги", reply_markup=markup)
    if len(new_services["services"]) + len(new_services["additions"]) < 4:
        bot.register_next_step_handler(message, final2)
    else:
        bot.register_next_step_handler(message, final)


def final2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    new_services["additions"].append(message.text)
    if new_services["kind_nails_procedure"] == "Ручки":
        final_message1 = types.KeyboardButton("Хочу ще педикюр")
        final_message2 = types.KeyboardButton("Завершити запис")
        markup.add(final_message1, final_message2)
        bot.send_message(message.from_user.id, text="Бажаєте додати ще послуги?", reply_markup=markup)
        bot.register_next_step_handler(message, second_procedure)

    elif new_services["kind_nails_procedure"] == "Ніжки":
        final_message1 = types.KeyboardButton("Хочу ще манікюр")
        final_message2 = types.KeyboardButton("Завершити запис")
        markup.add(final_message1, final_message2)
        bot.send_message(message.from_user.id, text="Бажаєте додати ще послуги?", reply_markup=markup)
        bot.register_next_step_handler(message, second_procedure)


def second_procedure(message):
    if message.text == "Хочу ще манікюр":
        hands(message)
    elif message.text == "Хочу ще педикюр":
        foots(message)
    else:
        final(message)


def final(message):
    if message.text in ADDITIVES_LIST:
        new_services["additions"].append(message.text)
    new_services["user_first_name"] = message.from_user.first_name
    if not user_exist(message.from_user.id):
        bot.send_message(message.from_user.id, text="Вкажіть ваш номер мобільного для зворотнього зв'язку")
        bot.register_next_step_handler(message, get_user_phone)
    else:
        new_services["user_phone"] = get_user_info(message.from_user.id).user_mobile
        order_message = f"Ваше замовлення: {new_services['user_first_name']}\n" \
                        f"{'|'.join(new_services['services'])}\n" \
                        f"Додаткові послуги: {'|'.join(new_services['additions'])}\n" \
                        f"Ваш контактний номер: {new_services['user_phone']}"
        bot.send_message(admin_id, order_message)
        print(order_message)
        add_procedure(new_services=new_services, user_id=message.from_user.id, time=datetime.utcnow())
        bot.send_message(message.from_user.id, f"Ви успішно записались \n"
                                               f"{order_message}")


def get_user_phone(message):
    try:
        phone = str(message.text.replace("+", "").replace("38", ""))
        print(f"LEN PHONE: {len(phone)}")
        if phone.isdigit() and phone.startswith("0") and len(phone) == 10:
            new_services["user_phone"] = phone
            """IF PHONE IS VALID ADD USER TO DATABASE"""
            user = User(user_id=message.from_user.id,
                        username=message.from_user.username,
                        first_name=message.from_user.first_name,
                        last_name=message.from_user.last_name,
                        mobile=new_services["user_phone"])
            add_user(user)
            order_message = f"Ваше замовлення: {new_services['user_first_name']}\n" \
                            f"{'|'.join(new_services['services'])}\n" \
                            f"Додаткові послуги: {'|'.join(new_services['additions'])}\n" \
                            f"Ваш контактний номер: {new_services['user_phone']}"
            add_procedure(new_services=new_services, user_id=message.from_user.id, time=datetime.utcnow())
            bot.send_message(admin_id, order_message)
            print(order_message)
            bot.send_message(message.from_user.id, f"Ви успішно записались \n"
                                                   f"{order_message}")

        else:
            """IF PHONE IS NOT VALID TRY AGAIN"""
            bot.send_message(message.from_user.id, text="Ви вказали некоректний номер🤨, введіть будь ласка ще раз")
            bot.register_next_step_handler(message, get_user_phone)

    except AttributeError:
        bot.send_message(message.from_user.id, text="Ви вказали некоректиний номер🤨, введіть будьласка ще раз")
        bot.register_next_step_handler(message, get_user_phone)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
