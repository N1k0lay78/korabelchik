from korabelchik2.Bot import Bot
from korabelchik2.run.commands import *

from config import token, db_path


def run():
    bot = Bot(token, db_path)
    bot.add_command(HelpCommand(bot))
    bot.add_command(IDCommand(bot))
    bot.add_command(InfoCommand(bot))
    bot.add_command(PageCommand(bot))
    bot.add_command(RolesCommand(bot))
    # login
    bot.add_command(StartCommand(bot))
    # tester
    bot.add_command(SetPageCommand(bot))
    bot.add_command(GetUserCommand(bot))
    bot.add_command(LikeCommand(bot))
    bot.add_command(WarnCommand(bot))
    bot.add_command(LikesMeCommand(bot))
    bot.add_command(LikesThemCommand(bot))
    bot.add_command(AcceptCommand(bot))
    # moderator
    bot.add_command(WarnsCommand(bot))
    bot.add_command(BanCommand(bot))
    bot.add_command(UnbanCommand(bot))
    bot.run()
