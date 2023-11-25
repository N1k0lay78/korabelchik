from UI.init import add_all
from config import db_path, token
from korabelchik.Bot import Korabelchik

bot = Korabelchik(token, db_path)

add_all(bot)

bot.run()
