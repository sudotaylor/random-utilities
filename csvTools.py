#!/usr/bin/env python
# CSV Tools
# Tools used to process .csv files (a work in progress)

from os.path import isfile
from shutil import copy

def csv_combine(csv_list: list[str], output_file: str, overwrite: bool) -> str | None:
    if len(csv_list) < 1:
        print("Could not combine csv files: file list is empty.\n")
        return
    elif isfile(output_file):
        if not overwrite:
            print("File '" + output_file + "' already exists and overwriting is not permitted.\n")
            return
        else:
            try:
                copy(csv_list[0], output_file)
                output_writer = open(output_file, 'a')
            except:
                print("Could not overwrite existing file '" + output_file + "' for output.\n")
                return
        if len(csv_list) == 1:
            print("Only one csv file (" + csv_list[0] + ") found in list. Output is a copy of that file.\n")
            output_writer.close()
            return output_file
    else:
        try:
            copy(csv_list[0], output_file)
            output_writer = open(output_file, 'a')
        except:
            print("Could not open new file '" + output_file + "' for output.\n")
    first_reader = open(csv_list.pop(0))
    header: str = first_reader.readline().strip()
    first_reader.close
    while len(csv_list)>0:
        current_csv: str = csv_list.pop(0)
        if isfile(current_csv):
            try:
                with open(current_csv, 'r') as file_reader:
                    current_header: str = file_reader.readline().strip()
                    if header == current_header:
                        content: list[str] = file_reader.readlines()
                        output_writer.writelines(content)
                    else:
                        print("Header mismatch in file '" + current_csv + "'.\nFile header: [" + current_header + "].\nOriginal header: [" + header + "]\n")
            except:
                print("Could not append file '" + current_csv + "' contents to '" + output_file + "'.\n") 
                # Could break out here (e.g. "return"), if desired. Otherwise it will still continue to try adding other files
