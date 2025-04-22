from flask import Flask, request, render_template
import pandas as pd
from collections import defaultdict
import os

# Initialize Flask with explicit template folder
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

class DrugInformationSystem:
    def __init__(self, excel_file='drugs_data_with_latin.xlsx'):
        self.excel_file = excel_file
        self.drugs_df = self._load_data()
        self.classification_map = self._create_classification_map()

    def _load_data(self):
        """Load drug data from Excel file"""
        try:
            # Get the absolute path to the Excel file
            excel_path = os.path.join(os.path.dirname(__file__), self.excel_file)
            df = pd.read_excel(excel_path)
            return df.set_index(df['Name'].str.lower()).to_dict('index')
        except FileNotFoundError:
            raise FileNotFoundError(f"Excel file {self.excel_file} not found")
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")

    def _create_classification_map(self):
        """Create a mapping of classifications to drugs"""
        classification_map = defaultdict(list)
        for drug_name, drug_info in self.drugs_df.items():
            classification = drug_info['Classification'].split('(')[0].strip()
            classification_map[classification].append(drug_name.title())
        return dict(classification_map)

    def search_drug(self, drug_name):
        """Search for drug by name (case-insensitive)"""
        drug_name = drug_name.lower()
        return self.drugs_df.get(drug_name)

# Debugging paths
print(f"Current directory: {os.getcwd()}")
print(f"Template folder exists: {os.path.exists('templates')}")
print(f"Prescription form exists: {os.path.exists('templates/prescription_form.html')}")

# Initialize the system when the app starts
drug_system = DrugInformationSystem()

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'search':
                drug_name = request.form.get('drug_name', '').strip()
                if drug_name:
                    drug_info = drug_system.search_drug(drug_name)
                    return render_template('result.html', 
                                        drug_name=drug_name.title(), 
                                        drug_info=drug_info)
            
            elif action == 'classify':
                drug_list = [name.strip() for name in request.form.get('drug_list', '').split(',') if name.strip()]
                classified = defaultdict(list)
                not_found = []
                
                for name in drug_list:
                    drug_info = drug_system.search_drug(name)
                    if drug_info:
                        classification = drug_info['Classification'].split('(')[0].strip()
                        classified[classification].append(name.title())
                    else:
                        not_found.append(name)
                
                return render_template('classification.html', 
                                    classified=classified, 
                                    not_found=not_found)
        
        return render_template('index.html')
    
    except Exception as e:
        print(f"Error in home route: {str(e)}")
        return render_template('error.html', error_message=str(e)), 500

@app.route('/prescription', methods=['GET', 'POST'])
def prescription():
    try:
        if request.method == 'POST':
            # Collect all prescription data
            prescription_data = {
                'doctor_name': request.form.get('doctor_name', '').strip(),
                'patient_name': request.form.get('patient_name', '').strip(),
                'patient_age': request.form.get('patient_age', '').strip(),
                'date': request.form.get('date', '').strip(),
                'drug_name': request.form.get('drug_name', '').strip(),
                'dosage_form': request.form.get('dosage_form', '').strip(),
                'strength': request.form.get('strength', '').strip(),
                'quantity': request.form.get('quantity', '').strip(),
                'instructions_pharmacist': request.form.get('instructions_pharmacist', '').strip(),
                'instructions_patient': request.form.get('instructions_patient', '').strip()
            }
            
            # Generate prescription text
            prescription_text = f"""
            Рецепт
            Врач: {prescription_data['doctor_name']}
            Пациент: {prescription_data['patient_name']}, {prescription_data['patient_age']} лет
            Дата: {prescription_data['date']}

            Rp.: {prescription_data['dosage_form']} {prescription_data['drug_name']} {prescription_data['strength']}
            {prescription_data['instructions_pharmacist']}
            S. {prescription_data['instructions_patient']}

            Подпись и печать врача: __________
            """
            
            return render_template('prescription_result.html', 
                                prescription_text=prescription_text,
                                data=prescription_data)
        
        return render_template('prescription_form.html')
    
    except Exception as e:
        print(f"Error in prescription route: {str(e)}")
        return render_template('error.html', error_message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
