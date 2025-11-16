from pathlib import Path

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from ...schemas.product import ProductUpdateSchema
from ...managers import ProductManager
from ...core.const import PATH_TO_SAVE_IMAGE
from ..state import Update

def update_init(api: ProductManager):
    router = Router()
    @router.callback_query(F.data.startswith("updtitle-"))
    async def handle_update_title(callback: CallbackQuery, state: FSMContext):
        """
        Хендлер для обновления названия товара
        """
        product_id = int(callback.data.split("-")[1])
        
        await callback.message.answer(
            f"Введите новое название для товара (ID: {product_id}):"
        )
        await state.set_state(Update.waiting_for_new_title)
        await state.update_data(product_id=product_id)

    @router.callback_query(F.data.startswith("updprice-"))
    async def handle_update_price(callback: CallbackQuery, state: FSMContext):
        """
        Хендлер для обновления цены товара
        """
        product_id = int(callback.data.split("-")[1])
        
        await callback.message.answer(
            f"Введите новую цену для товара (ID: {product_id}):"
        )
        await state.set_state(Update.waiting_for_new_price)
        await state.update_data(product_id=product_id)

    @router.callback_query(F.data.startswith("updcount-"))
    async def handle_update_count(callback: CallbackQuery, state: FSMContext):
        """
        Хендлер для обновления количества товаров
        """
        product_id = int(callback.data.split("-")[1])
        
        await callback.message.answer(
            f"Введите новое количество для товара (ID: {product_id}):"
        )
        await state.set_state(Update.waiting_for_new_count)
        await state.update_data(product_id=product_id)

    @router.callback_query(F.data.startswith("updesc-"))
    async def handle_update_description(callback: CallbackQuery, state: FSMContext):
        """
        Хендлер для обновления описания товара
        """
        product_id = int(callback.data.split("-")[1])
        
        await callback.message.answer(
            f"Введите новое описание для товара (ID: {product_id}):"
        )
        await state.set_state(Update.waiting_for_new_description)
        await state.update_data(product_id=product_id)

    @router.callback_query(F.data.startswith("updposter-"))
    async def handle_update_poster(callback: CallbackQuery, state: FSMContext):
        """
        Хендлер для обновления постера товара
        """
        product_id = int(callback.data.split("-")[1])
        
        await callback.message.answer(
            f"Отправьте новое изображение для товара (ID: {product_id}):"
        )
        await state.set_state(Update.waiting_for_new_poster)
        await state.update_data(product_id=product_id)
        
    
    @router.message(Update.waiting_for_new_title, F.text)
    async def update_title(message: Message, state: FSMContext):
        try:
            data = await state.get_data()
            upd = ProductUpdateSchema(id=data['product_id'], title=message.text)
            await api.update_product(upd)
            await message.answer("Успешно удалось изменить название")
            await state.clear()
        except Exception as e:
            await message.answer(
                (
                    "Ошибка при обновлении название!\n"
                    f"Подробнее: {str(e)}"
                )
            )
            
    @router.message(Update.waiting_for_new_price, F.text)
    async def update_price(message: Message, state: FSMContext):
        try:
            data = await state.get_data()
            price = float(message.text)
            upd = ProductUpdateSchema(id=data['product_id'], price=price)
            await api.update_product(upd)
            await message.answer("Успешно удалось изменить цену")
            await state.clear()
        except ValueError:
            await message.answer("Пожалуйста используйте числа")
            
        except Exception as e:
            await message.answer(
                (
                    "Ошибка при обновлении цены!\n"
                    f"Подробнее: {str(e)}"
                )
            )
            
    @router.message(Update.waiting_for_new_count, F.text)
    async def update_count(message: Message, state: FSMContext):
        try:
            data = await state.get_data()
            if not float(message.text).is_integer():
                await message.answer("Используйте целые числа")
                return
            
            count = int(message.text)
            upd = ProductUpdateSchema(id=data['product_id'], count=count)
            await api.update_product(upd)
            await message.answer("Успешно удалось изменить количество")
            await state.clear()
        except ValueError:
            await message.answer("Пожалуйста используйте числа")
            
        except Exception as e:
            await message.answer(
                (
                    "Ошибка при обновлении количество!\n"
                    f"Подробнее: {str(e)}"
                )
            )

    @router.message(Update.waiting_for_new_description, F.text)
    async def update_description(message: Message, state: FSMContext):
        try:
            data = await state.get_data()

            description = message.text
            upd = ProductUpdateSchema(id=data['product_id'], description = description)
            await api.update_product(upd)
            await message.answer("Успешно удалось изменить описнаие")
            await state.clear()

        except Exception as e:
            await message.answer(
                (
                    "Ошибка при обновлении описание!\n"
                    f"Подробнее: {str(e)}"
                )
            )
            
    @router.message(Update.waiting_for_new_poster, F.photo)
    async def update_count(message: Message, state: FSMContext):
        try:
            data = await state.get_data()
            photo = message.photo[-1]
            photo_id = photo.file_id
            
            data = await state.get_data()
            file = await message.bot.get_file(photo_id)
            PATH_TO_SAVE_IMAGE.mkdir(parents=True, exist_ok=True)
            download_path = PATH_TO_SAVE_IMAGE / (photo_id + Path(file.file_path).suffix if file.file_path else ".jpg")
            await message.bot.download_file(file.file_path, download_path)
            
            upd = ProductUpdateSchema(id=data['product_id'], poster = str(download_path))
            await api.update_product(upd)
            await message.answer("Успешно удалось изменить постер")
            await state.clear()

        except Exception as e:
            await message.answer(
                (
                    "Ошибка при обновлении постер!\n"
                    f"Подробнее: {str(e)}"
                )
            )
    return router