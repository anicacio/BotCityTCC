# Import for the Desktop Bot
from botcity.core import DesktopBot

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

import logging

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    # Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    name = execution.parameters.get('name', 'BOTCITY')
    address = execution.parameters.get('address', 'Rua Capitao Augusto Sales Pupo, 93')
    city = execution.parameters.get('city', 'CAMPINAS-SP')
    cep = execution.parameters.get('cep', '13070-114')
    phone = execution.parameters.get('phone', '(11) 98067-6036')
    avatar = execution.parameters.get('avatar', r'C:\BotCity\Projetos\BotCityTCC_Files\Files\sample.png')
    email = execution.parameters.get('email', 'gabriel@botcity.com.br')
    company = execution.parameters.get('company', 'BOTCITY DESENVOLVIMENTO DE SISTEMAS LTDA')

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

    bot = DesktopBot()

    logging.info("Abrindo aplicação")
    bot.execute(r"C:\Program Files (x86)\C-Organizer Lite\C-OrganizerLite.exe")

    logging.info("Aguardando abertura da aplicação")
    if not bot.find( "contatos", matching=0.97, waiting_time=120000):
        not_found("contatos")
    bot.click()
    
    if not bot.find( "novo_contato", matching=0.97, waiting_time=10000):
        not_found("novo_contato")
    bot.click()

    logging.info(f"Iniciando cadastro da task: {execution.task_id}\nNome: {name}")
    if not bot.find( "titulo", matching=0.97, waiting_time=10000):
        not_found("titulo")
    bot.click_relative(130, 9)
    bot.kb_type(name)

    if not bot.find( "nome", matching=0.97, waiting_time=10000):
        not_found("nome")
    bot.click_relative(233, 2)
    bot.kb_type(name)
    
    if not bot.find( "endereco", matching=0.97, waiting_time=10000):
        not_found("endereco")
    bot.click_relative(241, 5)
    bot.kb_type(address)
    
    if not bot.find( "cidade", matching=0.97, waiting_time=10000):
        not_found("cidade")
    bot.click_relative(237, 4)
    bot.kb_type(city)
    
    if not bot.find( "CEP", matching=0.97, waiting_time=10000):
        not_found("CEP")
    bot.click_relative(237, 6)
    bot.kb_type(cep)
    
    if not bot.find( "celular", matching=0.97, waiting_time=10000):
        not_found("celular")
    bot.click_relative(237, 5)
    bot.kb_type(phone)
    
    if not bot.find( "email", matching=0.97, waiting_time=10000):
        not_found("email")
    bot.click_relative(237, 2)
    bot.kb_type(email)
    
    if not bot.find( "scroll_down", matching=0.97, waiting_time=10000):
        not_found("scroll_down")
    bot.click()
    
    if not bot.find( "empresa", matching=0.97, waiting_time=10000):
        not_found("empresa")
    bot.click_relative(244, 5)
    bot.kb_type(company)
    
    if not bot.find( "avatar", matching=0.97, waiting_time=10000):
        not_found("avatar")
    bot.move()
    
    if not bot.find( "avatar_pasta", matching=0.97, waiting_time=10000):
        not_found("avatar_pasta")
    bot.click()

    bot.kb_type(avatar)
    bot.enter()
    
    if not bot.find( "aplicar", matching=0.97, waiting_time=10000):
        not_found("aplicar")
    bot.click()
    
    if not bot.find( "OK", matching=0.97, waiting_time=10000):
        not_found("OK")
    bot.click()
    
    bot.alt_f4()

    # Uncomment to mark this task as finished on BotMaestro
    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Task Finished OK."
    )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()

