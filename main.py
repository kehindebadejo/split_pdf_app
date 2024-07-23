import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from PyPDF2 import PdfReader, PdfWriter


class SplitPDFApp(App):
    def build(self):
        self.title = "PDF Splitter"
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label = Label(text="Select a PDF file to split")
        layout.add_widget(self.label)

        self.filechooser = FileChooserIconView(filters=["*.pdf"])
        layout.add_widget(self.filechooser)

        self.split_button = Button(text="Split PDF", on_press=self.split_pdf)
        layout.add_widget(self.split_button)

        self.status = Label(text="")
        layout.add_widget(self.status)

        return layout

    def split_pdf(self, instance):
        selected = self.filechooser.selection
        if selected:
            input_path = selected[0]
            if os.path.exists(input_path):
                self.status.text = "Splitting PDF..."
                self.split_pdf_file(input_path)
                self.status.text = "PDF split successfully!"
            else:
                self.status.text = "The specified file does not exist. Please check the path and try again."
        else:
            self.status.text = "No file selected. Please select a PDF file."

    def split_pdf_file(self, input_path):
        output_folder = os.path.dirname(input_path)
        base_filename = os.path.splitext(os.path.basename(input_path))[0]

        with open(input_path, 'rb') as file:
            pdf = PdfReader(file)
            for page_num in range(len(pdf.pages)):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf.pages[page_num])
                output_filename = f'{base_filename}_page_{page_num + 1}.pdf'
                output_path = os.path.join(output_folder, output_filename)
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                print(f'Created: {output_filename}')


if __name__ == '__main__':
    SplitPDFApp().run()
