from datetime import date, timedelta


def calculate_streak(dates):
    """
    Принимает список или множество дат (объекты datetime.date).
    Возвращает длину текущего стрика (последовательных дней учёбы до сегодня).
    """
    if not dates:
        return 0

    # Преобразуем во множество для быстрого поиска
    dates_set = set(dates)
    streak = 0
    current_day = date.today()

    # Пока текущий день есть в списке — увеличиваем стрик
    while current_day in dates_set:
        streak += 1
        current_day -= timedelta(days=1)

    return streak