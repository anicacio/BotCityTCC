# Import for integration with BotCity Maestro SDK
import random
import time

from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

gender_list = ['Male', 'Female']
name_set_list = ['American', 'Brazil', 'Ninja', 'Igbo', 'Hobbit']


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK()
    maestro.login(server="https://training.botcity.dev", login="INSIRA_LOGIN_AQUI", key="INSIRA_KEY_AQUI")

    for n in range(10):
        params = {
            'gender': gender_list[random.randint(0, 1)],
            'name_set': name_set_list[random.randint(0, 4)]
        }
        task = maestro.create_task(
            activity_label="BotCityTCC_generator",
            parameters=params,
            test=True
        )
        print(f"Task criada {task.id} - {params}")
        # time.sleep(15)
        # input()


if __name__ == '__main__':
    main()
