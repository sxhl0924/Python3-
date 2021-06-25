import zipfile
import io
from PIL import Image, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np


def detect_faces(search_term, zipfile_name):
    file = zipfile.ZipFile(zipfile_name, 'r')
    search_string = search_term

    zip_contents = []
    zip_imgs = []
    file_names = []
    for name in file.namelist():
        file_names.append(name)
        image = file.read(name)
        image = Image.open(io.BytesIO(image))
        zip_imgs.append(image)
        image = np.asarray(image, dtype = 'uint8')
        zip_contents.append(image)

    text_contents = []
    for img in zip_imgs:
        text = pytesseract.image_to_string(img)
        text_contents.append(text)

    search_results = []
    for article in text_contents:
        if search_string in article:
            search_results.append(True)
        else:
            search_results.append(False)

    results_by_name = {}
    for name, result in zip(file_names, search_results):
        results_by_name[name] = result

    face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
    cropped_faces = []
    info_sheets = []
    index = 0
    named_sheets = {}
    for pic in zip_contents:
        faces = face_cascade.detectMultiScale(pic, scaleFactor = 1.2, minSize = (50, 50))
        tups = [(x, y, x + w, y + h) for x, y, w, h in faces]
        img = Image.fromarray(pic)
        contact_sheet = Image.new(img.mode, (200 * 4, 200 * 3))

        x = 0
        y = 0
        num_cropped = 0
        for tup in tups:
            cropped = img.crop(tup)
            cropped = cropped.resize((200, 200))
            cropped_faces.append(cropped)
            contact_sheet.paste(cropped, (x, y))
            if x + 200 == contact_sheet.width:
                x = 0
                y = y + 200
            else:
                x = x + 200
            num_cropped += 1

        rect = Image.new(contact_sheet.mode, (contact_sheet.width, 100), color = (255, 255, 255))
        d = ImageDraw.Draw(rect)
        d.text((10, 10), 'Results found in {}'.format(file_names[index]), fill = (0, 0, 0))
        if num_cropped == 0:
            d.text((10, 20), 'But there were no faces in that file!', fill = (0, 0, 0))
        index += 1
        info_sheet = Image.new(contact_sheet.mode, (contact_sheet.width, contact_sheet.height + rect.height))
        info_sheet.paste(rect, (0, 0))
        info_sheet.paste(contact_sheet, (0, 100))
        info_sheets.append(info_sheet)


    for name, sheet in zip(file_names, info_sheets):
        named_sheets[name] = sheet


    for name in results_by_name:
        if results_by_name[name] == True:
            display(named_sheets[name])
