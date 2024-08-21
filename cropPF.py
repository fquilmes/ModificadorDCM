import tkinter as tk
from tkinter import filedialog, simpledialog
import pydicom
import numpy as np
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import filedialog
import pydicom
import numpy as np
import matplotlib.pyplot as plt

def crop_dicom():
    # Abrir diálogo para seleccionar archivo DICOM
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('DICOM Files', '*.dcm')])
    if not file_path:
        print('User pressed cancel')
        return None

    # Leer archivo DICOM seleccionado
    dicom_info = pydicom.dcmread(file_path,force=True)

    # Extraer la matriz de píxeles
    pixel_array = dicom_info.pixel_array

    # Seleccionar la columna central
    central_column = pixel_array[:, pixel_array.shape[1] // 2]

    # Filtrar las filas cuyos píxeles sean menores a 1000 o iguales a 4095
    filtered_indices = np.where((central_column >= 1000) & (central_column != 4095))[0]

    # Crear una nueva imagen recortada
    cropped_image = pixel_array[filtered_indices, :]

    # Mostrar la imagen original y la recortada para comparación (opcional)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(pixel_array, cmap='gray')

    plt.subplot(1, 2, 2)
    plt.title('Cropped Image')
    plt.imshow(cropped_image, cmap='gray')
    plt.show()

    # Crear un nuevo objeto FileDataset para la imagen recortada
    cropped_dicom_info = dicom_info.copy()
    cropped_dicom_info.PixelData = cropped_image.tobytes()
    cropped_dicom_info.Rows, cropped_dicom_info.Columns = cropped_image.shape

    # Devolver el objeto DICOM recortado
    return cropped_dicom_info





def main():
    cr_to_dcm()

if __name__ == '__main__':
    main()