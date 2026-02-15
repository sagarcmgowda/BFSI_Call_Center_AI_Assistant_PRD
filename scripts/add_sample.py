import json
import os

DATASET_PATH = "app/data/alpaca_dataset.json"


def load_dataset():
    if not os.path.exists(DATASET_PATH):
        return []

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_dataset(data):
    with open(DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_sample(instruction, input_text, output):
    dataset = load_dataset()

    new_entry = {
        "instruction": instruction,
        "input": input_text,
        "output": output
    }

    dataset.append(new_entry)
    save_dataset(dataset)

    print("Sample added successfully!")
    print(f"Total samples: {len(dataset)}")


if __name__ == "__main__":
    print("\n--- Add New Alpaca Sample ---\n")

    instruction = input("Instruction: ")
    input_text = input("Input (leave blank if none): ")
    output = input("Output: ")

    add_sample(instruction, input_text, output)
