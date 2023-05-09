# Imports
import os
import time
import requests
import io
from PIL import Image

from playwright.sync_api import sync_playwright, expect
import logging
import uuid

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False
uuid4 = uuid.uuid4()


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    # # Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    gender = execution.parameters.get('gender', 'Female')
    name_set = execution.parameters.get('name_set', 'Brazil')
    country = execution.parameters.get('country', 'Brazil')

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

    headless = True
    trace_path = r"C:\BotCity\Projetos\BotCityTCC_Files\Traces"
    files_path = r"C:\BotCity\Projetos\BotCityTCC_Files\Files"

    with sync_playwright() as playwright:
        try:
            def img_down(link):
                response = requests.get(link).content
                image_file = io.BytesIO(response)
                image = Image.open(image_file)
                image_path = os.path.join(files_path, (str(uuid4) + '.png'))
                with open(image_path, "wb") as f:
                    image.save(image_path, bitmap_format='png')
                    logging.info(f"Arquivo salvo: {image_path}")
                return image_path

            logging.info('Inicializando navegador.')
            browser = playwright.chromium.launch(headless=headless)
            context = browser.new_context(locale="pt-BR", viewport={"width": 1920, "height": 1080})

            logging.info('Inicializando tracing.')
            context.tracing.start(screenshots=True, snapshots=True, sources=True)

            logging.info('Abrindo nova página.')
            page = context.new_page()

            logging.info('Abrindo página de inicial.')
            page.goto('https://www.fakenamegenerator.com/')

            page.locator('select#gen').select_option(gender)
            page.locator('select#n').select_option(name_set)
            page.locator('select#c').select_option(country)

            page.locator('input#genbtn').click()

            name = page.locator('//div[@class="address"]/h3').inner_text()
            logging.info(f'Nome: {name}')

            address = page.locator('div.adr').inner_text().split('\n')
            logging.info(f'Endereço: {address[0]} - {address[1]} - {address[2]}')

            phone = page.locator('//dt[contains(text(), "Phone")]/../dd').inner_text()
            logging.info(f'Telefone: {phone}')

            img = page.locator(f'img[alt="{gender}"]').get_attribute('src')
            link_img = 'https://www.fakenamegenerator.com' + img
            photo = img_down(link_img)
            logging.info(f'Foto de perfil: {photo}')

            email = page.locator('//dt[contains(text(), "Email Address")]/../dd').inner_text().split('\n')[0]
            logging.info(f'E-mail: {email}')

            company = page.locator('//dt[contains(text(), "Company")]/../dd').inner_text()
            logging.info(f'Empresa: {company}')

            logging.info(f"---------------- Finalizando ----------------")
            page.close()

            logging.info('Finalizando relatório de execução e gravação.')
            context.tracing.stop(path=f"{trace_path}\\trace_{execution.task_id}_{uuid4}.zip")

            params = {
                'name': name,
                'address': address[0],
                'city': address[1],
                'cep': address[2],
                'phone': phone,
                'avatar': photo,
                'email': email,
                'company': company
            }

            task = maestro.create_task(
                activity_label="BotCityTCC_register",
                parameters=params,
                test=True
            )
            logging.info(f"Task gerada: {task.id}.")

            logging.info(f"Enviando artefato/trace.")
            maestro.post_artifact(
                task_id=execution.task_id,
                artifact_name=f"trace_{execution.task_id}_{uuid4}.zip",
                filepath=f"{trace_path}\\trace_{execution.task_id}_{uuid4}.zip"
            )

            maestro.finish_task(
                task_id=execution.task_id,
                status=AutomationTaskFinishStatus.SUCCESS,
                message="Task Finished with Success."
            )

        except Exception as e:
            logging.info(f"---------------- Finalizando com erro ----------------")
            logging.info(f"Erro: {e}")
            page.close()

            logging.info('Finalizando relatório de execução e gravação.')
            context.tracing.stop(path=f"{trace_path}\\trace_{execution.task_id}_{uuid4}_err.zip")

            maestro.finish_task(
                task_id=execution.task_id,
                status=AutomationTaskFinishStatus.FAILED,
                message="Task Failed."
            )

            exit(1)


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
