
import argparse
import glob
import os

from PyPDF2 import PdfFileReader


class PdfReader:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.pdf_list = glob.glob(os.path.join(folder_path, '*.pdf'))

    @staticmethod
    def get_info(pdf_path):
        path = pdf_path
        with open(path, 'rb') as f:
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()

        author = info.author
        title = info.title
        return author, title

    @staticmethod
    def generate_name(author, title):
        author_part = author.split(',')[0].split(' ')[-1]
        title_part = title.replace(' ', '_')
        return '-'.join([author_part, title_part]) + '.pdf'

    def rename_files(self):
        for pdf_file in self.pdf_list:
            author, title = self.get_info(pdf_file)
            new_name = self.generate_name(author, title)
            os.rename(pdf_file, os.path.join(self.folder_path, new_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Path to the folder with PDFs.')
    parser.add_argument('path', help='path to the folder with PDFs that will be renamed')

    args = parser.parse_args()

    reader = PdfReader(args.path)
    reader.rename_files()

