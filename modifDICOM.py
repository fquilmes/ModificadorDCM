import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pydicom
import numpy as np
import sys

def ui_get_dicom_file():
    """
    Opens a file dialog to select a DICOM file and returns the DICOM information, pixel data, file path, file name, and full name.

    This function opens a file dialog. The file dialog filters the files to only show DICOM files with the extension `.dcm`. If a file is selected, the file path is split to extract the file name and directory. The DICOM file is then read using `pydicom` to obtain the DICOM information and pixel data.

    Returns:
        tuple: [Dataset, numpy.ndarray or None, str, str, str]: A tuple containing the DICOM information (Dataset), pixel data (numpy.ndarray or None), file path (str), file name (str), and full name (str).
    """
    root = tk.Tk()
    root.withdraw()
    full_name = filedialog.askopenfilename(filetypes=[('DICOM Files', '*.dcm;*.img')])
    if full_name:
        file_path, file_name = os.path.split(full_name)  # Extract the directory and filename from the full path
        dicom_info = pydicom.dcmread(full_name,force=True)
        pixel_data = dicom_info.pixel_array if hasattr(dicom_info, 'pixel_array') else None
        return dicom_info, pixel_data, file_path, file_name, full_name
    else:
        return None, None, None, None, None
    
def get_dicom_file(full_name):
    """
    Opens a DICOM file and returns the DICOM information, pixel data, file path, file name, and full name.

    The DICOM file is then read using `pydicom` to obtain the DICOM information and pixel data.

    Returns:
        tuple: [Dataset, numpy.ndarray or None, str, str]: A tuple containing the DICOM information (Dataset), pixel data (numpy.ndarray or None), file path (str), and file name (str).
    """
    file_path, file_name = os.path.split(full_name)  # Extract the directory and filename from the full path
    dicom_info = pydicom.dcmread(full_name,force=True)
    pixel_data = dicom_info.pixel_array if hasattr(dicom_info, 'pixel_array') else None
    return dicom_info, pixel_data, file_path, file_name

def get_dose_reference_sequence(dicom_info):
    """
    Returns the DoseReferenceSequence from the given DICOM info.

    Args:
        dicom_info (pydicom.dataset.Dataset): The DICOM info containing the DoseReferenceSequence.

    Returns:
        pydicom.sequence.Sequence: The DoseReferenceSequence from the DICOM info.
    """ 
    return dicom_info.DoseReferenceSequence

def get_tolerace_table_sequence(dicom_info):   
    """
    Get the ToleranceTableSequence from the given DICOM info.

    Args:
        dicom_info (pydicom.dataset.Dataset): The DICOM info containing the ToleranceTableSequence.

    Returns:
        pydicom.sequence.Sequence: The ToleranceTableSequence from the DICOM info.
    """ 
    return dicom_info.ToleranceTableSequence

def get_fraction_group_sequence(dicom_info):
    """
    Returns the FractionGroupSequence from the given DICOM info.

    Args:
        dicom_info (pydicom.dataset.Dataset): The DICOM info containing the FractionGroupSequence.

    Returns:
        pydicom.sequence.Sequence: The FractionGroupSequence from the DICOM info.
    """
    return dicom_info.FractionGroupSequence

def get_beam_sequence(dicom_info):
    """
    Returns the BeamSequence from the given DICOM info.

    Args:
        dicom_info (pydicom.dataset.Dataset): The DICOM info containing the BeamSequence.

    Returns:
        pydicom.sequence.Sequence: The BeamSequence from the DICOM info.
    """
    return dicom_info.BeamSequence

def get_patient_setup_sequence(dicom_info):
    """
    Returns the PatientSetupSequence from the given DICOM info.

    Args:
        dicom_info (pydicom.dataset.Dataset): The DICOM info containing the PatientSetupSequence.

    Returns:
        pydicom.sequence.Sequence: The PatientSetupSequence from the DICOM info.
    """
    return dicom_info.PatientSetupSequence

def get_referenced_structure_set_sequence(dicom_info):
    """
    Returns the ReferencedStructureSetSequence from the given DICOM info.

    Args:
        dicom_info (pydicom.dataset.Dataset): The DICOM info containing the ReferencedStructureSetSequence.

    Returns:
        pydicom.sequence.Sequence: The ReferencedStructureSetSequence from the DICOM info.
    """
    return dicom_info.ReferencedStructureSetSequence

