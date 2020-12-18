import PyPDF2
from gtts import gTTS
from appJar import gui
from pathlib import Path
import cv2
import pytesseract


def image_to_text(input_file, output_file):
    pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'
    img = cv2.imread(input_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    im2 = img.copy()
    file = open(f'{output_file}.txt', "w+")
    file.write("")
    file.close()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Open the file in append mode
        file = open(f'{output_file}.txt', "a")

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

        # Appending the text into file
        file.write(text)
        file.write("\n")

        # Close the file
        file.close

    if (app.questionBox("File Save", "Output saved. Amar Do you want to quit?")):
            app.stop()


def validate_inputs(src_file, dest_dir, out_file):
    errors = False
    error_msgs = []
    if (Path(src_file).suffix.lower() != ".jpg"):
        errors = True
        error_msgs.append("Please select a .jpg input file")

    if not (Path(dest_dir)).exists():
        errors = True
        error_msgs.append("Please Select a valid output directory")

    # Check for a file name
    if len(out_file) < 1:
        errors = True
        error_msgs.append("Please enter a file name")

    return (errors, error_msgs)


def press(button):
    if button == "Process":
        src_file = app.getEntry("Input_File")
        dest_dir = app.getEntry("Output_Directory")
        out_file = app.getEntry("Output_name")
        errors, error_msg = validate_inputs(src_file, dest_dir, out_file)
        if errors:
            app.errorBox("Error", "\n".join(error_msg), parent=None)
        else:
            image_to_text(src_file, Path(dest_dir, out_file))
    else:
        app.stop()


app = gui("image to text file Amar Spandan 9849850456", useTtk=True)
app.setTtkTheme('alt')
app.setSize(1000, 1000)

# Add the interactive components
app.addLabel("Choose Source image File to convert to text")
app.addFileEntry("Input_File")

app.addLabel("Select Output Directory")
app.addDirectoryEntry("Output_Directory")

app.addLabel("Output text file name")
app.addEntry("Output_name")

app.addButtons(["Process", "Quit","Amar Spandan 9849850456"], press)
app.go()
