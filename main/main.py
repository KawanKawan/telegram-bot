import logging
import os
from db import fetch_profile, update_profile, fetch_payment, add_payment,update_payment_amount,update_payment_status,add_event,complete_payment
from utils import facts_to_str,generate_token
from typing import Dict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.utils import helpers
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# TODO: error handler
logger = logging.getLogger(__name__)

# Stages
FIRST,EDIT_PROFILE,COLLECT_MONEY,ONGOING_PAYMENT,AMOUNT_TYPE,END,TYPING_REPLY,BACK1,BACK2,BACK3,BACK4, SHARE, EDIT_TITLE_REPLY = range(13)

# Callback data


# Main Menu
message0="Hi! Weclome to XXXX. Please choose from the menu."
MainMenu=["1. Edit Profile","2. Collect Money","3. Ongoing Payment","4. View History"]
ONE, TWO, THREE, FOUR = range(4)

#1. Edit Profile
message1="Your profile:\n"
buttons_EditProfile=["Edit Name","Edit Phone Number","Edit Preferred Payment Menthods","<<BACK"]
ONE1,ONE2,ONE3=range(4,7)
#2. Collect Money
message2="Start collect money from your friends!"
message2_1="Title of the event"
message2_2="How many people?"
message2_3="Type of money amount"
message2_4="Enter the amount he/she need to pay"
buttons_collect = [
    'Title', 'Number of people',
    'Amount', 'Done!',
]
NumOfPeople=["2","3","4","5","6","7","8","9","Others"]
MoneyType=["Equal Amount","Different Amount"]
LINK_CALLBACKDATA = "link-callback-data"
CHECK_THIS_OUT = "check-this-out"
#3. Ongoing Payment
message3="Onging Payment"
buttons_amount_type=["equal amount","different amount"]
#4. View History
message4="Your History"

BACK='<<BACK'

