import os
import matplotlib.pyplot as plt

STUDENTS_FILE = r"C:\Users\gabojr\PycharmProjects\Lab11\Data\students.txt"
ASSIGNMENTS_FILE = r"C:\Users\gabojr\PycharmProjects\Lab11\Data\assignments.txt"
SUBMISSIONS_FOLDER = r"C:\Users\gabojr\PycharmProjects\Lab11\Data\submissions"

def load_students():
    students = {}
    with open(STUDENTS_FILE, 'r') as file:
        for line in file:
            student_id, name = line[:3], line[3:].strip()
            students[student_id] = name
    return students

def load_assignments():
    assignments = {}
    with open(ASSIGNMENTS_FILE, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            id = lines[i + 1].strip()
            max_score = int(lines[i + 2].strip())
            assignments[id] = {"name": name, "max_score": max_score}
    return assignments

def load_submissions():
    submissions = {}
    for filename in os.listdir(SUBMISSIONS_FOLDER):
        file_path = os.path.join(SUBMISSIONS_FOLDER, filename)
        with open(file_path, 'r') as file:
            for line in file:
                student_id, assignment_id, percentage = line.strip().split('|')
                if assignment_id not in submissions:
                    submissions[assignment_id] = {}
                submissions[assignment_id][student_id] = float(percentage)
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
    total_score = 0
    for assignment_id, scores in submissions.items():
        if student_id in scores:
            percentage = scores[student_id]
            max_score = assignments[assignment_id]["max_score"]
            earned_score = (percentage / 100) * max_score
            total_score += earned_score
    total_percentage = (total_score / 1000) * 100
    print(f"{round(total_percentage)}%")

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
    avg_score = round(sum(scores) / len(scores))
    min_score = round(min(scores))
    max_score = round(max(scores))
    print(f"Min: {min_score}%")
    print(f"Avg: {avg_score}%")
    print(f"Max: {max_score}%")

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
    bins = [i for i in range(50, 101, 5)]
    plt.hist(scores, bins=bins, edgecolor='black')
    plt.title(f"Scores for {name}")
    plt.xlabel("Score Ranges")
    plt.ylabel("Number of Students")
    plt.xlim(50, 100)
    plt.show()

def main():
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()
    while True:
        print("\n1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")
        choice = input("Enter your selection: ")
        if choice == "1":
            name = input("What is the student's name: ")
            student_grade(name, students, assignments, submissions)
        elif choice == "2":
            name = input("What is the assignment name: ")
            assignment_statistics(name, assignments, submissions)
        elif choice == "3":
            name = input("What is the assignment name: ")
            assignment_graph(name, assignments, submissions)
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
