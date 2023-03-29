import fitz

file = fitz.open("telekom_2017_report.pdf")


txt = open('telekom_report.txt', 'wb')

pageNum = 0
for page in file:
    pageNum += 1
    # Extract text
    text = page.get_text().encode("utf8")
    txt.write(text)
    #txt.write(bytes((12,)))
    # Extract image
    imgNum=0
    for img in page.get_images():
        print(img)
        imgHasContent = img[7] != 'Im0'
        imgNum+=1
        xref = img[0]
        pix = fitz.Pixmap(file, xref)

        # if pix.n > 4:
        #     pix = fitz.Pixmap(fitz.csRGB, pix)
        if not pix.colorspace.name in (fitz.csGRAY.name, fitz.csRGB.name):
            pix = fitz.Pixmap(fitz.csRGB, pix)
        if imgHasContent:
            pix.save("images_telekom/image-p.%i-%i.png" % (pageNum, imgNum))  # store image as a PNG
txt.close()

