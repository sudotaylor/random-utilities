#!/usr/bin/env python3

## csvProcessingNames.py
## Simple script to clear special characters from names and improve classification of name data.

## Note that the escapeList letters are not actually equivalent!
## However, in some situations these characters are not allowed,
## so they are set to the closest characters from the usable character set.

import csv
import re

escapeList: dict[str, str] = {
    'á': 'a',
    'Á': 'A',
    'à': 'a',
    'À': 'A',
    'â': 'a',
    'Â': 'A',
    'ä': 'a',
    'Ä': 'A',
    'ã': 'a',
    'Ã': 'A',
    'å': 'a',
    'Å': 'A',
    'æ': 'ae',
    'Æ': 'AE',
    'ç': 'c',
    'Ç': 'C',
    'é': 'e',
    'É': 'E',
    'è': 'e',
    'È': 'E',
    'ê': 'e',
    'Ê': 'E',
    'ë': 'e',
    'Ë': 'E',
    'í': 'i',
    'Í': 'I',
    'ì': 'i',
    'Ì': 'I',
    'î': 'i',
    'Î': 'I',
    'ï': 'i',
    'Ï': 'I',
    'ñ': 'n',
    'Ñ': 'N',
    'ó': 'o',
    'Ó': 'O',
    'ò': 'o',
    'Ò': 'O',
    'ô': 'o',
    'Ô': 'O',
    'ö': 'o',
    'Ö': 'O',
    'õ': 'o',
    'Õ': 'O',
    'ø': 'o',
    'Ø': 'O',
    'œ': 'oe',
    'Œ': 'OE',
    'ß': 'B',
    'ú': 'u',
    'Ú': 'U',
    'ù': 'u',
    'Ù': 'U',
    'û': 'u',
    'Û': 'U',
    'ü': 'u',
    'Ü': 'U'
}

def fixCharacters(row: list[str], colNumbers: list[int]) -> list[str]:
    for char, escape in escapeList.items():
        for colNum in colNumbers:
            row[colNum] = row[colNum].replace(char, escape)
    return row

def fullFixNames(row: list[str]) -> list[str]:
    ## Escape special characters first
    row: list[str] = fixCharacters(row)
    ## Check lastname + suffix
    if re.search('.\s+JR\.?$', row[2].upper()) is not None: ## could add option to catch those with a comma before each of these
        last: str = ' '.join(row[2].split()[:-1])
        suffix: str = "JR"
    elif re.search('.\s+SR\.?$', row[2].upper()) is not None:
        last: str = ' '.join(row[2].split()[:-1])
        suffix: str = "SR"
    elif re.search('.\s+II\.?$', row[2].upper()) is not None:
        last: str = ' '.join(row[2].split()[:-1])
        suffix: str = "II"
    elif re.search('.\s+III\.?$', row[2].upper()) is not None:
        last: str = ' '.join(row[2].split()[:-1])
        suffix: str = "III"
    elif re.search('.\s+IV\.?$', row[2].upper()) is not None:
        last: str = ' '.join(row[2].split()[:-1])
        suffix: str = "IV"
    ## Need others? Insert them here.
    else:
        last: str = row[2]
        suffix: str = ""
    ## Check firstname + middlename
    if re.search('.+\s+de\s+.+', row[3].upper()) is not None:
        first: str = ' '.join(row[3].split(' de ')[0].split()) # note that all of these are removeing potential extra spaces
        middle: str = ' '.join(row[3].split(' de ')[1].split())
    if re.search('.+\s*-\s*.+', row[3].upper()) is not None:
        first: str = ' '.join(row[3].split('-')[0].split()) # note that all of these are removeing potential extra spaces
        middle: str = ' '.join(row[3].split('-')[1].split())
    if re.search('.+\s+.+', row[3].upper()) is not None:
        first: str = ' '.join(row[3].split()[0].split()) # note that all of these are removeing potential extra spaces
        middle: str = ' '.join(row[3].split()[1].split())
    else:
        first: str = row[3]
        middle:str = ""
    return row[:2] + [last, first, middle, suffix] + row[4:]


def csvFixCharsCopy(inputCsv: str, outputCsv: str, delim: str = ',') -> None:
    if (inputCsv == outputCsv):
        print("Can not use same filename in csvFixCopy() - to overwrite original file, use csvFixOverwrite() instead")
        return
    with open(outputCsv, mode='w', encoding='UTF-8') as outFile:
        writer: csv._writer = csv.writer(outFile, delimiter=delim, lineterminator='\n')
        with open(inputCsv, mode='r', encoding='UTF-8') as f:
            for row in csv.reader(f, delimiter=delim):
                writer.writerow(delim.join(fixCharacters(row)))
        

def csvFixCharsOverwrite(csvFile: str, delim: str = ',') -> None:
    with open(csvFile, mode='r', encoding='UTF-8') as f:
        outputMem: list[str] = []
        for row in csv.reader(f, delimiter=delim):
            outputMem.append(delim.join(fixCharacters(row)))
    with open(csvFile, mode='w', encoding='UTF-8') as f:
        writer: csv._writer = csv.writer(f, delimiter=delim, lineterminator='\n')
        for row in outputMem:
            writer.writerow(row)

def csvFixFileCopy(inputCsv: str, outputCsv: str, delim: str = ',') -> None:
    with open(outputCsv, mode='w', encoding='UTF-8') as outputFile:
        writer: csv._writer = csv.writer(outputFile, delimiter=delim, lineterminator='\n')
        with open(inputCsv, mode='r', encoding='UTF-8') as f:
            headerList: list[str] = f.readline().split(delim)
            ## note hardcoded column positions, as in fullFixNames() -- can alter later if desired
            headerList = headerList[:2] + ["Last.Name", "First.Name", "Middle", "Suffix"] + headerList[4:]
            writer.writerow(delim.join(headerList))
            for row in csv.reader(f, delimiter=delim):
                writer.writerow(delim.join(fullFixNames(row))) ## could change quoting in csv.writer if desired

def csvFixFileOverwrite(csvFile: str, delim: str = ',') -> None:
    with open(csvFile, mode='r', encoding='UTF-8') as f:
        headerList: list[str] = f.readline().split(delim)
        ## note hardcoded column positions, as in fullFixNames() -- can alter later if desired
        headerList = headerList[:2] + ["Last.Name", "First.Name", "Middle", "Suffix"] + headerList[4:]
        outputMem: list[str] = []
        for row in csv.reader(f, delimiter=delim):
            outputMem.append(delim.join(fullFixNames(row)))
    with open(csvFile, mode='w', encoding='UTF-8') as f:
        writer: csv._writer = csv.writer(f, delimiter=delim, lineterminator='\n')
        writer.writerow(delim.join(headerList))
        for row in outputMem:
            writer.writerow(row)


########################
## Example usage:
def examples() -> None:
    csvFixCharsCopy('input.csv', 'output.csv')
    csvFixCharsCopy('input.csv', 'output.csv', '\t')
    csvFixCharsOverwrite('update_this.csv')
    csvFixCharsOverwrite('update_this.csv', '|')
    csvFixFileCopy('input.csv', 'output.csv')
    csvFixFileCopy('input.csv', 'output.csv', '\t')
    csvFixFileOverwrite('update_this.csv')
    csvFixFileOverwrite('update_this.csv', '|')
#examples()
########################



0
