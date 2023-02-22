
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

from api.utils import get_currencies_from_nb_kz



# Создаем планировщик задач
scheduler = BackgroundScheduler()

# Задаем дату, для которой нужно получить данные
today = datetime.date.today()
fdate = today.strftime("%d.%m.%Y")

# Определяем функцию, которая будет выполняться каждый день в 6 утра
@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=6)
async def get_daily_currencies():
    """
    Получает данные о курсах валют на текущую дату и сохраняет их в формате JSON в файл.
    """
    await get_currencies_from_nb_kz(fdate)

# Запускаем планировщик задач
scheduler.start()
