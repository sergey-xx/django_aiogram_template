from typing import Optional

from aiogram.filters.callback_data import CallbackData


class PaginationCallbackData(CallbackData, prefix='pag'):

    page: Optional[int]
    category: bool
    sub_category: bool
    category_id: int
