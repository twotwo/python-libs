import os
import platform
from io import BytesIO

from PIL import Image
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib import pagesizes, units
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import SimpleDocTemplate

if platform.system() == "Darwin":
    regular_path = os.path.join("~/Library/Fonts/Monofur for Powerline.ttf")
    italic_path = os.path.join("~/Library/Fonts/Monofur Italic for Powerline.ttf")

    pdfmetrics.registerFont(ttfonts.TTFont("Bold", regular_path))
    pdfmetrics.registerFont(ttfonts.TTFont("Medium", regular_path))
    pdfmetrics.registerFont(ttfonts.TTFont("Regular", regular_path))


# A4 页面外边距默认值 1.25 inch
MARGIN = 31.7 * units.mm


def build_pdf(flowables, pagesize=pagesizes.A4, margin=MARGIN):
    """根据 flowables 中的内容生成 pdf

    Args:
        flowables: content of pdf
        pagesize: default is pagesizes.A4
    Returns:
        store content in memory
    """
    pdf_buffer = BytesIO()
    # 更多配置信息，参考 BaseDocTemplate
    my_doc = SimpleDocTemplate(
        pdf_buffer, pagesize=pagesize, leftMargin=MARGIN, rightMargin=MARGIN
    )

    my_doc.build(flowables)
    # content = pdf_buffer.getbuffer()
    # pdf_buffer.close()
    return pdf_buffer


def new_line(width=210 * units.mm):
    """create a new line in pdf
    A4 = (210*mm,297*mm)
    """
    d = Drawing(width=width, height=1)
    d.hAlign = "CENTER"
    d.add(Line(x1=MARGIN, y1=0, x2=width - MARGIN, y2=0))
    return d


def load_image(fp):
    """load image with PIL.Image, convert to BytesIO

    Args:
        fp: Union[str, Path, BinaryIO]
    """
    img = BytesIO()
    Image.open(fp).save(img, "PNG")
    img.seek(0)
    return img
