import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from mybot import dp

logger = logging.getLogger(__name__)

# --- Keyboard ---
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('📝 Шинээр бүртгүүлэх')],
        [KeyboardButton('✅ Ажил ЭХЭЛСЭН цаг бүртгүүлэх')],
        [KeyboardButton('🏁 Ажил ДУУССАН цаг бүртгүүлэх')]
    ],
    resize_keyboard=True
)

# --- /menu болон /start команд өгөхөд үндсэн цэс харуулна ---
@dp.message_handler(commands=['menu', 'start'], state='*')
async def send_menu(message: types.Message, state: FSMContext):
    await state.finish()
    logger.info("Displaying menu for user %s", message.from_user.id)
    await message.answer(
        "Доорх цэснээс сонгоно уу:",
        reply_markup=menu_keyboard
    )

# ==== /help ====

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    help_text = (
        "🆘 <b>Тусламж ба Зааварчилгаа</b>\n\n"
        "Энэхүү бот нь ажилтнуудын цагийн бүртгэл, ажлын байршлын баталгаажуулалт хийхэд зориулагдсан.\n\n"
        "Энэхүү цагийн мэдээллээр таны цалингийн цаг бодогдох тул хариуцлагатай хандана уу.\n\n"
        "<b>🔹 Үндсэн коммандууд:</b>\n"
        "/register – Шинээр ажилтнаар бүртгүүлэх\n"
        "/checkin – Ажил эхэлсэн цаг болон байршлыг бүртгүүлэх\n"
        "/checkout – Ажил дууссан цаг, байршил, ажлын зураг, тайлбартай бүртгүүлэх\n"
        "/start – Үндсэн цэс рүү буцах\n\n"
        "<b>🔹 Зааварчилгаа алхам алхмаар:</b>\n"
        "1️⃣ <b>Шинээр бүртгүүлэх:</b>\n"
        "- /register коммандыг бичнэ\n"
        "- Бот таны Регистерийн дугаарыг асууна\n"
        "- РЕГИСТЕР-ийн дугаарын эхний АА үсгийг томоор бичихыг анхаарна уу!\n"
        "- ТА регистерийн дугаараа үнэн зөв бөглөж, бүртгэлээ баталгаажуулна\n\n"
        "2️⃣ <b>Ажил эхлэх (Check-in):</b>\n"
        "- /checkin коммандыг бичнэ\n"
        "- 'Байршил илгээх' товч дээр дараад 'Live Location' (Хөдөлгөөнт байршил) сонгоно\n"
        "- Байршлаа амжилттай илгээснээр ажлын эхлэх цаг, байршил бүртгэгдэнэ\n\n"
        "3️⃣ <b>Ажил дуусах (Check-out):</b>\n"
        "- /checkout коммандыг бичнэ\n"
        "- 'Байршил илгээх' → мөн 'Live Location' илгээнэ\n"
        "- Дараа нь ажлын зураг болон товч тайлбар (хийсэн ажлын тухай) илгээнэ\n"
        "- Бот таны ажлын дуусах цаг, байршил, зураг, тайлбарыг бүртгэнэ\n\n"
        "4️⃣ <b>Үндсэн цэс харагдахгүй болсон үед:</b>\n"
        "- /start коммандыг бичиж, үндсэн цэсийг дахин гаргана\n\n"
        "<b>❓ Түгээмэл асуулт, асуудлын шийдэл:</b>\n"
        "<b>Байршил илгээх боломжгүй байна:</b>\n"
        "– Telegram апп-ийн тохиргоонд байршлын зөвшөөрлийг идэвхжүүлсэн эсэхээ шалгана\n"
        "– Гар утасны GPS асаалттай эсэхийг шалгана\n"
        "– Апп-аа бүрэн хаагаад дахин нээнэ\n\n"
        "<b>Бот ажиллахгүй эсвэл алдаа өгч байна:</b>\n"
        "– Интернэт холболтоо шалгана\n"
        "– Шаардлагатай бол Telegram апп-аа update хийнэ\n"
        "– /start эсвэл /help коммандуудыг ашиглаж дахин оролдоно\n\n"
        "<b>Бусад асуулт, тусламж хэрэгтэй бол:</b>\n"
        "– Энэ /help коммандыг ашиглаж болно\n"
        "– Эсвэл <a href=\"https://t.me/your_admin_link\">Админд хандах</a>\n\n"
        "<b>⚠️ Анхаар:</b>\n"
        "- Байршлын зөвшөөрлийг Telegram апп-д заавал идэвхжүүлсэн байх шаардлагатай!\n"
        "- 'Live Location' (хөдөлгөөнт байршил) илгээхгүй бол бүртгэл баталгаажихгүй!\n"
        "- Зөвхөн ажиллаж буй газрынхаа байршлыг илгээнэ үү!\n"
        "- Live Location буюу яг одоо байгаа өөрийнхаа байршилыг илгээхгүй бол бүртгэл хийгдэхгүй тул анхаарна уу.\n\n"
        "<b>📌 Хурдан зөвлөгөө:</b>\n"
        "- Коммандуудыг бичихэд эхэнд нь “/” тавихаа мартуузай: жишээ нь, <code>/checkin</code>\n"
        "- Үндсэн цэс үргэлж гарч ирэхгүй бол /start гэж бичнэ\n\n"
        "<b>Амжилт хүсье!</b>"
    )
    await message.answer(help_text, parse_mode="HTML", disable_web_page_preview=True)
