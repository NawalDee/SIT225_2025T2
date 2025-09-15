import glob
import csv
import os

def generate_annotations():
    # Only match files
    files = sorted(glob.glob("[0-9]_*.csv"))

    annotations = []
    for file in files:
        print(f"File: {file}")
        label = input("Enter label (0, 1, 2): ")
        while label not in ["0", "1", "2"]:
            print("Invalid input. Please enter 0, 1, or 2.")
            label = input("Enter label (0, 1, 2): ")
        annotations.append([os.path.splitext(file)[0], label])

    # Save annotations
    with open("annotations.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "label"])
        writer.writerows(annotations)

    print("\nSaved annotations.csv")

if __name__ == "__main__":
    generate_annotations()