def get_number_of_beams(dicom_info):
    """
    Returns the number of beams in the given DICOM info.

    Args:
        dicom_info (pydicom.dataset.Dataset): The DICOM info containing the number of beams.

    Returns:
        int: The number of beams in the DICOM info.
    """
    return len(dicom_info.BeamSequence)

def ui_modify_gantry_angles(dicom_info):
    """
    Modifies the gantry angles of the given DICOM info.

    This function iterates over the BeamSequence of the DICOM info and prompts the user to change the gantry angle
    of each beam. The function creates a window to display the current gantry angle and asks the user if they want to
    change it. If the user confirms, the function prompts the user to enter a new gantry angle within the range of 0 to
    360. If the user enters a valid angle, the gantry angle of the corresponding beam is updated. If the user enters an
    invalid angle, an error message is displayed.

    Args:
        dicom_info (pydicom.dataset.Dataset): The DICOM info containing the BeamSequence.

    Returns:
        None
    """
    if hasattr(dicom_info, 'BeamSequence'):
        beam_sequence = dicom_info.BeamSequence
        for i, beam in enumerate(beam_sequence):
            gantry_angle = beam.ControlPointSequence[0].GantryAngle
            beam_name = beam.BeamName if hasattr(beam, 'BeamName') else 'NN'

            # Crear ventana para mostrar el ángulo actual y preguntar si desea cambiarlo
            root = tk.Tk()
            root.withdraw()
            change_angle = messagebox.askyesno("Modificar ángulo de gantry", f"Beam {i+1} ({beam_name}): El ángulo actual de gantry es {gantry_angle}°. ¿Desea cambiarlo?")

            if change_angle:
                valid_input = False
                while not valid_input:
                    new_angle = simpledialog.askinteger("Nuevo ángulo", "Ingrese un nuevo ángulo de gantry (0-360):", minvalue=0, maxvalue=360)
                    if new_angle is not None:
                        valid_input = True
                        beam.ControlPointSequence[0].GantryAngle = new_angle
                    else:
                        messagebox.showerror("Entrada no válida", "Por favor ingrese un número válido entre 0 y 360.")
            
            root.destroy()

def ui_modify_collimator_angles(dicom_info):
    """
    Modifies the collimator angles of the given DICOM info.

    This function iterates over the BeamSequence of the DICOM info and prompts the user to change the collimator angle
    of each beam. The function creates a window to display the current collimator angle and asks the user if they want to
    change it. If the user confirms, the function prompts the user to enter a new collimator angle within the range of (100-0 o 360-260). 
    If the user enters a valid angle, the collimator angle of the corresponding beam is updated. If the user enters an
    invalid angle, an error message is displayed.

    Args:
        dicom_info (pydicom.dataset.Dataset): The DICOM info containing the BeamSequence.

    Returns:
        None
    """
    if hasattr(dicom_info, 'BeamSequence'):
        beam_sequence = dicom_info.BeamSequence
        for i, beam in enumerate(beam_sequence):
            collimator_angle = beam.ControlPointSequence[0].BeamLimitingDeviceAngle
            beam_name = beam.BeamName if hasattr(beam, 'BeamName') else 'NN'

            # Crear ventana para mostrar el ángulo actual y preguntar si desea cambiarlo
            root = tk.Tk()
            root.withdraw()
            change_angle = messagebox.askyesno("Modificar ángulo del colimador", f"Beam {i+1} ({beam_name}): El ángulo actual del colimador es {collimator_angle}°. ¿Desea cambiarlo?")

            if change_angle:
                valid_input = False
                while not valid_input:
                    new_angle = simpledialog.askinteger("Nuevo ángulo", "Ingrese un nuevo ángulo del colimador (100-0 o 360-260):")
                    if new_angle is not None and ((0 <= new_angle <= 100) or (260 <= new_angle <= 360)):
                        valid_input = True
                        beam.ControlPointSequence[0].BeamLimitingDeviceAngle = new_angle
                    else:
                        messagebox.showerror("Entrada no válida", "Por favor ingrese un número válido entre (100-0 o 360-260)")
            
            root.destroy()

