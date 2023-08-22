import os

import sys

import colorama
import teracord

from .src import requests, user_agents


colorama.init()

settings = teracord.settings(factory = teracord.model.Standart)


def token_valid(token: str):
    client = teracord.gateaway.bot(
        token = token
    )

    client.resetStatus()
    return client.is_alive() & client.close()


class Menu(teracord.Menu):
    def __init__(self, *items):
        super().__init__(items)

    def show(self, clear: bool = True):
        if clear:
            os.system("cls" if os.name == 'nt' else 'clear')

        super().show()

main_menu = Menu(
    teracord.model.Menu
)
auth_menu = Menu(
    teracord.model.Auth
)
settings_menu = Menu(
    teracord.model.Settings
)


if __name__ == "__main__":
    while teracord.exec_():
        item_ = main_menu.show()

        match item_:
            case 1:
                if not settings.token:
                    teracord.Menu.err("Invalid token...", timeout = 2.5)
                    continue

                is_valid = token_valid(settings.token)
                
                if is_valid == True:
                    with requests.Session() as session:
                        teracord.run(
                            token      = settings.token,
                            session    = session,
                            user_agent = user_agents.parse(),
                            reconnect  = True
                        )

                        sys.exit(0)
                else:
                    teracord.Menu.err("Invalid token...", timeout = 2.5)
                    continue

            case 2:
                sub_item_ = auth_menu.show()
            
                if sub_item_ == 1:
                    settings.token = input("> ")

                elif sub_item_ == 2:
                    settings.token = teracord.os.walk(
                        system_type = os.name
                    )[-1]

            case 3:
                sub_item_ = settings_menu.show()

                if sub_item_:
                    teracord.settings.setter.exec_(value = f"3.{sub_item_}")

            case 4:
                sys.exit(0)