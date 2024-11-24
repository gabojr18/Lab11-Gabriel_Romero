import os
import matplotlib.pyplot as plt

# Update the file paths to the new location
STUDENTS_FILE = r"C:\Users\gabojr\OneDrive\UF 2024\Fall Semester 2024\Cop3502c\Lab 11\Data\students.txt"
ASSIGNMENTS_FILE = r"C:\Users\gabojr\OneDrive\UF 2024\Fall Semester 2024\Cop3502c\Lab 11\Data\assignments.txt"
SUBMISSIONS_FOLDER = r"C:\Users\gabojr\OneDrive\UF 2024\Fall Semester 2024\Cop3502c\Lab 11\Data\submissions"

def load_students():
    students = {}
    try:
        with open(STUDENTS_FILE, 'r') as file:
            for line in file:
                try:
                    student_id, name = line[:3], line[3:].strip()
                    students[student_id] = name
                except ValueError:
                    print(f"Skipping invalid line in {STUDENTS_FILE}: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: {STUDENTS_FILE} not found.")
    return students

def load_assignments():
    assignments = {}
    try:
        with open(ASSIGNMENTS_FILE, 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 3):
                try:
                    name = lines[i].strip()
                    id = lines[i + 1].strip()
                    max_score = int(lines[i + 2].strip())
                    assignments[id] = {"name": name, "max_score": max_score}
                except (IndexError, ValueError):
                    print(f"Skipping invalid lines in {ASSIGNMENTS_FILE} starting at line {i + 1}")
    except FileNotFoundError:
        print(f"Error: {ASSIGNMENTS_FILE} not found.")
    return assignments

def load_submissions():
    submissions = {}
    if not os.path.isdir(SUBMISSIONS_FOLDER):
        print(f"Error: {SUBMISSIONS_FOLDER} not found.")
        return submissions

    for filename in os.listdir(SUBMISSIONS_FOLDER):
        file_path = os.path.join(SUBMISSIONS_FOLDER, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        try:
                            student_id, assignment_id, score = line.strip().split('|')
                            score = int(score)
                            if assignment_id not in submissions:
                                submissions[assignment_id] = {}
                            submissions[assignment_id][student_id] = score
                        except ValueError:
                            print(f"Skipping invalid line in {filename}: {line.strip()}")
            except FileNotFoundError:
                print(f"Error: {filename} not found in {SUBMISSIONS_FOLDER}.")
    return submissions

def student_grade(name, students, assignments, submissions):
    student_id = None
    for id, student_name in students.items():
        if student_name.lower() == name.lower():
            student_id = id
            break

    if not student_id:
        print(f"Student {name} not found.")
        return

    print(f"Grades for {name}:")
    total_score = 0
    total_max_score = 0
    for assignment_id, scores in submissions.items():
        if student_id in scores:
            score = scores[student_id]
            max_score = assignments[assignment_id]["max_score"]
            print(f"{assignments[assignment_id]['name']}: {score}/{max_score}")
            total_score += score
            total_max_score += max_score

    if total_max_score > 0:
        print(f"Total Grade: {total_score}/{total_max_score} ({(total_score / total_max_score) * 100:.2f}%)")
    else:
        print("No grades available for this student.")

def assignment_statistics(name, assignments, submissions):
    assignment_id = None
    for id, info in assignments.items():
        if info["name"].lower() == name.lower():
            assignment_id = id
            break

    if not assignment_id:
        print(f"Assignment {name} not found.")
        return

    if assignment_id not in submissions:
        print(f"No submissions found for {name}.")
        return

    scores = submissions[assignment_id].values()
    print(f"Statistics for {name}:")
    print(f"Average: {sum(scores) / len(scores):.2f}")
    print(f"Min: {min(scores)}")
    print(f"Max: {max(scores)}")

def assignment_graph(name, assignments, submissions):
    assignment_id = None
    for id, info in assignments.items():
        if info["name"].lower() == name.lower():
            assignment_id = id
            break

    if not assignment_id:
        print(f"Assignment {name} not found.")
        return

    if assignment_id not in submissions:
        print(f"No submissions found for {name}.")
        return

    scores = list(submissions[assignment_id].values())
    bins = [i for i in range(50, 101, 5)]  # Bins start at 50 and end at 100
    plt.hist(scores, bins=bins, edgecolor='black')
    plt.title(f"Scores for {name}")
    plt.xlabel("Score Ranges")
    plt.ylabel("Number of Students")
    plt.xlim(50, 100)  # Limit x-axis to 50–100
    plt.show()


def main():
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()

    if not students or not assignments or not submissions:
        print("Data could not be loaded. Exiting program.")
        return

    while True:
        print("\n1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")
        choice = input("Enter your selection: ")

        if choice == "1":
            name = input("What is the student name? ")
            student_grade(name, students, assignments, submissions)
        elif choice == "2":
            name = input("What is the assignment name? ")
            assignment_statistics(name, assignments, submissions)
        elif choice == "3":
            name = input("What is the assignment name? ")
            assignment_graph(name, assignments, submissions)
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