def modificar_portal_possition(dicom_info):
    """
    Recorre todos los beams en BeamSequence, muestra el valor actual de RTImageSID y permite cambiarlo.
    
    Args:
        dicom_info (pydicom.Dataset): El dataset DICOM que contiene la información de los beams.
    """
    if hasattr(dicom_info, 'BeamSequence'):
        for beam in dicom_info.BeamSequence:
            beam_name = beam.BeamName
            if hasattr(beam, 'PlannedVerificationImageSequence'):
                for verification_image in beam.PlannedVerificationImageSequence:
                    if hasattr(verification_image, 'RTImageSID'):
                        current_sid = (verification_image.RTImageSID - 1000)/10

                        # Mostrar mensaje con el valor actual de RTImageSID y preguntar si desea cambiarlo
                        root = tk.Tk()
                        root.withdraw()
                        if current_sid == 0:
                            message = f"Campo [{beam_name}]: La posición del portal es el ISO. ¿Desea cambiarlo?"
                        else:
                            message = f"Campo [{beam_name}]: La posición del portal es {current_sid} cm debajo del ISO. ¿Desea cambiarlo?"
                        change_sid = messagebox.askyesno("Modificar RTImageSID", message)

                        if change_sid:
                            valid_input = False
                            while not valid_input:
                                new_sid = simpledialog.askinteger("Nuevo RTImageSID", "Ingrese la nueva posición del portal en cm:")
                                if new_sid is not None:
                                    valid_input = True
                                    verification_image.RTImageSID = (new_sid*10 + 1000)
                                else:
                                    messagebox.showerror("Entrada no válida", "Por favor ingrese un número válido.")

                        root.destroy()


def set_tolerances_to_qa(dicom_info):
    """
    Modifica la tabla de tolerancia de un archivo DICOM.

    Args:
        dicom_info (pydicom.dataset.FileDataset): Información del archivo DICOM.
    """
    if hasattr(dicom_info, 'ToleranceTableSequence'):        
        tolerance_table = dicom_info.ToleranceTableSequence[0]

        tolerance_table.ToleranceTableNumber = 3
        tolerance_table.ToleranceTableLabel = 'T_QA'
        tolerance_table.GantryAngleTolerance = 180
        tolerance_table.BeamLimitingDeviceAngleTolerance = 90
        tolerance_table.PatientSupportAngleTolerance = 90
        tolerance_table.TableTopVerticalPositionTolerance = 2000
        tolerance_table.TableTopLongitudinalPositionTolerance = 2000
        tolerance_table.TableTopLateralPositionTolerance = 200
    for beam in dicom_info.BeamSequence:
        beam.ReferencedToleranceTableNumber = 3


def ui_select_machine():
    def get_selected_option():
        selected_option.set(option_var.get())
        root.quit()  # Termina el mainloop

    root = tk.Tk()
    root.title("Seleccione el equipo")
    root.geometry("220x160")  # Establecer el tamaño de la ventana (ancho x alto)

    label = tk.Label(root, text="Seleccione el equipo:")
    label.pack(pady=10)

    option_var = tk.StringVar(root)
    option_var.set('-')  # Opción predeterminada

    option_menu = tk.OptionMenu(root, option_var, "Equipo 1 (QBA_600CD_523)", "Equipo 2 (EQ2_iX_827)")
    option_menu.pack(pady=10)

    selected_option = tk.StringVar()

    button = tk.Button(root, text="Seleccionar", command=get_selected_option)
    button.pack(pady=10)

    root.mainloop()  # Corre el mainloop de tkinter

    result = selected_option.get()  # Obtiene el valor seleccionado
    root.destroy()  # Destruye la ventana después de obtener el valor
    return result

def update_beam_params(dicom_info, equipo_destino):
    """
    Update the manufacturer, institution, model name, serial number, and treatment machine name of all beams in the BeamSequence of the given DICOM info based on the equipment destination.

    Args:
        dicom_info (pydicom.dataset.FileDataset): The DICOM info containing the BeamSequence.
        equipo_destino (str): The equipment destination.

    Returns:
        None
    """
    if equipo_destino == "Equipo 1 (QBA_600CD_523)":
        new_manufacturer = "Varian Medical Systems"
        new_institution = "Mevaterapia Quilmes"
        new_modelname = "600CD"
        new_serialnumber = "523"
        new_treatment_machine_name = "QBA_600CD_523"

    elif equipo_destino == "Equipo 2 (EQ2_iX_827)":
        new_manufacturer = "Varian Medical Systems"
        new_institution = "Mevaterapia Quilmes"
        new_modelname = "iX-S"
        new_serialnumber = "827"
        new_treatment_machine_name = "EQ2_iX_827"

    if hasattr(dicom_info, 'BeamSequence'):
        for beam in dicom_info.BeamSequence:
            beam.Manufacturer = new_manufacturer
            beam.InstitutionName = new_institution
            beam.ManufacturerModelName = new_modelname
            beam.DeviceSerialNumber = new_serialnumber
            beam.TreatmentMachineName = new_treatment_machine_name


