from util.ImageProcessorUtil import ImageProcessorUtil
from playwright.async_api import async_playwright
from util.PdfUtil import PdfUtil
from dotenv import load_dotenv
import pytesseract as pyt
import logging
import asyncio
import shutil
import os


class RioGrandeNorte:
    def __init__(self, db_name, empresa):
        self.db_name = db_name
        self.empresa = empresa

    async def rio_grande_norte_estadual(self):
        try:
            await self.new_directory()
            async with async_playwright() as pw:
                navigate = await self.new_navigate(pw)
                page = await self.new_pag(navigate)
                await self.navigate_page(page)
                await self.click_input_cnpj(page)
                await self.set_cnpj(page)
                await self.screenshot_captcha(page)
                token = await self.solver_captcha()
                await self.set_captcha(page, token)
                await self.send_data(page)
                await self.get_validade()
        except Exception as ex:
            logging.info(ex)
            raise Exception
        finally:
            await self.delete_archives()

    async def new_directory(self):
        try:
            os.makedirs(f'certidoes/{self.db_name}', exist_ok=True)
            logging.info("new directory, sucesso.")
        except Exception as ex:
            logging.info(ex)
            raise Exception

    async def new_navigate(self, pw):
        try:
            load_dotenv()
            proxy_url = os.environ.get('PROXY_URL')
            browser = await pw.chromium.connect_over_cdp(proxy_url)
            return browser
        except Exception as ex:
            logging.info(ex)
            raise Exception

    async def new_pag(self, navigate):
        try:
            new_pag = await navigate.new_page()
            logging.info("New pag, sucesso.")
            return new_pag
        except Exception as ex:
            logging.info(ex)
            raise Exception

    async def navigate_page(self, page):
        try:
            pag_go = await page.goto('https://uvt2.set.rn.gov.br/#/services/certidao-negativa/emitir')
            logging.info("Navigate page, sucesso.")
            return pag_go
        except Exception as ex:
            logging.info(ex)
            raise Exception

    async def click_input_cnpj(self, page):
        try:
            await page.locator('xpath=//*[@id="identificacao"]').click()
            logging.info("Click Input Cnpj, sucesso.")
        except Exception as ex:
            logging.info(ex)
            raise Exception

    async def set_cnpj(self, page):
        try:
            await page.fill('xpath=//*[@id="identificacao"]', self.empresa['cnpj'])
            logging.info("Set Cnpj, sucesso.")
        except Exception as ex:
            logging.info(ex)
            raise Exception

    async def screenshot_captcha(self, page):
        try:
            img = await page.query_selector('xpath=/html/body/section/div/div[4]/div/form/div[1]/div/div[2]/div/div/img')
            await img.screenshot(path=f'certidoes/{self.db_name}/img/captcha.png')
            ImageProcessorUtil.process_image(self.db_name)
            logging.info("Screenshot Captcha, sucesso.")
        except Exception as ex:
            logging.info(ex)
            raise Exception

    async def solver_captcha(self):
        try:
            img = ImageProcessorUtil.load_img(self.db_name)
            token = pyt.image_to_string(img, lang='eng')
            logging.info("Solver Captcha, sucesso.")
            return token
        except Exception as ex:
            logging.info(ex)
            raise Exception

    async def set_captcha(self, page, token):
        try:
            await page.fill('xpath=//*[@id="captcha"]', token)
            logging.info("Set Captcha, sucesso.")
        except Exception as ex:
            logging.info(ex)
            raise Exception

    async def send_data(self, page):
        try:
            await asyncio.sleep(10)
            await page.locator('xpath=/html/body/section/div/div[4]/div/form/div[2]/div[1]/button').click()
            download = await page.wait_for_event('download')

            directory = f'certidoes/{self.db_name}/certidao'
            filename = f'{self.empresa["cnpj"]}.pdf'
            download_path = os.path.join(directory, filename)

            await download.save_as(download_path)

            logging.info("Send Data, sucesso.")
        except Exception as ex:
            logging.info(ex)
            raise Exception

    async def get_validade(self):
        try:
            PdfUtil.extract_text_from_pdf(self.db_name)
            logging.info("Get Validade, sucesso.")
        except Exception as ex:
            logging.info(ex)
            raise Exception

    async def delete_archives(self):
        try:
            directory = os.path.abspath(f'certidoes/{self.db_name}')
            shutil.rmtree(directory)
            logging.info("Delete Archives, sucesso.")
        except Exception as ex:
            logging.info(ex)
            raise Exception


if __name__ == '__main__':
    db_name = 'teste'
    empresa = {
        'cnpj': '28298593000133'
    }
    CND = RioGrandeNorte(db_name, empresa)

    asyncio.run(CND.rio_grande_norte_estadual())
