from fpdf import FPDF

class RecipePDF(FPDF):

    def set_recipe(self, recipe):
        self.recipe = recipe

    def header(self):
        # Setting font: helvetica bold 15
        self.set_font('helvetica', 'B', size=16)
        # Moving cursor to the right:
        self.cell(80)
        # Printing title:
        self.cell(30, 10, self.recipe.name, border=0, align='C')
        # Performing a line break:
        self.ln(20)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica 8
        self.set_font('helvetica', size=8)
        # Printing page number:
        self.cell(0, 10, f"{self.page_no()}/{{nb}}", align='C')