def start(update: Update, _: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user  

    logger.info("User %s started the conversation.", user.first_name)
    
    
    # initialize user_data 
    _.user_data['profile']={}
    _.user_data['payment']={}

    #user id in telegram 
    # https://python-telegram-bot.readthedocs.io/en/stable/telegram.user.html#telegram.User
    _.user_data['user_id']=update.message.from_user.id
    

    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton(MainMenu[0], callback_data=str(ONE)),
            InlineKeyboardButton(MainMenu[1], callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton(MainMenu[2], callback_data=str(THREE)),
            InlineKeyboardButton(MainMenu[3], callback_data=str(FOUR))
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # TODO: args in deeplink
    # if deeplink have args, it considers as others click the link
    # each link should a unique payload to search the specific payment in db
    if(_.args):
        update.message.reply_text(f"yes! bro, you got it {_.args[0]}", parse_mode= 'Markdown',reply_markup=reply_markup)
        complete_payment(_.args[0],update.message.from_user.id)
    else:
        update.message.reply_text(message0, parse_mode= 'Markdown',reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

def start_over(update: Update, _: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    query = update.callback_query
  
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton(MainMenu[0], callback_data=str(ONE)),
            InlineKeyboardButton(MainMenu[1], callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton(MainMenu[2], callback_data=str(THREE)),
            InlineKeyboardButton(MainMenu[3], callback_data=str(FOUR))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    query.edit_message_text(message0, parse_mode= 'Markdown',reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


# 1.Edit Profile  
def one(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton(buttons_EditProfile[0], callback_data=str("Name")),
            InlineKeyboardButton(buttons_EditProfile[1], callback_data=str("Phone")),
        ],
        [
            InlineKeyboardButton(buttons_EditProfile[2], callback_data=str("Payment Method")),
            InlineKeyboardButton(BACK, callback_data=str("start")),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    profilemessage=facts_to_str(fetch_profile(1078844444))
    query.edit_message_text(
        text=message1+profilemessage, parse_mode= 'Markdown',reply_markup=reply_markup
    )
    return EDIT_PROFILE

def edit_profile(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    _.user_data['profile']['choice'] = query.data
    query.message.reply_text(f'Your {query.data} ? Yes, I would love to hear about that!')

    return TYPING_REPLY

def received_profile_information(update: Update, _: CallbackContext) -> int:
    user_data = _.user_data['profile']
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    # update db
    userid=update.message.from_user.id
    update_profile(userid,category,text)

    keyboard = [
        [
            InlineKeyboardButton(BACK, callback_data=str(ONE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
    f"Success! {category} section updated."
    f"{facts_to_str(fetch_profile(1078844444))}",
    parse_mode= 'Markdown',reply_markup=reply_markup)

    # Tell ConversationHandler that we're in state `BACK1` now 
    return BACK1

# 2.Collect Money
def two(update: Update, _: CallbackContext) -> int:

    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton(buttons_collect[0], callback_data=str("Title")),
            InlineKeyboardButton(buttons_collect[1], callback_data=str("Number of people")),
        ],
        [
            InlineKeyboardButton(buttons_collect[2], callback_data=str("Amount")),
            InlineKeyboardButton(buttons_collect[3], callback_data=str(LINK_CALLBACKDATA)),
        ],
        [   InlineKeyboardButton(BACK, callback_data=str("start"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=message2, parse_mode='Markdown', reply_markup=reply_markup
    )
  
    return COLLECT_MONEY

def share_link(update: Update, context: CallbackContext)-> None:
    query = update.callback_query
    query.answer()
    bot = context.bot

    user_data = context.user_data['payment']
    numOfPersons=int(user_data['Number of people'])

    payloads=[]
    i=0
    text = f"{facts_to_str(user_data)}"
    while i<numOfPersons:
        payloads.append(generate_token())
        # TODO: link can only share to groups not individuals
        url = helpers.create_deep_linked_url(bot.username, str(payloads[i]))
        event_id=add_event(context.user_data['user_id'],user_data['Title'])
        # TODO: amount need to be replace by specific amount
        add_payment(context.user_data['user_id'],10,event_id,str(payloads[i]))
        text+=(f"Share the payment information to your friends: [▶️ CLICK HERE]({url}). \n")
        i+=1

    # create_deep_linked_url(bot_username, payload=None, group=False) 
    # the link will start the bot with /start, cant start with other command
    # url = helpers.create_deep_linked_url(bot.username, CHECK_THIS_OUT, group=True)
    query.edit_message_text(text=text, parse_mode='Markdown', disable_web_page_preview=True)

def edit_title(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
   
    # prompt user if user click amount before enter number of people 
    if (query.data=='Amount' and (not _.user_data['payment'].get('Number of people'))):
        query.message.reply_text(f'Please enter number of people first')
        return COLLECT_MONEY
    elif(query.data=='Amount' and _.user_data['payment'].get('Number of people')):
        """Show new choice of buttons"""
        query = update.callback_query
        query.answer()
    
        keyboard = [
            [
                InlineKeyboardButton(buttons_amount_type[0], callback_data=str("equal")),
                InlineKeyboardButton(buttons_amount_type[1], callback_data=str("different")),
            ],    
            [   InlineKeyboardButton(BACK, callback_data=str(ONE))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="Please choose the amount type", parse_mode='Markdown', reply_markup=reply_markup
        )
  
        return AMOUNT_TYPE
    else:
        _.user_data['payment']['choice'] = query.data
        query.message.reply_text(f'{query.data} ? Yes, I would love to hear about that!')
        return EDIT_TITLE_REPLY

# def choose_amount_type(update: Update, _: CallbackContext) -> int:
    

def handle_amount_type(update: Update, _: CallbackContext) -> int:
    return 1

def received_payment_info(update: Update, _: CallbackContext) -> int:
    user_data = _.user_data['payment']
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    # update userdata and later should be save in db after user DONE
    user_data.update({category:text})

    keyboard = [
        [
            InlineKeyboardButton(buttons_collect[0], callback_data=str("Title")),
            InlineKeyboardButton(buttons_collect[1], callback_data=str("Number of people")),
        ],
        [
            InlineKeyboardButton(buttons_collect[2], callback_data=str("Amount")),
            InlineKeyboardButton(buttons_collect[3], callback_data=str(LINK_CALLBACKDATA)),
        ],
        [   InlineKeyboardButton(BACK, callback_data=str("start"))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    #display the payment info
    update.message.reply_text(
    f"Success! {category} section updated."
    f"{facts_to_str(user_data)}",
    parse_mode= 'Markdown',reply_markup=reply_markup)

    return COLLECT_MONEY

# 3.Ongoing Payment
def three(update: Update, _: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()

    # fetch ongoing payment from database
    # TODO: replace with real data from db
    payment=["1","2","3","4"]
    keyboard = [
        [
            InlineKeyboardButton(payment[0], callback_data=str(ONE)),
            InlineKeyboardButton(payment[1], callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton(payment[2], callback_data=str(THREE)),
            InlineKeyboardButton(payment[3], callback_data=str(FOUR)),
        ],
        [   InlineKeyboardButton(BACK, callback_data=str("start"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Here are your ongoing payment",parse_mode= 'Markdown',reply_markup=reply_markup
    )
   
    return ONGOING_PAYMENT

def display_payment(update: Update, _: CallbackContext) -> int:
    #fetch 
    return null

# 4. View History
def four(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    # TODO: replace by our own website url with authentication
    url = "www.google.com"
    text = f"Visit our website to find out your payment summary: [▶️ CLICK HERE]({url})."
    query.edit_message_text(text=text, parse_mode='Markdown', disable_web_page_preview=True)


def end(update: Update, _: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv('API_token'), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and THIRD
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
       
        states={
            FIRST: [
                CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
            ],
            EDIT_PROFILE:[
                 CallbackQueryHandler(edit_profile, pattern='^' + str("Name") + '$'),
                 CallbackQueryHandler(edit_profile, pattern='^' + str("Phone") + '$'),
                 CallbackQueryHandler(edit_profile, pattern='^' + str("Payment Method") + '$'),
                 CallbackQueryHandler(start_over, pattern='^' + str("start") + '$'),
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_profile_information,
                )
            ],
            COLLECT_MONEY: [
                CallbackQueryHandler(edit_title, pattern='^' + str("Title") + '$'),
                CallbackQueryHandler(edit_title, pattern='^' + str("Number of people") + '$'),
                CallbackQueryHandler(edit_title, pattern='^' + str("Amount") + '$'),
                CallbackQueryHandler(share_link, pattern='^' + str(LINK_CALLBACKDATA) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str("start") + '$'),
            ],
            EDIT_TITLE_REPLY:[
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_payment_info,
                )
            ],
            AMOUNT_TYPE:[
                CallbackQueryHandler(handle_amount_type, pattern='^' + str("equal") + '$'),
                CallbackQueryHandler(handle_amount_type, pattern='^' + str("different") + '$'),
                CallbackQueryHandler(two, pattern='^' + str(ONE) + '$'),
            ],
            ONGOING_PAYMENT:[
                CallbackQueryHandler(display_payment, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str("start") + '$'),
            ],
            END: [
                CallbackQueryHandler(end, pattern='^' + str(ONE) + '$')
            ],
            BACK1:[
                CallbackQueryHandler(one, pattern='^' + str(ONE) + '$')
            ],
            BACK2:[
                CallbackQueryHandler(two, pattern='^' + str(ONE) + '$')
            ]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
