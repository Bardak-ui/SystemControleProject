import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackQueryHandler, ContextTypes
from asgiref.sync import sync_to_async

# Добавьте путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemControleProject.settings')
import django
django.setup()

from scp.models import Profile

TOKEN = '7724435274:AAG2pzTE01tPR6tAHY8UPEIN89qvaDKyPYE3'

# Состояния для ConversationHandler
MENU, SETTINGS, PROFILE, USERS = range(4)

# Главное меню
def menu_bk():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('👤 Профиль', callback_data='profile')],
        [InlineKeyboardButton('👥 Пользователи', callback_data='users')],
        [InlineKeyboardButton('⚙ Настройки', callback_data='settings')],
        [InlineKeyboardButton('❌ Выход', callback_data='exit')],
    ])

# Меню профиля
def profile_bk():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('Обо мне', callback_data='about')],
        [InlineKeyboardButton('Установить псевдоним', callback_data='set_name')],
        [InlineKeyboardButton('🔙 Назад', callback_data='back')],
    ])

# Меню настроек
def settings_bk():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('❌ Удалить свою уч.запись', callback_data='del_acc')],
        [InlineKeyboardButton('🔙 Назад', callback_data='back')],
    ])

def users_bk():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('🔙 Назад', callback_data='back')],
    ])

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    start_menu = f"Привет, {user.first_name}!\nВыберите действие:"
    await update.message.reply_text(start_menu, reply_markup=menu_bk())
    return MENU

# Обработка главного меню
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'profile':
        await query.edit_message_text("👤 Профиль", reply_markup=profile_bk())
        return PROFILE

    elif query.data == 'users':
        await query.edit_message_text("👥 Пользователи", reply_markup=users_bk())
        return USERS

    elif query.data == 'settings':
        await query.edit_message_text("⚙ Настройки", reply_markup=settings_bk())
        return SETTINGS

    elif query.data == 'exit':
        await query.edit_message_text("До встречи!")
        return ConversationHandler.END

# Обработка меню профиля
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'about':
        user = query.from_user
        await query.edit_message_text(
            f"О вас:\nЮзернейм: {user.username}\nИмя: {user.first_name}",
            reply_markup=profile_bk()
        )
    elif query.data == 'back':
        await query.edit_message_text("Главное меню", reply_markup=menu_bk())
        return MENU

# Обработка меню настроек
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'back':
        await query.edit_message_text("Главное меню", reply_markup=menu_bk())
        return MENU

# Получение всех пользователей
@sync_to_async
def get_all_profiles_sync():
    return list(Profile.objects.all())

# Обработка списка пользователей
async def get_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'users':
        profiles = await get_all_profiles_sync()
        if profiles:
            for profile in profiles:
                avatar = await sync_to_async(lambda: profile.avatar.path if profile.avatar else None)()
                puser = await sync_to_async(lambda: profile.puser)()
                role = await sync_to_async(lambda: profile.role)()
                bio = await sync_to_async(lambda: profile.bio)()
                message = f"👤 Профиль:\n✘ Имя: {puser}\n✘ Роль: {role}\n✘ Био: {bio}\n"

                if avatar and os.path.exists(avatar):
                    with open(avatar, 'rb') as photo:
                        await query.message.reply_photo(photo=photo, caption=message)  # Используем query.message.reply_photo
                else:
                    await query.message.reply_text(message)  # Используем query.message.reply_text
        else:
            await query.message.reply_text("Пользователи не найдены.")  # Используем query.message.reply_text
    elif query.data == 'back':
        await query.edit_message_text("Главное меню", reply_markup=menu_bk())
        return MENU

# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("До встречи!")
    return ConversationHandler.END

# Запуск бота
def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [CallbackQueryHandler(menu)],
            PROFILE: [CallbackQueryHandler(profile)],
            SETTINGS: [CallbackQueryHandler(settings)],
            USERS: [CallbackQueryHandler(get_user)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()