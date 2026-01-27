change_instructions = """<b>Замена</b> инструкций для нейросети

Напишите <b>Новые</b> инструкции для нейросети через точку,
либо введите <b>Отмена</b>, чтобы оставить текущие настройки"""

back_to_menu = """Вы снова в меню"""

success_instruction_change = "Инструкции изменены"

automod_changing = "Поставьте на отзывы с камими оценками ответы будут отправляться без модерации."

diagnos_wait = 'Идет диагностика, подождите'


def diagnos_result(proxy_check, gpt_check, wb_checks: list):
    result = ' Диагностика завершена\n'
    if proxy_check:
        result += f'✅ Прокси работает {proxy_check[0]}'
    else:
        result += f'⛔️ Прокси не работает'
    result += '\n'

    if gpt_check[0]:
        result += f'✅ openAI токен работает'
    else:
        result += f'⛔️ openAI токен не работает {gpt_check[1]}'
    result += '\n'

    for wb_check in wb_checks:
        if wb_check[0]:
            result += f'✅ WB токен работает'
        else:
            result += f'⛔️ WB токен не работает {wb_check[1]}'
        result += '\n'

    return result


