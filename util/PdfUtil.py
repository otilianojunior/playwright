import os
import PyPDF2


class PdfUtil:
    def __init__(self, db_name, empresa):
        self.db_name = db_name
        self.empresa = empresa

    def extract_text_from_pdf(self):
        try:
            directory = f'certidoes/{self.db_name}/certidao'
            filename = f'{self.empresa["cnpj"]}.pdf'
            file_path = os.path.join(directory, filename)

            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except Exception as ex:
            print(f"Erro ao extrair texto do PDF: {ex}")
