
import argparse
import glob
import os
import shutil

from PyPDF2 import PdfFileReader


class PdfReader:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.pdf_list = glob.glob(os.path.join(folder_path, '*.pdf'))
        self.renamed_folder = os.path.join(self.folder_path, 'renamed')
        self.failed_folder = os.path.join(self.folder_path, 'failed')

    @staticmethod
    def get_info(pdf_path):
        path = pdf_path
        with open(path, 'rb') as f:
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
        author = info.author
        title = info.title
        return author, title

    def generate_name(self, author, title):
        author_part = author.split(',')[0].split(' ')[-1]
        title_part = title.replace(' ', '_')
        new_name = '-'.join([author_part, title_part]) + '.pdf'
        new_path = os.path.join(self.renamed_folder, new_name)
        deduplication_number = 0
        while os.path.isfile(new_path):
            new_name = '-'.join([author_part, title_part, str(deduplication_number)]) + '.pdf'
            new_path = os.path.join(self.renamed_folder, new_name)
            deduplication_number += 1
        return new_path

    def copy_files(self):
        fail_counter = 0
        try:
            os.mkdir(os.path.join(self.folder_path, self.renamed_folder))
            os.mkdir(os.path.join(self.folder_path, self.failed_folder))
        except FileExistsError:
            input_value = input('Path exists, you want to continue? y/n ')
            if input_value != 'y':
                raise FileExistsError
        for pdf_file in self.pdf_list:
            try:
                author, title = self.get_info(pdf_file)
                if author == '' or author is None or title == '' or title is None:
                    print(f"Failed renaming with file {pdf_file}.")
                    print(f"The detected values were author: {author} and title: {title}.")
                    fail_counter += 1
                    continue
                new_path = self.generate_name(author, title)
                shutil.copyfile(pdf_file, new_path)
            except Exception as e:
                print(e)
                fail_counter += 1

        print(f"Fail ratio: {fail_counter}/{len(self.pdf_list)}.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Path to the folder with PDFs.')
    parser.add_argument('path', help='path to the folder with PDFs that will be renamed')

    args = parser.parse_args()

    reader = PdfReader(args.path)
    reader.copy_files()

