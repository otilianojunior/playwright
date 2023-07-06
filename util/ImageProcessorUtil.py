import cv2
import logging


class ImageProcessorUtil:
    @classmethod
    def process_image(cls, db_name):
        try:
            img_path = f'/home/veri-developer/Documentos/PROJETOS/POCS/' \
                       f'PLAYWRIGHT/certidoes/{db_name}/img/captcha.png'
            img = cv2.imread(img_path)
            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            _, img_transform = cv2.threshold(img_gray, 127, 255, cv2.ADAPTIVE_THRESH_MEAN_C | cv2.THRESH_OTSU)

            output_path = f'/home/veri-developer/Documentos/PROJETOS/POCS/' \
                          f'PLAYWRIGHT/certidoes/{db_name}/img/captcha_transform.png'
            cv2.imwrite(output_path, img_transform)
        except Exception as ex:
            logging.info(ex)
            raise Exception

    @classmethod
    def load_img(cls, db_name):
        try:
            path = f'/home/veri-developer/Documentos/PROJETOS/POCS/PLAYWRIGHT/certidoes/{db_name}' \
                   f'/img/captcha_transform.png'
            img = cv2.imread(path)
            return img
        except Exception as ex:
            logging.info(ex)
            raise Exception
