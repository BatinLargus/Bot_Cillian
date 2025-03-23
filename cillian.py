import telebot

from telebot import types

token = "8006745214:AAHuZ73jE_9OU3CjiV2we9XdfLYckGh2I0Y"

bot = telebot.TeleBot(token)

levels = ["Elementary", "Pre - Intermediate", "Intermediate", "Upper Intermediate", "Advanced", "Proficiency"]
plan = []
n = 0
prep_plan = []
users = {}


print("Successfully started")

def level_menu():

    menu = types.ReplyKeyboardMarkup(resize_keyboard = True)

    for level in levels:
        menu.add(types.KeyboardButton(level))

    return menu

@bot.message_handler(commands = ['start', 'plan', 'restart'])

def command(message):

    print(message.text)
    if message.text == '/start':
        menu = level_menu()

        if message.chat.id in users:
            bot.send_message(message.chat.id, "Thank you, but you already have your plan! ")

        else:

            bot.send_message(message.chat.id, "Hello, {0.first_name}! What is the level of your proficiency in English? ".format(message.from_user), reply_markup=menu)

    elif message.text == '/plan' and message.chat.id in users:
        bot.send_message(message.chat.id, f"Sure thing! Here's your plan, {message.from_user.first_name} 👇👇👇 : ")
        for step in prep_plan:
            bot.send_message(message.chat.id, f"😉 {step}")

    elif message.text == '/restart':
        menu = level_menu()
        prep_plan.clear()
        plan.clear()
        users.clear()
        bot.send_message(message.chat.id,"Hello, {0.first_name}! What is the level of your proficiency in English? ".format(message.from_user), reply_markup=menu)



    elif message.text == '/plan' and message.chat.id not in users:
        bot.send_message(message.chat.id, "Choose your level of proficiency first! Write \'/start\' and start your educational journey!")

    elif '/' in message.text:
        bot.send_message(message.text.id, "Invalid command! Try again!")




@bot.message_handler(content_types= ['text'])


def user_message(message):
    if message.text in levels and message.chat.id not in users:
        users[message.chat.id] = message.text
        with open(f"{message.text}.txt", "r", encoding='UTF-8') as file:
            lines = file.readlines()
            for line in lines:
                plan.append(line)

        file.close()
        make_prep_plan(message)

        bot.send_message(message.chat.id, "That's great! Now, we are ready set out for our unforgettable journey in learning English with focus on enhancing public speaking skills!")
        print(message.text == "Advanced")
        if message.text != "Advanced" and message.text != "Proficiency":
            bot.send_message(message.chat.id, f"{message.text} - it's the great start! We have a lot of thing to do, {message.from_user.first_name}! Let not waste any time! Let's go! 😎", reply_markup=types.ReplyKeyboardRemove())
            intro_lesson(message)
        else:
            bot.send_message(message.chat.id, f"""{message.text} - such a high level you have! So, for you I have more interesting tasks) But no worry! They will help you to learn more and I'll provide you with some assistance, if needed, of course. Let's get started! 😎 """, reply_markup=types.ReplyKeyboardRemove())
            intro_lesson(message)

    if message.text == "Yes! Let's go!":
        bot.send_message(message.chat.id, "Well, let's get started!", reply_markup = types.ReplyKeyboardRemove())
        start_lesson(message)

    elif message.text == "Well, give me some time, please":

        bot.send_message(message.chat.id, "Ok, carefully read the plan I send to you and prepare all you need. Since you're ready - push the first button!")

    elif message.text =="I managed to do that!":
        bot.send_message(message.chat.id, "Amazing! Let's go ahead! ")
        start_lesson(message)

    elif "thank" in message.text:
        bot.send_message(message.chat,id, f"Thank YOU, {message.from_user.first_name}! I'm glad to be your personal assistant!")


    else:
        bot.send_message(message.chat.id, "Hmm...  You may already have a plan or didn't make valid choice. Try again! ")



def intro_lesson(message):

    bot.send_message(message.chat.id, "First of all, here is the plan that will always help you prepare and organize your speech 👇👇👇 : ")

    for step in prep_plan:
        bot.send_message(message.chat.id, f"😉 {step}")

    bot.send_message(message.chat.id, "This is a plan that you can use if you need help in preparing and organizing your public speaking")

    bot.send_message(message.chat.id,"If you need, you can also write \'/plan\' to see your personal plan again! ")

    menu = y_n_menu(message)

    bot.send_message(message.chat.id, f"Well, well, well... Are you ready for our journey, {message.from_user.first_name} 😏 ? ", reply_markup= menu)

def start_lesson(message):
    global n

    if n == 7:
        bot.send_message(message.chat.id, f"""Congratulations, {message.from_user.first_name}! You did it! Now, out 7 day amazing educational journey
came to end! It was nice to be your assistant, i really appreciate your efforts and you got far more better in your
public speaking skills! """, reply_markup=types.ReplyKeyboardRemove())

        bot.send_message(message.chat.id, "Don't worry! If you want to take up a new course - write \'/restart\'! Good luck!")

    else:
        day_plan = plan[n]
        n+=1
        bot.send_message(message.chat.id, day_plan)

        menu = next_menu()
        bot.send_message(message.chat.id, "Good luck! Since you manage to do that, we'll go to the next step!",reply_markup= menu)



def next_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add(types.KeyboardButton("I managed to do that!"))
    return menu
def y_n_menu(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add(types.KeyboardButton("Yes! Let's go!"))
    menu.add(types.KeyboardButton("Well, give me some time, please"))
    return menu
def make_prep_plan(message):

    if message.text in levels:
        with open(f"{message.text}_plan.txt", "r", encoding = 'UTF_8') as file:
            lines = file.readlines()
            for line in lines:
                prep_plan.append(line.strip())
            file.close()
        return prep_plan


bot.polling()

