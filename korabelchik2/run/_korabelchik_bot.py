from korabelchik2.Bot import Bot
from korabelchik2.run.AdminCommands import *
from korabelchik2.run.InfoCommands import *
from korabelchik2.run.LoginCommands import *
from korabelchik2.run.LookingForCommands import *
from korabelchik2.run.MenuCommands import *
from korabelchik2.run.ModeratorCommands import *

from config import token, db_path


def run():
    bot = Bot(token, db_path)

    # ===== default =====

    bot.add_command(HelpCommand(bot))
    bot.add_command(IDCommand(bot))
    bot.add_command(DinoCommand(bot))
    bot.add_command(InfoCommand(bot))
    bot.add_command(PageCommand(bot))
    bot.add_command(RolesCommand(bot))

    # ===== READY =====

    # --- login ---
    # start
    bot.add_command(StartCommand(bot))
    # profile info
    # bot.add_command(AskProfileInfoCommand(bot))
    # bot.add_command(SetProfileInfoCommand(bot))
    # age
    bot.add_command(AskAgeCommand(bot))
    bot.add_command(SetAgeCommand(bot))
    # gender
    bot.add_command(AskGenderCommand(bot))
    bot.add_command(SetGenderCommand(bot))
    # faculty
    bot.add_command(AskFacultyCommand(bot))
    bot.add_command(SetFacultyCommand(bot))
    # about text
    bot.add_command(AskAboutTextCommand(bot))
    bot.add_command(SetAboutTextCommand(bot))
    # image
    # bot.add_command(AskImageCommand(bot))
    # bot.add_command(SetImageCommand(bot))

    bot.add_command(MainPageCommand(bot))
    bot.add_command(EditPageCommand(bot))
    bot.add_command(ProfilePageCommand(bot))
    bot.add_command(ToggleQuestionnaireCommand(bot))
    bot.add_command(ViewMyCommand(bot))
    bot.add_command(LookingForCommand(bot))
    bot.add_command(LookingForCommand(bot))

    # ===== NEED TO DO ====

    # --- tester ---
    bot.add_command(SetPageCommand(bot))
    bot.add_command(GetUserCommand(bot))
    bot.add_command(ReactionCommand(bot))
    # bot.add_command(WarnCommand(bot))
    bot.add_command(LikesMeCommand(bot))
    bot.add_command(LikesThemCommand(bot))
    bot.add_command(AcceptCommand(bot))
    # --- moderator ---
    bot.add_command(WarnsCommand(bot))
    bot.add_command(BanCommand(bot))
    bot.add_command(UnbanCommand(bot))
    bot.run()