def change_machine(dicom_info, goal_machine):
    if goal_machine == "Equipo 1 (QBA_600CD_523)":
        # Cargo dicom base de 600CD
        path_eq1 = rf'\\10.130.1.253\FisicaQuilmes\_Datos\2_ Desarrollos\0_ En Curso\Modificador DCM\PlanBase_1_QA.dcm'
        info_eq1, sin_uso, sin_uso1, sin_uso2 = get_dicom_file(path_eq1)

        if hasattr(dicom_info, 'SOPClassUID'): info_eq1.SOPClassUID = dicom_info.SOPClassUID
        if hasattr(dicom_info, 'SOPInstanceUID'): info_eq1.SOPInstanceUID = dicom_info.SOPInstanceUID
        info_eq1.PatientName = 'Equipo1_QA'
        info_eq1.PatientID = '1-000000-1'
        if hasattr(dicom_info, 'StudyInstanceUID'): info_eq1.StudyInstanceUID = dicom_info.StudyInstanceUID
        if hasattr(dicom_info, 'SeriesInstanceUID'): info_eq1.SeriesInstanceUID = dicom_info.SeriesInstanceUID
        if hasattr(dicom_info, 'FrameOfReferenceUID'): info_eq1.FrameOfReferenceUID = dicom_info.FrameOfReferenceUID
        if hasattr(dicom_info, 'FractionGroupSequence'): info_eq1.FractionGroupSequence = dicom_info.FractionGroupSequence
        if hasattr(dicom_info, 'BeamSequence'): info_eq1.BeamSequence = dicom_info.BeamSequence
        if hasattr(dicom_info, 'ReferencedStructureSetSequence'): info_eq1.ReferencedStructureSetSequence = dicom_info.ReferencedStructureSetSequence

        update_beam_params(info_eq1,goal_machine)
        
        return info_eq1
    
    elif goal_machine == "Equipo 2 (EQ2_iX_827)":
        # Cargo dicom base de iX
        path_eq2 = rf'\\10.130.1.253\FisicaQuilmes\_Datos\2_ Desarrollos\0_ En Curso\Modificador DCM\PlanBase_2_QA.dcm'
        info_eq2, sin_uso, sin_uso1, sin_uso2 = get_dicom_file(path_eq2)

        if hasattr(dicom_info, 'SOPClassUID'): info_eq2.SOPClassUID = dicom_info.SOPClassUID
        if hasattr(dicom_info, 'SOPInstanceUID'): info_eq2.SOPInstanceUID = dicom_info.SOPInstanceUID
        info_eq2.PatientName = 'Equipo2_QA'
        info_eq2.PatientID = '1-000000-2'
        if hasattr(dicom_info, 'StudyInstanceUID'): info_eq2.StudyInstanceUID = dicom_info.StudyInstanceUID
        if hasattr(dicom_info, 'SeriesInstanceUID'): info_eq2.SeriesInstanceUID = dicom_info.SeriesInstanceUID
        if hasattr(dicom_info, 'FrameOfReferenceUID'): info_eq2.FrameOfReferenceUID = dicom_info.FrameOfReferenceUID
        if hasattr(dicom_info, 'FractionGroupSequence'): info_eq2.FractionGroupSequence = dicom_info.FractionGroupSequence
        if hasattr(dicom_info, 'BeamSequence'): info_eq2.BeamSequence = dicom_info.BeamSequence
        if hasattr(dicom_info, 'ReferencedStructureSetSequence'): info_eq2.ReferencedStructureSetSequence = dicom_info.ReferencedStructureSetSequence

        update_beam_params(info_eq2,goal_machine)
        
        return info_eq2
    
    else:
        return dicom_info



