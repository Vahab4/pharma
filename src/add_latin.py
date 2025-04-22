import pandas as pd

# Dictionary of Russian to Latin drug names
latin_names = {
    'преноксдиазин': 'Prenoxdiazine',
    'бутамират': 'Butamirate',
    'бромгексин': 'Bromhexine',
    'ацетилцистеин': 'Acetylcysteine',
    'будесонид': 'Budesonide',
    'кромолин-натрий': 'Cromoglicic acid',
    'сальбутамол': 'Salbutamol',
    'фенотерол': 'Fenoterol',
    'аминофиллин': 'Aminophylline',
    'тиотропий': 'Tiotropium',
    'теофиллин': 'Theophylline',
    'сибутрамин': 'Sibutramine',
    'метоклопрамид': 'Metoclopramide',
    'омепразол': 'Omeprazole',
    'фамотидин': 'Famotidine',
    'пирензепин': 'Pirenzepine',
    'дротаверина гидрохлорид': 'Drotaverine',
    'окситоцин': 'Oxytocin',
    'цианокобаламин': 'Cyanocobalamin',
    'молграмостим': 'Molgramostim',
    'кислота ацетилсалициловая': 'Acetylsalicylic acid',
    'клопидогрел': 'Clopidogrel',
    'гепарин': 'Heparin',
    'варфарин': 'Warfarin',
    'циклоспорин': 'Cyclosporine',
    'преднизолон': 'Prednisolone',
    'ибупрофен': 'Ibuprofen',
    'диклофенак-натрий': 'Diclofenac',
    'целекоксиб': 'Celecoxib',
    'дифенгидрамин': 'Diphenhydramine',
    'лоратадин': 'Loratadine',
    'адреналин': 'Epinephrine',
    'l-тироксин': 'Levothyroxine',
    'тиамазол': 'Thiamazole',
    'глимепирид': 'Glimepiride',
    'метформин': 'Metformin',
    'ситаглиптин': 'Sitagliptin'
}


def add_latin_column(input_file, output_file=None):
    """
    Add Latin names column to an existing Excel file

    Args:
        input_file: Path to the input Excel file
        output_file: Path to save the modified file (if None, overwrites input file)
    """
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Add Latin column by mapping the Russian names
    df['Latin'] = df['Name'].str.lower().map(latin_names)

    # Reorder columns to make Latin appear right after Name
    cols = df.columns.tolist()
    name_index = cols.index('Name')
    cols.insert(name_index + 1, cols.pop(cols.index('Latin')))
    df = df[cols]

    # Save the modified file
    if output_file is None:
        output_file = input_file
    df.to_excel(output_file, index=False)
    print(f"Successfully added Latin names to {output_file}")


# Example usage - modify these paths as needed
input_excel = "drugs_data.xlsx"  # Your existing file
output_excel = "drugs_data_with_latin.xlsx"  # New file (or same as input to overwrite)

add_latin_column(input_excel, output_excel)