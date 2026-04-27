import os
import csv
import json


class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"Error: {self.filename} not found. Please download the file from LMS.")
            return False

    def create_output_folder(self, folder="output"):
        print("\nChecking output folder...")
        if os.path.exists(folder):
            print(f"Output folder already exists: {folder}/")
        else:
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("\nLoading data...")
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.students = list(reader)

            print(f"Data loaded successfully: {len(self.students)} students")
            return self.students

        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found. Please check the filename.")
            return []

        except Exception as e:
            print("Error while loading data:", e)
            return []

    def preview(self, n=5):
        print(f"\nFirst {n} rows:")
        print("------------------------------")

        for student in self.students[:n]:
            print(
                f"{student['student_id']} | "
                f"{student['age']} | "
                f"{student['gender']} | "
                f"{student['country']} | "
                f"GPA: {student['GPA']}"
            )

        print("------------------------------")


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        top_students = []

        try:
            sorted_students = sorted(
                self.students,
                key=lambda s: float(s["final_exam_score"]),
                reverse=True
            )

            top10 = sorted_students[:10]

            for i, student in enumerate(top10, start=1):
                top_students.append({
                    "rank": i,
                    "student_id": student["student_id"],
                    "country": student["country"],
                    "major": student["major"],
                    "final_exam_score": float(student["final_exam_score"]),
                    "GPA": float(student["GPA"])
                })

            self.result = {
                "analysis": "Top 10 Students by Exam Score",
                "total_students": len(self.students),
                "top_10": top_students
            }

            return self.result

        except ValueError:
            print("Warning: could not convert value to number.")
            return {}

        except Exception as e:
            print("Error during analysis:", e)
            return {}

    def lambda_map_filter_demo(self):
        print("\nLambda / Map / Filter")
        print("------------------------------")

        try:
            top_scorers = list(
                filter(lambda s: float(s["final_exam_score"]) > 95, self.students)
            )

            gpa_values = list(
                map(lambda s: float(s["GPA"]), self.students)
            )

            good_assignment = list(
                filter(lambda s: float(s["assignment_score"]) > 90, self.students)
            )

            print(f"Students with score > 95 : {len(top_scorers)}")
            print(f"GPA values (first 5) : {gpa_values[:5]}")
            print(f"Students assignment > 90 : {len(good_assignment)}")

        except ValueError:
            print("Warning: could not convert value — skipping row.")

        except Exception as e:
            print("Error in lambda/map/filter part:", e)

    def print_results(self):
        print("\n------------------------------")
        print("Top 10 Students by Exam Score")
        print("------------------------------")

        for student in self.result.get("top_10", []):
            print(
                f"{student['rank']}. "
                f"{student['student_id']} | "
                f"{student['country']} | "
                f"{student['major']} | "
                f"Score: {student['final_exam_score']} | "
                f"GPA: {student['GPA']}"
            )

        print("------------------------------")


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, "w", encoding="utf-8") as file:
                json.dump(self.result, file, indent=4)

            print(f"\nResult saved to {self.output_path}")

        except Exception as e:
            print("Error while saving JSON:", e)


def main():
    fm = FileManager("students.csv")

    if not fm.check_file():
        print("Stopping program.")
        return

    fm.create_output_folder()

    dl = DataLoader("students.csv")
    students = dl.load()

    if not students:
        print("Stopping program.")
        return

    dl.preview()

    analyser = DataAnalyser(students)
    analyser.analyse()
    analyser.print_results()
    analyser.lambda_map_filter_demo()

    saver = ResultSaver(analyser.result, "output/result.json")
    saver.save_json()


main()