# Recipe Assistant

This project is a simple desktop application that detects allergens from a list of ingredients and provides substitute recommendations. It uses a pre-trained FastText model for allergen detection and a substitution dataset for suggestions.

## Folder Structure

```
project/
│
├── datasets/
│   └── substitution_map.csv      # Substitution map for allergens
│
├── model/
│   └── allergen_detection_model.bin  # Pre-trained FastText model
│
├── src/
│   └── allergen_checker.py       # Main Python script for the application
```

## Requirements

Ensure you have the following installed:

- Python 3.8 or later
- Required Python libraries:
  - tkinter (built-in with Python)
  - pandas
  - fasttext

## Installation

**Install dependencies**:

```bash
pip install pandas fasttext
```

## How to Run

1. Navigate to the `src` folder:

   ```bash
   cd src
   ```

2. Run the application:
   ```bash
   python allergen_checker.py
   ```

## Usage

1. Enter a list of ingredients (comma-separated) in the input field.
2. Click the "Check Allergens" button.
3. View detected allergens and substitute recommendations in a new window.

## Example

### Input:

```
milk, peanuts, shellfish
```

### Output:

- **Detected Allergens**: `milk, peanuts, shellfish`
- **Suggested Substitutes**:
  ```
  milk -> almond milk
  peanuts -> sunflower seed butter
  shellfish -> king oyster mushrooms
  ```

## Dataset Format

The substitution dataset (`substitution_map.csv`) should have the following format:

| Allergen  | Substitute Food Item  |
| --------- | --------------------- |
| milk      | almond milk           |
| peanuts   | sunflower seed butter |
| tree nuts | pumpkin seeds         |
| shellfish | king oyster mushrooms |

## Troubleshooting

1. **"No allergens detected" for all inputs**:

   - Ensure the substitution dataset is correctly formatted and located in the `datasets` folder.
   - Verify that the pre-trained model is in the `model` folder.

2. **Tkinter not found**:
   - Ensure Python is correctly installed. Tkinter is included in most Python distributions.

## License

This project is licensed under the MIT License.

## Acknowledgements

- FastText for text classification
- Tkinter for GUI development
