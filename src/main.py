import pandas as pd
from collections import defaultdict


class DrugInformationSystem:
    def __init__(self, excel_file='drugs_data_with_latin.xlsx'):
        self.excel_file = excel_file
        self.drugs_df = self._load_data()
        self.classification_map = self._create_classification_map()

    def _load_data(self):
        """Load drug data from Excel file"""
        try:
            df = pd.read_excel(self.excel_file)
            # Convert to dictionary with drug names as keys (case-insensitive)
            return df.set_index(df['Name'].str.lower()).to_dict('index')
        except FileNotFoundError:
            raise FileNotFoundError(f"Excel file {self.excel_file} not found")
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")

    def _create_classification_map(self):
        """Create a mapping of classifications to drugs"""
        classification_map = defaultdict(list)
        for drug_name, drug_info in self.drugs_df.items():
            classification = drug_info['Classification'].split('(')[0].strip()  # Get main classification
            classification_map[classification].append(drug_name.title())  # Store with proper capitalization
        return dict(classification_map)

    def search_drug(self, drug_name):
        """Search for drug by name (case-insensitive)"""
        drug_name = drug_name.lower()
        return self.drugs_df.get(drug_name)

    def display_drug_info(self, drug_name):
        """Display formatted drug information for a single drug"""
        drug_info = self.search_drug(drug_name)

        if drug_info:
            print(f"\n=== {drug_name.upper()} ===")
            for key, value in drug_info.items():
                if key != 'Name' and pd.notna(value):
                    print(f"{key.capitalize()}: {value}")
        else:
            print(f"Препарат '{drug_name}' не найден в базе данных.")

    def classify_drugs_interactive(self):
        """
        Interactive mode for classifying multiple drugs
        Collects drugs one by one until 'finish' is entered
        """
        drug_list = []
        print("\nВводите названия препаратов по одному (для завершения введите 'finish'):")

        while True:
            drug_input = input("Название препарата: ").strip()

            if drug_input.lower() == 'finish':
                if not drug_list:
                    print("Не введено ни одного препарата!")
                    return
                break

            if drug_input:  # Only add non-empty inputs
                drug_list.append(drug_input)

        # Classify the collected drugs
        self._classify_and_display(drug_list)

    def _classify_and_display(self, drug_names):
        """
        Internal method to classify drugs and display results
        Args:
            drug_names: list of drug names to classify
        """
        classified = defaultdict(list)
        not_found = []

        for name in drug_names:
            drug_info = self.search_drug(name)
            if drug_info:
                classification = drug_info['Classification'].split('(')[0].strip()
                classified[classification].append(name.title())
            else:
                not_found.append(name)

        # Display results
        print("\n=== Классификация препаратов ===")
        for classification, drugs in classified.items():
            print(f"\n{classification}:")
            print(", ".join(sorted(drugs)))

        if not_found:
            print(f"\nПрепараты не найдены: {', '.join(not_found)}")

    def run(self):
        """Main interactive interface"""
        while True:
            print("\nВыберите действие:")
            print("1. Поиск информации по одному препарату")
            print("2. Классификация нескольких препаратов")
            print("3. (Функция в разработке)")
            print("0. Выход")

            choice = input("Ваш выбор (0-3): ").strip()

            if choice == '0':
                print("Выход из программы.")
                break

            elif choice == '1':
                drug_name = input("Введите название препарата: ").strip()
                self.display_drug_info(drug_name)

            elif choice == '2':
                self.classify_drugs_interactive()

            elif choice == '3':
                print("\nЭта функция находится в разработке.")
                # Placeholder for future functionality

            else:
                print("Некорректный выбор. Пожалуйста, введите число от 0 до 3.")


# Example usage
if __name__ == "__main__":
    try:
        system = DrugInformationSystem()
        system.run()
    except Exception as e:
        print(f"Ошибка: {str(e)}")
