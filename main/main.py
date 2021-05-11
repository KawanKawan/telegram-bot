import logging
from db import fetch_profile, update_profile
from utils import facts_to_str
from typing import Dict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
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

logger = logging.getLogger(__name__)

# Stages
FIRST,EDIT_PROFILE,COLLECT_MONEY,ONGOING_PAYMENT,VIEW_HISTORY,END,TYPING_REPLY,BACK = range(8)

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
    ['Title'], ['Number of people'],
    ['Amount'], ['Done!'],
]
NumOfPeople=["2","3","4","5","6","7","8","9","Others"]
MoneyType=["Equal Amount","Different Amount"]
#3. Ongoing Payment
message3="Onging Payment"
buttons_OngoingPayment=["1","2","3","4"]
#4. View History
message4="Your History"

BACK='BACK'

def start(update: Update, _: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user  
    logger.info("User %s started the conversation.", user.first_name)
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
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(message0, parse_mode= 'Markdown',reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

def start_over(update: Update, _: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
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


# My profile: 
def one(update: Update, _: CallbackContext) -> int:
    """Show new choice of buttons"""
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
    profilemessage=facts_to_str(fetch_profile(123))
    query.edit_message_text(
        text=message1+profilemessage, parse_mode= 'Markdown',reply_markup=reply_markup
    )
    return EDIT_PROFILE

def edit_profile(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    _.user_data['choice'] = query.data
    query.message.reply_text(f'Your {query.data} ? Yes, I would love to hear about that!')
    return TYPING_REPLY

def received_information(update: Update, _: CallbackContext) -> int:
    user_data = _.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    # update db
    update_profile({category:text})

    keyboard = [
        [
            InlineKeyboardButton(BACK, callback_data=str(ONE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
    f"Success! {category} section updated."
    f"{facts_to_str(fetch_profile(123))}",
    parse_mode= 'Markdown',reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `BACK` now 
    return BACK

def two(update: Update, _: CallbackContext) -> int:

    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton(buttons_collect[0], callback_data=str(ONE)),
            InlineKeyboardButton(buttons_collect[1], callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton(buttons_collect[2], callback_data=str(THREE)),
            InlineKeyboardButton(buttons_collect[3], callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=message2, parse_mode= 'Markdown', reply_markup=reply_markup
    )
  
    return COLLECT_MONEY

def three(update: Update, _: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton(buttons_OngoingPayment[0], callback_data=str(ONE)),
            InlineKeyboardButton(buttons_OngoingPayment[1], callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton(buttons_OngoingPayment[2], callback_data=str(ONE)),
            InlineKeyboardButton(buttons_OngoingPayment[3], callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Third CallbackQueryHandler. Do want to start over?",parse_mode= 'Markdown',reply_markup=reply_markup
    )
   
    return ONGOING_PAYMENT


def four(update: Update, _: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Fourth CallbackQueryHandler, Choose a route", parse_mode= 'Markdown',reply_markup=reply_markup
    )
    return VIEW_HISTORY


def end(update: Update, _: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("1812536998:AAFUxezkWLEpoB2-OEWibE1ozbrO5VF5tlA", use_context=True)

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
                    received_information,
                )
            ],
            # COLLECT_MONEY: [

            # ],
            # ONGOING_PAYMENT:[

            # ],
            # VIEW_HISTORY: [

            # ],
            END: [
                CallbackQueryHandler(end, pattern='^' + str(ONE) + '$')
            ],
            BACK:[
                CallbackQueryHandler(one, pattern='^' + str(ONE) + '$')
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