def add_private_fields(path_file_name):
    """
    Adds private fields to a DICOM file.

    Args:
        path_file_name (str): The path to the DICOM file.

    Returns:
        None

    This function reads an XML file located in the same directory as the script and adds its contents to the end of the DICOM file specified by `path_file_name`. The modified DICOM file is saved with the suffix "_mod.dcm" appended to the original file name. The function prints the path to the modified DICOM file after it is saved.

    The function first obtains the directory and file name of the DICOM file using `os.path.dirname` and `os.path.basename`. It then constructs the path to the XML file using `os.path.join` and `os.path.realpath` to ensure that the path is correct regardless of the current working directory.

    The function reads the contents of the XML file using a binary mode file object. It then reads the contents of the DICOM file using a binary mode file object.

    The function searches for the position of the string 'APPROVED' at the end of the DICOM file. It does this by iteratively checking the last 8 bytes of the file until it finds the string 'APPROVED'.
    """
    # Obtener el directorio y nombre del archivo DICOM
    dir_path = os.path.dirname(path_file_name)
    file_name = os.path.basename(path_file_name)
    
    # Ruta al archivo XML en el mismo directorio que el script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    xml_path = os.path.join(script_dir, 'anexo_XML.txt')

    # Leer el archivo XML
    with open(xml_path, 'rb') as xml_file:
        data_xml = xml_file.read()

    # Leer el archivo DICOM
    with open(path_file_name, 'rb') as dicom_file:
        data_dcm = dicom_file.read()

    # Buscar la posición de 'APPROVED' al final del archivo DICOM
    APPROVED = b'APPROVED'
    aux = len(data_dcm)
    i = 0
    while data_dcm[aux-8-i:aux-i] != APPROVED:
        i += 1

    # Reescribir el archivo DICOM agregando el anexo en XML
    data_dcm_mod = data_dcm[:aux-i]  # data2 cortado al final de 'APPROVED'
    output_path = os.path.join(dir_path, file_name[:-4] + '_private.dcm')
    with open(output_path, 'wb') as fid3:
        fid3.write(data_dcm_mod + data_xml)

    # Imprimir la ruta al archivo modificado
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Listo!", f"Archivo modificado guardado en: {output_path}")

def main():
    # Cargo el DICOM
    info, pixel_data, file_path, file_name, full_path_file = ui_get_dicom_file()
    if info is None:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Bueno, adiós!", "No se selecciono ningun archivo.")
        sys.exit()

    # Creo una copia para modificar
    info_mod = info

    # Cambio el equipo
    current_machine = info_mod.BeamSequence[0].TreatmentMachineName
    selected_machine = 'Null'
    root = tk.Tk()
    root.withdraw()
    change_machine_question = messagebox.askyesno("Equipo", "El equipo es '" + current_machine + "'. ¿Desea cambiarlo?")
    if change_machine_question: 
        selected_machine = ui_select_machine()
    root.destroy()
    info_mod = change_machine(info_mod, selected_machine)

    # Modificar Gantry Angle
    root = tk.Tk()
    root.withdraw()
    change_angle = messagebox.askyesno("Gantry", "¿Desea cambiar el ángulo de Gantry?")
    if change_angle: ui_modify_gantry_angles(info_mod)
    root.destroy()

    # Modificar Col Angle
    root = tk.Tk()
    root.withdraw()
    change_angle = messagebox.askyesno("Colimador", "¿Desea cambiar el ángulo de Colimador?")
    if change_angle: ui_modify_collimator_angles(info_mod)
    root.destroy()

    # Modifiar posicion del portal
    modificar_portal_possition(info_mod)

    # Cambiar tabla de tolerancia
    tolerance_table_dicom = info_mod.ToleranceTableSequence[0].ToleranceTableNumber
    tolerance_table_beam = info_mod.BeamSequence[0].ReferencedToleranceTableNumber
    tolerance_table_original = info_mod.ToleranceTableSequence[0].ToleranceTableLabel
    if tolerance_table_original != 'T_QA':
        root = tk.Tk()
        root.withdraw()
        message = f"La tabla de tolerancia es '{tolerance_table_original}'. ¿Desea cambiarla a 'T_QA'?"
        change_tol_table = messagebox.askyesno("Tabla de tolerancia", message)

        if change_tol_table: set_tolerances_to_qa(info_mod)
        root.destroy()

    if tolerance_table_dicom != tolerance_table_beam:
        set_tolerances_to_qa(info_mod)

    # Definir el nombre del archivo de salida
    out_path_name = file_path
    output_file_name = os.path.splitext(file_name)[0] + '_mod.dcm'
    output_path_file = os.path.join(out_path_name, output_file_name)

    # Guardar el archivo DICOM modificado
    pydicom.write_file(output_path_file, info_mod, write_like_original=True)
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Listo!", f"Archivo modificado guardado en: {out_path_name}")

    # Llamar a la función para modificar y guardar el archivo DICOM
    #add_private_fields(output_path_file)

if __name__ == '__main__':
    main()
