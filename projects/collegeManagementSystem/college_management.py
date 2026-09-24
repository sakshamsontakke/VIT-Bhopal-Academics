#!/usr/bin/env python3
"""
==================================================================
        VIT-STYLE COLLEGE MANAGEMENT SYSTEM
==================================================================
A single-file, console-based College Management System written in
pure Python (standard library only), inspired by the general
academic concepts used at large Indian private engineering
universities (FFCS, CAT-1/CAT-2/FAT, CGPA, etc.).

This is an ORIGINAL educational project. It is NOT affiliated with,
endorsed by, or a copy of any real university's software, and it
does not use any confidential or internal data.

Run with:
    python college_management.py

NOTE ON SECURITY: For simplicity, this educational project stores
passwords as plain text inside JSON files. A production system
MUST hash and salt passwords (e.g. using hashlib.pbkdf2_hmac or a
library like bcrypt) and should never store credentials in plain
text.
==================================================================
"""

import json
import os
import random
import statistics
import textwrap
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# ==================================================================
# GLOBAL CONFIGURATION
# ==================================================================

DATA_DIR = "cms_data"

FILES = {
    "students": "students.json",
    "faculty": "faculty.json",
    "users": "users.json",
    "courses": "courses.json",
    "enrollments": "enrollments.json",
    "attendance": "attendance.json",
    "marks": "marks.json",
    "exams": "exams.json",
    "fees": "fees.json",
    "hostel": "hostel.json",
    "transport": "transport.json",
    "books": "books.json",
    "library_transactions": "library_transactions.json",
    "leaves": "leaves.json",
    "clubs": "clubs.json",
    "placements": "placements.json",
    "notices": "notices.json",
    "settings": "settings.json",
}

DEFAULT_SETTINGS = {
    "required_attendance_percentage": 75.0,
    "ffcs_registration_open": True,
    "current_semester": 5,
    "current_academic_year": "2025-2026",
}

GRADE_SCALE = [
    (90, 100, "S", 10),
    (80, 89, "A", 9),
    (70, 79, "B", 8),
    (60, 69, "C", 7),
    (50, 59, "D", 6),
    (40, 49, "E", 5),
    (0, 39, "F", 0),
]


def line(char="=", length=60):
    return char * length


def header(title):
    print("\n" + line())
    print(title.center(60))
    print(line())


def sub_header(title):
    print("\n" + line("-", 60))
    print(title)
    print(line("-", 60))


def pause():
    input("\nPress Enter to continue...")


def safe_int_input(prompt, minimum=None, maximum=None):
    """Read an integer from the console with validation."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if minimum is not None and value < minimum:
                print(f"Value must be >= {minimum}.")
                continue
            if maximum is not None and value > maximum:
                print(f"Value must be <= {maximum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number.")


def safe_float_input(prompt, minimum=None, maximum=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if minimum is not None and value < minimum:
                print(f"Value must be >= {minimum}.")
                continue
            if maximum is not None and value > maximum:
                print(f"Value must be <= {maximum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def non_empty_input(prompt):
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("This field cannot be empty.")


def generate_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


# ==================================================================
# FILE MANAGER  (single place for all JSON persistence)
# ==================================================================

class FileManager:
    """Centralised JSON file handling so no other class touches
    open()/json.load()/json.dump() directly. This avoids duplicating
    file-handling logic across the many manager classes."""

    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _path(self, filename):
        return os.path.join(self.data_dir, filename)

    def load_data(self, filename, default=None):
        path = self._path(filename)
        if not os.path.exists(path):
            default = default if default is not None else []
            self.save_data(filename, default)
            return default
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    default = default if default is not None else []
                    self.save_data(filename, default)
                    return default
                return json.loads(content)
        except (json.JSONDecodeError, OSError):
            print(f"[WARNING] Could not read {filename}. Reinitialising it.")
            default = default if default is not None else []
            self.save_data(filename, default)
            return default

    def save_data(self, filename, data):
        path = self._path(filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except OSError as exc:
            print(f"[ERROR] Could not save {filename}: {exc}")
            return False

    def add_record(self, filename, record):
        data = self.load_data(filename)
        data.append(record)
        self.save_data(filename, data)
        return record

    def update_record(self, filename, key, value, updates):
        data = self.load_data(filename)
        updated = False
        for record in data:
            if record.get(key) == value:
                record.update(updates)
                updated = True
        if updated:
            self.save_data(filename, data)
        return updated

    def delete_record(self, filename, key, value):
        data = self.load_data(filename)
        new_data = [r for r in data if r.get(key) != value]
        deleted = len(new_data) != len(data)
        if deleted:
            self.save_data(filename, new_data)
        return deleted

    def find_one(self, filename, key, value):
        data = self.load_data(filename)
        for record in data:
            if record.get(key) == value:
                return record
        return None

    def find_all(self, filename, key, value):
        data = self.load_data(filename)
        return [r for r in data if r.get(key) == value]

    def reset_all(self):
        """Delete every managed JSON file (used by 'reset demo data')."""
        for filename in FILES.values():
            path = self._path(filename)
            if os.path.exists(path):
                os.remove(path)


# ==================================================================
# GRADE CALCULATOR
# ==================================================================

class GradeCalculator:
    """Configurable grade calculation, GPA and CGPA logic."""

    def __init__(self, scale=None):
        self.scale = scale if scale else GRADE_SCALE

    def marks_to_grade(self, total_marks):
        for low, high, letter, points in self.scale:
            if low <= total_marks <= high:
                return letter, points
        return "F", 0

    @staticmethod
    def compute_total(cat1, cat2, fat, ca):
        """Weighted total, VIT-style: CAT-1 15%, CAT-2 15%, FAT 40%,
        Continuous Assessment 30% (each component given out of 100)."""
        return round(cat1 * 0.15 + cat2 * 0.15 + fat * 0.40 + ca * 0.30, 2)

    def semester_gpa(self, course_results):
        """course_results: list of dicts with 'credits' and 'grade_point'."""
        total_credits = sum(c["credits"] for c in course_results)
        if total_credits == 0:
            return 0.0
        weighted = sum(c["credits"] * c["grade_point"] for c in course_results)
        return round(weighted / total_credits, 2)

    def cumulative_gpa(self, all_semester_results):
        """all_semester_results: list of lists of course_results."""
        flat = [c for sem in all_semester_results for c in sem]
        return self.semester_gpa(flat)


# ==================================================================
# ABSTRACT BASE CLASS: Person
# ==================================================================

class Person(ABC):
    """Abstract base class shared by Student, Faculty and
    Administrator. Demonstrates abstraction + inheritance."""

    college_name = "Institute of Technology and Advanced Sciences"  # class variable

    def __init__(self, person_id, name, dob, gender, email, phone, address):
        self.person_id = person_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.email = email
        self.phone = phone
        self.address = address

    @abstractmethod
    def dashboard_menu(self):
        """Each subclass must define its own menu items."""
        raise NotImplementedError

    @abstractmethod
    def role(self):
        raise NotImplementedError

    @property
    def contact_info(self):
        return f"{self.email} | {self.phone}"

    def display_profile(self):
        sub_header(f"{self.role()} PROFILE")
        print(f"ID          : {self.person_id}")
        print(f"Name        : {self.name}")
        print(f"DOB         : {self.dob}")
        print(f"Gender      : {self.gender}")
        print(f"Email       : {self.email}")
        print(f"Phone       : {self.phone}")
        print(f"Address     : {self.address}")
        print(f"Institution : {Person.college_name}")

    @staticmethod
    def is_valid_email(email):
        return "@" in email and "." in email.split("@")[-1]

    def __str__(self):
        return f"{self.role()}: {self.name} ({self.person_id})"


class Student(Person):
    required_attendance_default = 75.0  # class variable fallback

    def __init__(self, person_id, name, dob, gender, email, phone, address,
                 registration_number, school, program, campus, semester,
                 batch, section):
        super().__init__(person_id, name, dob, gender, email, phone, address)
        self.registration_number = registration_number
        self.school = school
        self.program = program
        self.campus = campus
        self.semester = semester
        self.batch = batch
        self.section = section
        self._cgpa = 0.0
        self.credits_completed = 0

    def role(self):
        return "Student"

    @property
    def cgpa(self):
        return self._cgpa

    @cgpa.setter
    def cgpa(self, value):
        if 0.0 <= value <= 10.0:
            self._cgpa = round(value, 2)
        else:
            raise ValueError("CGPA must be between 0.0 and 10.0")

    @property
    def academic_standing(self):
        if self._cgpa >= 9.0:
            return "Excellent"
        elif self._cgpa >= 7.5:
            return "Good"
        elif self._cgpa >= 6.0:
            return "Satisfactory"
        elif self._cgpa > 0:
            return "Needs Improvement"
        return "Not Available"

    def dashboard_menu(self):
        return [
            "Profile", "Academic Performance", "Attendance",
            "FFCS Registration", "Timetable", "Examinations", "Fees",
            "Hostel", "Transport", "Library", "Leave", "Clubs",
            "Placements", "Notices", "Logout",
        ]

    def display_profile(self):
        super().display_profile()
        print(f"Reg. No.    : {self.registration_number}")
        print(f"School      : {self.school}")
        print(f"Program     : {self.program}")
        print(f"Campus      : {self.campus}")
        print(f"Semester    : {self.semester}")
        print(f"Batch       : {self.batch}")
        print(f"Section     : {self.section}")
        print(f"CGPA        : {self.cgpa}")
        print(f"Credits     : {self.credits_completed}")
        print(f"Standing    : {self.academic_standing}")

    def to_dict(self):
        return {
            "person_id": self.person_id, "name": self.name, "dob": self.dob,
            "gender": self.gender, "email": self.email, "phone": self.phone,
            "address": self.address,
            "registration_number": self.registration_number,
            "school": self.school, "program": self.program,
            "campus": self.campus, "semester": self.semester,
            "batch": self.batch, "section": self.section,
            "cgpa": self._cgpa, "credits_completed": self.credits_completed,
        }

    @classmethod
    def from_dict(cls, d):
        student = cls(
            d["person_id"], d["name"], d["dob"], d["gender"], d["email"],
            d["phone"], d["address"], d["registration_number"], d["school"],
            d["program"], d["campus"], d["semester"], d["batch"], d["section"],
        )
        student._cgpa = d.get("cgpa", 0.0)
        student.credits_completed = d.get("credits_completed", 0)
        return student


class Faculty(Person):
    def __init__(self, person_id, name, dob, gender, email, phone, address,
                 employee_id, school, designation, specialization):
        super().__init__(person_id, name, dob, gender, email, phone, address)
        self.employee_id = employee_id
        self.school = school
        self.designation = designation
        self.specialization = specialization

    def role(self):
        return "Faculty"

    def dashboard_menu(self):
        return [
            "Profile", "My Courses", "Timetable", "Students", "Attendance",
            "Marks", "Leave Requests", "Notices", "Course Statistics",
            "Logout",
        ]

    def display_profile(self):
        super().display_profile()
        print(f"Employee ID   : {self.employee_id}")
        print(f"School        : {self.school}")
        print(f"Designation   : {self.designation}")
        print(f"Specialization: {self.specialization}")

    def to_dict(self):
        return {
            "person_id": self.person_id, "name": self.name, "dob": self.dob,
            "gender": self.gender, "email": self.email, "phone": self.phone,
            "address": self.address, "employee_id": self.employee_id,
            "school": self.school, "designation": self.designation,
            "specialization": self.specialization,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["person_id"], d["name"], d["dob"], d["gender"], d["email"],
            d["phone"], d["address"], d["employee_id"], d["school"],
            d["designation"], d["specialization"],
        )


class Administrator(Person):
    def __init__(self, person_id, name, dob, gender, email, phone, address,
                 admin_level="Standard"):
        super().__init__(person_id, name, dob, gender, email, phone, address)
        self.admin_level = admin_level

    def role(self):
        return "Administrator"

    def dashboard_menu(self):
        return [
            "Student Management", "Faculty Management", "Course Management",
            "FFCS Management", "Examination Management", "Fee Management",
            "Hostel Management", "Transport Management", "Library Management",
            "Club Management", "Placement Management", "Notice Management",
            "System Statistics", "Logout",
        ]


# ==================================================================
# COURSE / ENROLLMENT
# ==================================================================

class Course:
    def __init__(self, course_code, course_name, credits, faculty_id,
                 faculty_name, slot, room, capacity, registered_students=None):
        self.course_code = course_code
        self.course_name = course_name
        self.credits = credits
        self.faculty_id = faculty_id
        self.faculty_name = faculty_name
        self.slot = slot
        self.room = room
        self.capacity = capacity
        self.registered_students = registered_students if registered_students else []

    @property
    def available_seats(self):
        return max(self.capacity - len(self.registered_students), 0)

    @property
    def is_full(self):
        return self.available_seats <= 0

    def to_dict(self):
        return {
            "course_code": self.course_code, "course_name": self.course_name,
            "credits": self.credits, "faculty_id": self.faculty_id,
            "faculty_name": self.faculty_name, "slot": self.slot,
            "room": self.room, "capacity": self.capacity,
            "registered_students": self.registered_students,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["course_code"], d["course_name"], d["credits"], d["faculty_id"],
            d["faculty_name"], d["slot"], d["room"], d["capacity"],
            d.get("registered_students", []),
        )

    def __str__(self):
        return (f"{self.course_code} | {self.course_name} | Credits:{self.credits} "
                f"| Faculty:{self.faculty_name} | Slot:{self.slot} | Room:{self.room} "
                f"| Seats:{self.available_seats}/{self.capacity}")


# ==================================================================
# MANAGER CLASSES (composed into CollegeManagementSystem)
# ==================================================================

class AuthenticationManager:
    def __init__(self, fm: FileManager):
        self.fm = fm

    def register_user(self, username, password, role, linked_id):
        users = self.fm.load_data(FILES["users"])
        if any(u["username"] == username for u in users):
            return False, "Username already exists."
        users.append({
            "username": username, "password": password,
            "role": role, "linked_id": linked_id,
        })
        self.fm.save_data(FILES["users"], users)
        return True, "Registered successfully."

    def login(self, username, password, expected_role=None):
        users = self.fm.load_data(FILES["users"])
        for u in users:
            if u["username"] == username and u["password"] == password:
                if expected_role and u["role"] != expected_role:
                    return None, "This account is not registered for that role."
                return u, "Login successful."
        return None, "Invalid username or password."


class FFCSManager:
    def __init__(self, fm: FileManager, settings):
        self.fm = fm
        self.settings = settings

    def list_courses(self):
        return [Course.from_dict(c) for c in self.fm.load_data(FILES["courses"])]

    def find_course(self, code):
        c = self.fm.find_one(FILES["courses"], "course_code", code.upper())
        return Course.from_dict(c) if c else None

    def search_courses(self, keyword):
        keyword = keyword.lower()
        return [c for c in self.list_courses()
                if keyword in c.course_code.lower() or keyword in c.course_name.lower()]

    def register(self, student_id, course_code):
        if not self.settings.get("ffcs_registration_open", True):
            return False, "FFCS registration window is currently closed."
        course = self.find_course(course_code)
        if not course:
            return False, "Invalid course code."
        enrollments = self.fm.load_data(FILES["enrollments"])
        if any(e["student_id"] == student_id and e["course_code"] == course_code
               for e in enrollments):
            return False, "Already registered for this course."
        if course.is_full:
            return False, "Course has reached full capacity."
        course.registered_students.append(student_id)
        self.fm.update_record(FILES["courses"], "course_code", course_code,
                               {"registered_students": course.registered_students})
        enrollments.append({
            "enrollment_id": generate_id("ENR"), "student_id": student_id,
            "course_code": course_code, "registered_on": str(datetime.now().date()),
            "status": "REGISTERED",
        })
        self.fm.save_data(FILES["enrollments"], enrollments)
        return True, f"Registered for {course_code} successfully."

    def drop(self, student_id, course_code):
        course = self.find_course(course_code)
        if not course:
            return False, "Invalid course code."
        if student_id not in course.registered_students:
            return False, "You are not registered for this course."
        course.registered_students.remove(student_id)
        self.fm.update_record(FILES["courses"], "course_code", course_code,
                               {"registered_students": course.registered_students})
        self.fm.delete_record(FILES["enrollments"], "student_id", student_id) \
            if False else None  # placeholder guard, real removal below
        enrollments = self.fm.load_data(FILES["enrollments"])
        enrollments = [e for e in enrollments if not (
            e["student_id"] == student_id and e["course_code"] == course_code)]
        self.fm.save_data(FILES["enrollments"], enrollments)
        return True, f"Dropped {course_code} successfully."

    def student_courses(self, student_id):
        enrollments = self.fm.find_all(FILES["enrollments"], "student_id", student_id)
        codes = [e["course_code"] for e in enrollments]
        return [c for c in self.list_courses() if c.course_code in codes]


class AttendanceManager:
    def __init__(self, fm: FileManager, settings):
        self.fm = fm
        self.settings = settings

    def mark_attendance(self, course_code, student_id, date_str, status):
        records = self.fm.load_data(FILES["attendance"])
        for r in records:
            if (r["course_code"] == course_code and r["student_id"] == student_id
                    and r["date"] == date_str):
                r["status"] = status
                self.fm.save_data(FILES["attendance"], records)
                return "Attendance updated."
        records.append({
            "record_id": generate_id("ATT"), "course_code": course_code,
            "student_id": student_id, "date": date_str, "status": status,
        })
        self.fm.save_data(FILES["attendance"], records)
        return "Attendance marked."

    def course_attendance_for_student(self, student_id, course_code):
        records = [r for r in self.fm.load_data(FILES["attendance"])
                   if r["student_id"] == student_id and r["course_code"] == course_code]
        conducted = len(records)
        attended = len([r for r in records if r["status"] == "Present"])
        pct = round((attended / conducted) * 100, 2) if conducted else 0.0
        return conducted, attended, pct

    def full_report_for_student(self, student_id, course_codes):
        report = []
        required = self.settings.get("required_attendance_percentage", 75.0)
        for code in course_codes:
            conducted, attended, pct = self.course_attendance_for_student(student_id, code)
            status = "OK" if pct >= required or conducted == 0 else "LOW - WARNING"
            report.append({
                "course_code": code, "conducted": conducted,
                "attended": attended, "percentage": pct, "status": status,
            })
        return report

    def low_attendance_students(self, course_code, roster):
        required = self.settings.get("required_attendance_percentage", 75.0)
        result = []
        for sid in roster:
            conducted, attended, pct = self.course_attendance_for_student(sid, course_code)
            if conducted > 0 and pct < required:
                result.append((sid, pct))
        return result


class FeeManager:
    def __init__(self, fm: FileManager):
        self.fm = fm

    def get_fee_record(self, student_id):
        return self.fm.find_one(FILES["fees"], "student_id", student_id)

    def create_fee_record(self, student_id, tuition, hostel, transport, library_fine=0, other=0):
        record = {
            "student_id": student_id, "tuition_fee": tuition, "hostel_fee": hostel,
            "transport_fee": transport, "library_fine": library_fine,
            "other_charges": other, "paid_amount": 0,
        }
        self.fm.add_record(FILES["fees"], record)
        return record

    @staticmethod
    def total_due(record):
        return (record["tuition_fee"] + record["hostel_fee"] + record["transport_fee"]
                + record["library_fine"] + record["other_charges"])

    def pay(self, student_id, amount):
        record = self.get_fee_record(student_id)
        if not record:
            return False, "No fee record found."
        total = self.total_due(record)
        pending = total - record["paid_amount"]
        if amount <= 0:
            return False, "Payment amount must be positive."
        if amount > pending:
            return False, f"Amount exceeds pending balance of Rs.{pending:.2f}."
        record["paid_amount"] += amount
        self.fm.update_record(FILES["fees"], "student_id", student_id,
                               {"paid_amount": record["paid_amount"]})
        return True, f"Payment of Rs.{amount:.2f} recorded successfully."

    def status(self, record):
        total = self.total_due(record)
        pending = total - record["paid_amount"]
        if pending <= 0:
            return "PAID"
        elif record["paid_amount"] > 0:
            return "PARTIALLY PAID"
        return "PENDING"


class HostelManager:
    def __init__(self, fm: FileManager):
        self.fm = fm

    def add_room(self, block, room_no, room_type, capacity):
        record = {
            "room_id": generate_id("RM"), "block": block, "room_no": room_no,
            "room_type": room_type, "capacity": capacity, "occupants": [],
        }
        self.fm.add_record(FILES["hostel"], record)
        return record

    def list_rooms(self):
        return self.fm.load_data(FILES["hostel"])

    def allocate(self, student_id, room_id):
        rooms = self.list_rooms()
        for r in rooms:
            if r["room_id"] == room_id:
                if student_id in r["occupants"]:
                    return False, "Student already allocated to this room."
                if len(r["occupants"]) >= r["capacity"]:
                    return False, "Room is at full capacity."
                r["occupants"].append(student_id)
                self.fm.save_data(FILES["hostel"], rooms)
                return True, f"Allocated room {r['room_no']} ({r['block']})."
        return False, "Room not found."

    def vacate(self, student_id, room_id):
        rooms = self.list_rooms()
        for r in rooms:
            if r["room_id"] == room_id and student_id in r["occupants"]:
                r["occupants"].remove(student_id)
                self.fm.save_data(FILES["hostel"], rooms)
                return True, "Room vacated."
        return False, "Allocation not found."

    def find_allocation(self, student_id):
        for r in self.list_rooms():
            if student_id in r["occupants"]:
                return r
        return None

    def occupancy_stats(self):
        rooms = self.list_rooms()
        total_cap = sum(r["capacity"] for r in rooms)
        total_occ = sum(len(r["occupants"]) for r in rooms)
        return total_occ, total_cap


class TransportManager:
    def __init__(self, fm: FileManager):
        self.fm = fm

    def add_route(self, bus_number, route_name, pickup_point, pickup_time,
                  drop_time, fee):
        record = {
            "route_id": generate_id("BUS"), "bus_number": bus_number,
            "route_name": route_name, "pickup_point": pickup_point,
            "pickup_time": pickup_time, "drop_time": drop_time,
            "fee": fee, "assigned_students": [],
        }
        self.fm.add_record(FILES["transport"], record)
        return record

    def list_routes(self):
        return self.fm.load_data(FILES["transport"])

    def assign_student(self, student_id, route_id):
        routes = self.list_routes()
        for r in routes:
            if r["route_id"] == route_id:
                if student_id in r["assigned_students"]:
                    return False, "Already assigned to this route."
                r["assigned_students"].append(student_id)
                self.fm.save_data(FILES["transport"], routes)
                return True, f"Assigned to route {r['route_name']}."
        return False, "Route not found."

    def find_assignment(self, student_id):
        for r in self.list_routes():
            if student_id in r["assigned_students"]:
                return r
        return None


class LibraryManager:
    def __init__(self, fm: FileManager):
        self.fm = fm
        self.fine_per_day = 5

    def add_book(self, title, author, isbn, copies):
        record = {
            "book_id": generate_id("BK"), "title": title, "author": author,
            "isbn": isbn, "total_copies": copies, "available_copies": copies,
        }
        self.fm.add_record(FILES["books"], record)
        return record

    def list_books(self):
        return self.fm.load_data(FILES["books"])

    def search_books(self, keyword):
        keyword = keyword.lower()
        return [b for b in self.list_books()
                if keyword in b["title"].lower() or keyword in b["author"].lower()]

    def borrow(self, student_id, book_id):
        books = self.list_books()
        for b in books:
            if b["book_id"] == book_id:
                if b["available_copies"] <= 0:
                    return False, "No copies currently available."
                b["available_copies"] -= 1
                self.fm.save_data(FILES["books"], books)
                due_date = (datetime.now() + timedelta(days=14)).date()
                self.fm.add_record(FILES["library_transactions"], {
                    "txn_id": generate_id("LIB"), "student_id": student_id,
                    "book_id": book_id, "title": b["title"],
                    "borrow_date": str(datetime.now().date()),
                    "due_date": str(due_date), "return_date": None, "fine": 0,
                })
                return True, f"Borrowed '{b['title']}'. Due on {due_date}."
        return False, "Book not found."

    def return_book(self, student_id, txn_id):
        txns = self.fm.load_data(FILES["library_transactions"])
        for t in txns:
            if t["txn_id"] == txn_id and t["student_id"] == student_id:
                if t["return_date"]:
                    return False, "Book already returned."
                t["return_date"] = str(datetime.now().date())
                due = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
                today = datetime.now().date()
                overdue_days = max((today - due).days, 0)
                t["fine"] = overdue_days * self.fine_per_day
                self.fm.save_data(FILES["library_transactions"], txns)
                books = self.list_books()
                for b in books:
                    if b["book_id"] == t["book_id"]:
                        b["available_copies"] += 1
                self.fm.save_data(FILES["books"], books)
                msg = "Book returned."
                if t["fine"] > 0:
                    msg += f" Fine due: Rs.{t['fine']}"
                return True, msg
        return False, "Borrow record not found."

    def borrowed_by(self, student_id):
        return [t for t in self.fm.load_data(FILES["library_transactions"])
                if t["student_id"] == student_id and not t["return_date"]]

    def calculate_fine(self, txn):
        if txn["return_date"]:
            return txn["fine"]
        due = datetime.strptime(txn["due_date"], "%Y-%m-%d").date()
        today = datetime.now().date()
        overdue_days = max((today - due).days, 0)
        return overdue_days * self.fine_per_day


class PlacementManager:
    def __init__(self, fm: FileManager):
        self.fm = fm

    def add_company(self, name, role_title, min_cgpa, package_lpa):
        record = {
            "company_id": generate_id("CMP"), "company_name": name,
            "role_title": role_title, "min_cgpa": min_cgpa,
            "package_lpa": package_lpa,
        }
        self.fm.add_record(FILES["placements"], record)
        return record

    def list_companies(self):
        return self.fm.load_data(FILES["placements"])

    def eligible_companies(self, cgpa):
        return [c for c in self.list_companies() if cgpa >= c["min_cgpa"]]

    def apply(self, student_id, company_id):
        applications_file = "placement_applications"
        FILES.setdefault(applications_file, "placement_applications.json")
        apps = self.fm.load_data(FILES[applications_file])
        if any(a["student_id"] == student_id and a["company_id"] == company_id
               for a in apps):
            return False, "Already applied to this company."
        apps.append({
            "application_id": generate_id("APP"), "student_id": student_id,
            "company_id": company_id, "status": "APPLIED",
            "applied_on": str(datetime.now().date()),
        })
        self.fm.save_data(FILES[applications_file], apps)
        return True, "Application submitted."

    def student_applications(self, student_id):
        apps_file = FILES.get("placement_applications", "placement_applications.json")
        return [a for a in self.fm.load_data(apps_file) if a["student_id"] == student_id]

    def update_status(self, application_id, status):
        apps_file = FILES.get("placement_applications", "placement_applications.json")
        return self.fm.update_record(apps_file, "application_id", application_id,
                                      {"status": status})


# ==================================================================
# THE MAIN SYSTEM CLASS (composition root)
# ==================================================================

class CollegeManagementSystem:
    def __init__(self):
        self.fm = FileManager()
        self.settings = self.fm.load_data(FILES["settings"], dict(DEFAULT_SETTINGS))
        self.auth = AuthenticationManager(self.fm)
        self.ffcs = FFCSManager(self.fm, self.settings)
        self.attendance_mgr = AttendanceManager(self.fm, self.settings)
        self.fee_mgr = FeeManager(self.fm)
        self.hostel_mgr = HostelManager(self.fm)
        self.transport_mgr = TransportManager(self.fm)
        self.library_mgr = LibraryManager(self.fm)
        self.placement_mgr = PlacementManager(self.fm)
        self.grade_calc = GradeCalculator()
        self.current_user = None
        self._initialize_demo_data_if_needed()

    # ---------------- Demo Data ----------------

    def _initialize_demo_data_if_needed(self):
        if self.fm.load_data(FILES["users"]):
            return  # already initialised
        print("First run detected. Initialising demo data...")

        schools = ["School of Computer Science", "School of Electronics",
                   "School of Mechanical Engineering"]
        programs = ["B.Tech CSE", "B.Tech ECE", "B.Tech Mech"]
        first_names = ["Aarav", "Vivaan", "Ishaan", "Ananya", "Diya", "Kabir",
                       "Sara", "Reyansh", "Myra", "Aditya"]
        last_names = ["Sharma", "Verma", "Iyer", "Reddy", "Gupta", "Nair",
                      "Joshi", "Khan", "Chatterjee", "Patel"]

        students = []
        for i in range(1, 11):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            student = Student(
                person_id=generate_id("STU"), name=name,
                dob=f"200{random.randint(2, 6)}-0{random.randint(1, 9)}-1{i % 9}",
                gender=random.choice(["Male", "Female"]),
                email=f"student{i:02d}@college.edu.in", phone=f"9{random.randint(100000000, 999999999)}",
                address=f"{i} MG Road, Bengaluru",
                registration_number=f"21BCE{1000 + i}",
                school=random.choice(schools), program=random.choice(programs),
                campus="Main Campus", semester=self.settings["current_semester"],
                batch="2021-2025", section=random.choice(["A", "B", "C"]),
            )
            student.cgpa = round(random.uniform(6.0, 9.5), 2)
            student.credits_completed = random.randint(60, 120)
            students.append(student)
        self.fm.save_data(FILES["students"], [s.to_dict() for s in students])

        faculty_specs = ["Artificial Intelligence", "Data Structures",
                         "VLSI Design", "Thermodynamics", "Networks"]
        faculty_list = []
        for i in range(1, 6):
            fac = Faculty(
                person_id=generate_id("FAC"), name=f"Dr. {random.choice(last_names)}",
                dob=f"198{random.randint(0, 5)}-0{random.randint(1, 9)}-1{i}",
                gender=random.choice(["Male", "Female"]),
                email=f"faculty{i:02d}@college.edu.in", phone=f"8{random.randint(100000000, 999999999)}",
                address=f"Faculty Quarters Block {i}",
                employee_id=f"EMP{2000 + i}", school=random.choice(schools),
                designation=random.choice(["Assistant Professor", "Associate Professor", "Professor"]),
                specialization=random.choice(faculty_specs),
            )
            faculty_list.append(fac)
        self.fm.save_data(FILES["faculty"], [f.to_dict() for f in faculty_list])

        course_catalog = [
            ("CSE1001", "Problem Solving and Programming", 4, "A1"),
            ("CSE1002", "Data Structures and Algorithms", 4, "B1"),
            ("MAT1001", "Calculus", 3, "C1"),
            ("PHY1001", "Engineering Physics", 3, "D1"),
            ("CHY1001", "Engineering Chemistry", 3, "E1"),
            ("ENG1001", "Effective Communication", 2, "F1"),
            ("EVS1001", "Environmental Studies", 2, "G1"),
            ("CSE2001", "Object Oriented Programming", 4, "A2"),
            ("CSE2002", "Database Systems", 4, "B2"),
            ("CSE2003", "Computer Networks", 3, "C2"),
        ]
        courses = []
        for idx, (code, title, credits, slot) in enumerate(course_catalog):
            fac = faculty_list[idx % len(faculty_list)]
            courses.append(Course(
                course_code=code, course_name=title, credits=credits,
                faculty_id=fac.person_id, faculty_name=fac.name, slot=slot,
                room=f"AB1-{100 + idx}", capacity=random.randint(3, 6),
            ))
        self.fm.save_data(FILES["courses"], [c.to_dict() for c in courses])

        # Enroll each student in 3 random courses
        enrollments = []
        for s in students:
            picks = random.sample(courses, k=min(3, len(courses)))
            for c in picks:
                if len(c.registered_students) < c.capacity:
                    c.registered_students.append(s.person_id)
                    enrollments.append({
                        "enrollment_id": generate_id("ENR"),
                        "student_id": s.person_id, "course_code": c.course_code,
                        "registered_on": str(datetime.now().date()),
                        "status": "REGISTERED",
                    })
        self.fm.save_data(FILES["courses"], [c.to_dict() for c in courses])
        self.fm.save_data(FILES["enrollments"], enrollments)

        # Attendance demo data (last 10 sessions per enrollment)
        attendance_records = []
        for e in enrollments:
            for day in range(10):
                date_str = str((datetime.now() - timedelta(days=day)).date())
                status = random.choices(["Present", "Absent"], weights=[8, 2])[0]
                attendance_records.append({
                    "record_id": generate_id("ATT"), "course_code": e["course_code"],
                    "student_id": e["student_id"], "date": date_str, "status": status,
                })
        self.fm.save_data(FILES["attendance"], attendance_records)

        # Marks demo data
        marks_records = []
        for e in enrollments:
            cat1 = random.randint(60, 100)
            cat2 = random.randint(60, 100)
            fat = random.randint(50, 100)
            ca = random.randint(60, 100)
            total = self.grade_calc.compute_total(cat1, cat2, fat, ca)
            letter, points = self.grade_calc.marks_to_grade(total)
            marks_records.append({
                "student_id": e["student_id"], "course_code": e["course_code"],
                "cat1": cat1, "cat2": cat2, "fat": fat, "ca": ca,
                "total": total, "grade": letter, "grade_point": points,
            })
        self.fm.save_data(FILES["marks"], marks_records)

        # Exams
        exams = []
        for c in courses:
            for ex_type in ["CAT-1", "CAT-2", "FAT"]:
                exams.append({
                    "exam_id": generate_id("EXM"), "course_code": c.course_code,
                    "exam_type": ex_type,
                    "date": str((datetime.now() + timedelta(days=random.randint(1, 60))).date()),
                    "max_marks": 100,
                })
        self.fm.save_data(FILES["exams"], exams)

        # Fees
        fee_records = []
        for s in students:
            fee_records.append({
                "student_id": s.person_id, "tuition_fee": 150000,
                "hostel_fee": 60000, "transport_fee": 15000,
                "library_fine": 0, "other_charges": 5000,
                "paid_amount": random.choice([0, 50000, 230000]),
            })
        self.fm.save_data(FILES["fees"], fee_records)

        # Hostel
        hostel_rooms = []
        for i in range(1, 6):
            hostel_rooms.append({
                "room_id": generate_id("RM"), "block": random.choice(["A", "B", "C"]),
                "room_no": f"{100 + i}", "room_type": random.choice(["Single", "Double", "Triple"]),
                "capacity": random.choice([1, 2, 3]), "occupants": [],
            })
        for i, s in enumerate(students[:5]):
            room = hostel_rooms[i % len(hostel_rooms)]
            if len(room["occupants"]) < room["capacity"]:
                room["occupants"].append(s.person_id)
        self.fm.save_data(FILES["hostel"], hostel_rooms)

        # Transport
        transport_routes = []
        route_names = ["Whitefield Express", "Electronic City Link", "Koramangala Shuttle"]
        for i, rname in enumerate(route_names, start=1):
            transport_routes.append({
                "route_id": generate_id("BUS"), "bus_number": f"KA-01-{1000 + i}",
                "route_name": rname, "pickup_point": f"{rname} Stop",
                "pickup_time": "07:30 AM", "drop_time": "05:30 PM",
                "fee": 15000, "assigned_students": [s.person_id for s in students[i::3]][:3],
            })
        self.fm.save_data(FILES["transport"], transport_routes)

        # Library
        book_titles = [
            ("Introduction to Algorithms", "Cormen et al."),
            ("Clean Code", "Robert C. Martin"),
            ("Operating System Concepts", "Silberschatz"),
            ("Computer Networks", "Tanenbaum"),
            ("Database System Concepts", "Silberschatz"),
            ("Artificial Intelligence: A Modern Approach", "Russell & Norvig"),
            ("Design Patterns", "Gang of Four"),
            ("The Pragmatic Programmer", "Hunt & Thomas"),
            ("Physics for Engineers", "Serway"),
            ("Engineering Mathematics", "B.S. Grewal"),
            ("Digital Logic Design", "Morris Mano"),
            ("Compilers: Principles and Techniques", "Aho et al."),
            ("Computer Organization", "Hamacher"),
            ("Software Engineering", "Sommerville"),
            ("Data Communications", "Forouzan"),
        ]
        books = []
        for title, author in book_titles:
            copies = random.randint(2, 6)
            books.append({
                "book_id": generate_id("BK"), "title": title, "author": author,
                "isbn": f"978-{random.randint(1000000000, 9999999999)}",
                "total_copies": copies, "available_copies": copies,
            })
        self.fm.save_data(FILES["books"], books)

        # Clubs
        club_names = ["Coding Club", "Robotics Club", "Music Club",
                      "Dramatics Club", "Entrepreneurship Cell"]
        clubs = []
        for cname in club_names:
            members = random.sample([s.person_id for s in students], k=random.randint(2, 5))
            clubs.append({
                "club_id": generate_id("CLB"), "club_name": cname,
                "members": members,
                "events": [{
                    "event_id": generate_id("EVT"), "event_name": f"{cname} Annual Meet",
                    "date": str((datetime.now() + timedelta(days=random.randint(5, 90))).date()),
                }],
            })
        self.fm.save_data(FILES["clubs"], clubs)

        # Placements (companies)
        companies = [
            {"company_id": generate_id("CMP"), "company_name": "TechNova Solutions",
             "role_title": "Software Engineer", "min_cgpa": 7.0, "package_lpa": 12},
            {"company_id": generate_id("CMP"), "company_name": "DataForge Analytics",
             "role_title": "Data Analyst", "min_cgpa": 6.5, "package_lpa": 9},
            {"company_id": generate_id("CMP"), "company_name": "CoreStack Systems",
             "role_title": "Backend Developer", "min_cgpa": 7.5, "package_lpa": 15},
        ]
        self.fm.save_data(FILES["placements"], companies)
        self.fm.save_data("placement_applications.json", [])
        FILES["placement_applications"] = "placement_applications.json"

        # Leaves
        self.fm.save_data(FILES["leaves"], [])

        # Notices
        notices = [
            {"notice_id": generate_id("NOT"), "category": "Academic",
             "title": "Mid-semester exams schedule released",
             "content": "Check the examination tab for CAT-1 timetable.",
             "date": str(datetime.now().date())},
            {"notice_id": generate_id("NOT"), "category": "Placement",
             "title": "TechNova Solutions campus drive",
             "content": "Eligible students can apply from the Placements tab.",
             "date": str(datetime.now().date())},
            {"notice_id": generate_id("NOT"), "category": "General",
             "title": "Library timings extended",
             "content": "Library will remain open till 9 PM during exam weeks.",
             "date": str(datetime.now().date())},
        ]
        self.fm.save_data(FILES["notices"], notices)

        # Users (login accounts)
        users = [{"username": "admin", "password": "admin123",
                   "role": "Administrator", "linked_id": "ADMIN-0001"}]
        self.fm.save_data(FILES["users"], [])  # clear placeholder
        admin = Administrator(
            person_id="ADMIN-0001", name="System Administrator", dob="1980-01-01",
            gender="Other", email="admin@college.edu.in", phone="9000000000",
            address="Admin Block", admin_level="Super Admin",
        )
        for i, fac in enumerate(faculty_list, start=1):
            username = f"faculty{i:02d}" if i > 1 else "faculty01"
            self.auth.register_user(username, "faculty123", "Faculty", fac.person_id)
        for i, s in enumerate(students, start=1):
            username = f"student{i:02d}" if i > 1 else "student01"
            self.auth.register_user(username, "student123", "Student", s.person_id)
        self.auth.register_user("admin", "admin123", "Administrator", admin.person_id)
        # Store the single administrator record for lookups
        self.fm.save_data("administrators.json", [{
            "person_id": admin.person_id, "name": admin.name, "dob": admin.dob,
            "gender": admin.gender, "email": admin.email, "phone": admin.phone,
            "address": admin.address, "admin_level": admin.admin_level,
        }])
        FILES["administrators"] = "administrators.json"

        self.fm.save_data(FILES["settings"], self.settings)
        print("Demo data initialised successfully.\n")

    # ---------------- Object loaders ----------------

    def _load_student(self, person_id):
        d = self.fm.find_one(FILES["students"], "person_id", person_id)
        return Student.from_dict(d) if d else None

    def _load_faculty(self, person_id):
        d = self.fm.find_one(FILES["faculty"], "person_id", person_id)
        return Faculty.from_dict(d) if d else None

    def _load_administrator(self, person_id):
        FILES.setdefault("administrators", "administrators.json")
        d = self.fm.find_one(FILES["administrators"], "person_id", person_id)
        if d:
            return Administrator(d["person_id"], d["name"], d["dob"], d["gender"],
                                  d["email"], d["phone"], d["address"],
                                  d.get("admin_level", "Standard"))
        return None

    # ---------------- Main Menu Loop ----------------

    def run(self):
        header("VIT-STYLE COLLEGE MANAGEMENT SYSTEM")
        print(f"{Person.college_name}\nAcademic Year: {self.settings['current_academic_year']}")
        while True:
            print("\n1. Student Login")
            print("2. Faculty Login")
            print("3. Administrator Login")
            print("4. Exit")
            choice = safe_int_input("Enter choice: ", 1, 4)
            if choice == 1:
                self._login_flow("Student")
            elif choice == 2:
                self._login_flow("Faculty")
            elif choice == 3:
                self._login_flow("Administrator")
            elif choice == 4:
                print("Thank you for using the College Management System. Goodbye!")
                break

    def _login_flow(self, role):
        header(f"{role.upper()} LOGIN")
        username = non_empty_input("Username: ")
        password = non_empty_input("Password: ")
        user, message = self.auth.login(username, password, expected_role=role)
        if not user:
            print(f"[LOGIN FAILED] {message}")
            pause()
            return
        print(f"[LOGIN SUCCESS] Welcome, {username}!")
        if role == "Student":
            person = self._load_student(user["linked_id"])
            self._student_session(person)
        elif role == "Faculty":
            person = self._load_faculty(user["linked_id"])
            self._faculty_session(person)
        else:
            person = self._load_administrator(user["linked_id"])
            self._admin_session(person)

    # ---------------- STUDENT SESSION ----------------

    def _student_session(self, student: Student):
        while True:
            header("STUDENT DASHBOARD")
            menu = student.dashboard_menu()
            for i, item in enumerate(menu, start=1):
                print(f"{i}. {item}")
            choice = safe_int_input("Enter choice: ", 1, len(menu))
            action = menu[choice - 1]

            if action == "Profile":
                student.display_profile()
            elif action == "Academic Performance":
                self._student_academic_performance(student)
            elif action == "Attendance":
                self._student_attendance(student)
            elif action == "FFCS Registration":
                self._student_ffcs(student)
            elif action == "Timetable":
                self._student_timetable(student)
            elif action == "Examinations":
                self._student_examinations(student)
            elif action == "Fees":
                self._student_fees(student)
            elif action == "Hostel":
                self._student_hostel(student)
            elif action == "Transport":
                self._student_transport(student)
            elif action == "Library":
                self._student_library(student)
            elif action == "Leave":
                self._student_leave(student)
            elif action == "Clubs":
                self._student_clubs(student)
            elif action == "Placements":
                self._student_placements(student)
            elif action == "Notices":
                self._show_notices()
            elif action == "Logout":
                print("Logged out successfully.")
                break
            pause()

    def _student_academic_performance(self, student):
        sub_header("ACADEMIC PERFORMANCE")
        marks = self.fm.find_all(FILES["marks"], "student_id", student.person_id)
        if not marks:
            print("No academic records found yet.")
            return
        results = []
        print(f"{'Course':10}{'CAT1':>6}{'CAT2':>6}{'FAT':>6}{'CA':>6}{'Total':>8}{'Grade':>7}{'GP':>4}")
        for m in marks:
            print(f"{m['course_code']:10}{m['cat1']:>6}{m['cat2']:>6}{m['fat']:>6}"
                  f"{m['ca']:>6}{m['total']:>8}{m['grade']:>7}{m['grade_point']:>4}")
            course = self.ffcs.find_course(m["course_code"])
            credits = course.credits if course else 3
            results.append({"credits": credits, "grade_point": m["grade_point"]})
        gpa = self.grade_calc.semester_gpa(results)
        print(f"\nSemester GPA : {gpa}")
        print(f"CGPA (recorded): {student.cgpa}")

    def _student_attendance(self, student):
        sub_header("ATTENDANCE")
        courses = self.ffcs.student_courses(student.person_id)
        if not courses:
            print("You are not registered for any courses.")
            return
        codes = [c.course_code for c in courses]
        report = self.attendance_mgr.full_report_for_student(student.person_id, codes)
        print(f"{'Course':10}{'Conducted':>11}{'Attended':>10}{'Pct%':>8}   Status")
        for r in report:
            print(f"{r['course_code']:10}{r['conducted']:>11}{r['attended']:>10}"
                  f"{r['percentage']:>8}   {r['status']}")

    def _student_ffcs(self, student):
        while True:
            sub_header("FFCS COURSE REGISTRATION")
            print("1. View Available Courses")
            print("2. Search Courses")
            print("3. Register for a Course")
            print("4. Drop a Course")
            print("5. View My Registered Courses")
            print("6. Back")
            choice = safe_int_input("Enter choice: ", 1, 6)
            if choice == 1:
                for c in self.ffcs.list_courses():
                    print(c)
            elif choice == 2:
                keyword = non_empty_input("Search keyword: ")
                results = self.ffcs.search_courses(keyword)
                if not results:
                    print("No matching courses found.")
                for c in results:
                    print(c)
            elif choice == 3:
                code = non_empty_input("Enter course code to register: ").upper()
                ok, msg = self.ffcs.register(student.person_id, code)
                print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 4:
                code = non_empty_input("Enter course code to drop: ").upper()
                ok, msg = self.ffcs.drop(student.person_id, code)
                print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 5:
                for c in self.ffcs.student_courses(student.person_id):
                    print(c)
            elif choice == 6:
                break

    def _student_timetable(self, student):
        sub_header("TIMETABLE")
        courses = self.ffcs.student_courses(student.person_id)
        if not courses:
            print("No timetable available. Register for courses first.")
            return
        days = ["MON", "TUE", "WED", "THU", "FRI"]
        print(f"{'Day':6}{'Slot':6}{'Course':10}{'Faculty':20}{'Room':8}")
        for i, c in enumerate(courses):
            day = days[i % len(days)]
            print(f"{day:6}{c.slot:6}{c.course_code:10}{c.faculty_name[:19]:20}{c.room:8}")

    def _student_examinations(self, student):
        sub_header("EXAMINATIONS")
        courses = self.ffcs.student_courses(student.person_id)
        codes = [c.course_code for c in courses]
        exams = [e for e in self.fm.load_data(FILES["exams"]) if e["course_code"] in codes]
        marks = {m["course_code"]: m for m in
                 self.fm.find_all(FILES["marks"], "student_id", student.person_id)}
        if not exams:
            print("No examinations scheduled.")
            return
        print(f"{'Course':10}{'Type':8}{'Date':12}{'Marks':>8}{'Grade':>7}")
        for e in exams:
            m = marks.get(e["course_code"])
            mark_display = "-"
            grade_display = "-"
            if m:
                key_map = {"CAT-1": "cat1", "CAT-2": "cat2", "FAT": "fat"}
                mark_display = str(m.get(key_map.get(e["exam_type"], ""), "-"))
                grade_display = m["grade"]
            print(f"{e['course_code']:10}{e['exam_type']:8}{e['date']:12}"
                  f"{mark_display:>8}{grade_display:>7}")
        print("\n--- GPA / CGPA Calculator ---")
        if input("Compute now? (y/n): ").strip().lower() == "y":
            self._student_academic_performance(student)

    def _student_fees(self, student):
        sub_header("FEES")
        record = self.fee_mgr.get_fee_record(student.person_id)
        if not record:
            print("No fee record found.")
            return
        total = self.fee_mgr.total_due(record)
        pending = total - record["paid_amount"]
        print(f"Tuition Fee    : Rs.{record['tuition_fee']:.2f}")
        print(f"Hostel Fee     : Rs.{record['hostel_fee']:.2f}")
        print(f"Transport Fee  : Rs.{record['transport_fee']:.2f}")
        print(f"Library Fine   : Rs.{record['library_fine']:.2f}")
        print(f"Other Charges  : Rs.{record['other_charges']:.2f}")
        print(f"Total Amount   : Rs.{total:.2f}")
        print(f"Paid Amount    : Rs.{record['paid_amount']:.2f}")
        print(f"Pending Amount : Rs.{pending:.2f}")
        print(f"Status         : {self.fee_mgr.status(record)}")
        if pending > 0 and input("Make a payment now? (y/n): ").strip().lower() == "y":
            amount = safe_float_input("Enter amount to pay: Rs.", minimum=0.01)
            ok, msg = self.fee_mgr.pay(student.person_id, amount)
            print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            if ok:
                print("--- Fee Receipt ---")
                print(f"Student   : {student.name} ({student.registration_number})")
                print(f"Amount    : Rs.{amount:.2f}")
                print(f"Date      : {datetime.now().date()}")

    def _student_hostel(self, student):
        sub_header("HOSTEL")
        allocation = self.hostel_mgr.find_allocation(student.person_id)
        if allocation:
            print(f"Block       : {allocation['block']}")
            print(f"Room No.    : {allocation['room_no']}")
            print(f"Room Type   : {allocation['room_type']}")
            print("Mess Status : Active")
            print("Hostel Fee  : Included in overall fee record")
            if input("Register a complaint? (y/n): ").strip().lower() == "y":
                complaint = non_empty_input("Describe the issue: ")
                print(f"[LOGGED] Complaint registered: '{complaint}'. "
                      f"Warden will address it shortly.")
        else:
            print("You do not currently have a hostel allocation.")

    def _student_transport(self, student):
        sub_header("TRANSPORT")
        route = self.transport_mgr.find_assignment(student.person_id)
        if route:
            print(f"Bus Route     : {route['route_name']}")
            print(f"Bus Number    : {route['bus_number']}")
            print(f"Pickup Point  : {route['pickup_point']}")
            print(f"Pickup Time   : {route['pickup_time']}")
            print(f"Drop Time     : {route['drop_time']}")
            print(f"Transport Fee : Rs.{route['fee']}")
        else:
            print("No transport route assigned.")

    def _student_library(self, student):
        while True:
            sub_header("LIBRARY")
            print("1. Search Books")
            print("2. View Available Books")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. My Borrowed Books")
            print("6. Back")
            choice = safe_int_input("Enter choice: ", 1, 6)
            if choice == 1:
                keyword = non_empty_input("Search keyword: ")
                for b in self.library_mgr.search_books(keyword):
                    print(f"{b['book_id']} | {b['title']} by {b['author']} "
                          f"| Available: {b['available_copies']}/{b['total_copies']}")
            elif choice == 2:
                for b in self.library_mgr.list_books():
                    print(f"{b['book_id']} | {b['title']} by {b['author']} "
                          f"| Available: {b['available_copies']}/{b['total_copies']}")
            elif choice == 3:
                book_id = non_empty_input("Enter Book ID to borrow: ").upper()
                ok, msg = self.library_mgr.borrow(student.person_id, book_id)
                print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 4:
                borrowed = self.library_mgr.borrowed_by(student.person_id)
                if not borrowed:
                    print("You have no borrowed books.")
                    continue
                for t in borrowed:
                    fine_preview = self.library_mgr.calculate_fine(t)
                    print(f"{t['txn_id']} | {t['title']} | Due: {t['due_date']} "
                          f"| Current Fine: Rs.{fine_preview}")
                txn_id = non_empty_input("Enter Transaction ID to return: ").upper()
                ok, msg = self.library_mgr.return_book(student.person_id, txn_id)
                print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 5:
                borrowed = self.library_mgr.borrowed_by(student.person_id)
                if not borrowed:
                    print("You have no borrowed books.")
                for t in borrowed:
                    print(f"{t['txn_id']} | {t['title']} | Due: {t['due_date']}")
            elif choice == 6:
                break

    def _student_leave(self, student):
        while True:
            sub_header("LEAVE MANAGEMENT")
            print("1. Apply for Leave")
            print("2. View My Leave Applications")
            print("3. Back")
            choice = safe_int_input("Enter choice: ", 1, 3)
            if choice == 1:
                leave_type = non_empty_input("Leave type (Medical/Personal/Other): ")
                start = non_empty_input("Start date (YYYY-MM-DD): ")
                end = non_empty_input("End date (YYYY-MM-DD): ")
                reason = non_empty_input("Reason: ")
                record = {
                    "leave_id": generate_id("LV"), "student_id": student.person_id,
                    "leave_type": leave_type, "start_date": start, "end_date": end,
                    "reason": reason, "status": "PENDING",
                }
                self.fm.add_record(FILES["leaves"], record)
                print("[SUCCESS] Leave application submitted.")
            elif choice == 2:
                mine = self.fm.find_all(FILES["leaves"], "student_id", student.person_id)
                if not mine:
                    print("No leave applications found.")
                for lv in mine:
                    print(f"{lv['leave_id']} | {lv['leave_type']} | {lv['start_date']} "
                          f"to {lv['end_date']} | Status: {lv['status']}")
            elif choice == 3:
                break

    def _student_clubs(self, student):
        while True:
            sub_header("CLUBS AND ACTIVITIES")
            print("1. View Clubs")
            print("2. Join a Club")
            print("3. Leave a Club")
            print("4. View My Participation")
            print("5. Back")
            choice = safe_int_input("Enter choice: ", 1, 5)
            clubs = self.fm.load_data(FILES["clubs"])
            if choice == 1:
                for c in clubs:
                    print(f"{c['club_id']} | {c['club_name']} | Members: {len(c['members'])}")
                    for ev in c["events"]:
                        print(f"    Event: {ev['event_name']} on {ev['date']}")
            elif choice == 2:
                club_id = non_empty_input("Enter Club ID to join: ").upper()
                found = False
                for c in clubs:
                    if c["club_id"] == club_id:
                        found = True
                        if student.person_id in c["members"]:
                            print("[ERROR] Already a member.")
                        else:
                            c["members"].append(student.person_id)
                            self.fm.save_data(FILES["clubs"], clubs)
                            print(f"[SUCCESS] Joined {c['club_name']}.")
                if not found:
                    print("[ERROR] Club not found.")
            elif choice == 3:
                club_id = non_empty_input("Enter Club ID to leave: ").upper()
                found = False
                for c in clubs:
                    if c["club_id"] == club_id:
                        found = True
                        if student.person_id not in c["members"]:
                            print("[ERROR] You are not a member of this club.")
                        else:
                            c["members"].remove(student.person_id)
                            self.fm.save_data(FILES["clubs"], clubs)
                            print(f"[SUCCESS] Left {c['club_name']}.")
                if not found:
                    print("[ERROR] Club not found.")
            elif choice == 4:
                joined = [c for c in clubs if student.person_id in c["members"]]
                if not joined:
                    print("You have not joined any clubs.")
                for c in joined:
                    print(f"{c['club_name']} - {len(c['events'])} upcoming event(s)")
            elif choice == 5:
                break

    def _student_placements(self, student):
        while True:
            sub_header("PLACEMENTS")
            print("1. View Placement Profile")
            print("2. View Eligible Companies")
            print("3. Apply to a Company")
            print("4. View My Applications")
            print("5. Back")
            choice = safe_int_input("Enter choice: ", 1, 5)
            if choice == 1:
                print(f"Name        : {student.name}")
                print(f"CGPA        : {student.cgpa}")
                print(f"Resume Status: Submitted")
                print(f"Skills      : Python, Data Structures, Communication")
            elif choice == 2:
                eligible = self.placement_mgr.eligible_companies(student.cgpa)
                if not eligible:
                    print("No companies match your current CGPA.")
                for c in eligible:
                    print(f"{c['company_id']} | {c['company_name']} | {c['role_title']} "
                          f"| Min CGPA: {c['min_cgpa']} | Package: {c['package_lpa']} LPA")
            elif choice == 3:
                company_id = non_empty_input("Enter Company ID to apply: ").upper()
                company = next((c for c in self.placement_mgr.list_companies()
                                if c["company_id"] == company_id), None)
                if not company:
                    print("[ERROR] Company not found.")
                elif student.cgpa < company["min_cgpa"]:
                    print(f"[ERROR] You do not meet the minimum CGPA of {company['min_cgpa']}.")
                else:
                    ok, msg = self.placement_mgr.apply(student.person_id, company_id)
                    print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 4:
                apps = self.placement_mgr.student_applications(student.person_id)
                if not apps:
                    print("No applications submitted yet.")
                for a in apps:
                    print(f"{a['application_id']} | Company: {a['company_id']} "
                          f"| Status: {a['status']}")
            elif choice == 5:
                break

    def _show_notices(self):
        sub_header("NOTICES")
        notices = self.fm.load_data(FILES["notices"])
        if not notices:
            print("No notices available.")
            return
        for cat in ["Academic", "Examination", "Placement", "General"]:
            relevant = [n for n in notices if n["category"] == cat]
            if relevant:
                print(f"\n-- {cat} --")
                for n in relevant:
                    print(f"[{n['date']}] {n['title']}")
                    print(textwrap.indent(textwrap.fill(n["content"], 55), "    "))

    # ---------------- FACULTY SESSION ----------------

    def _faculty_session(self, faculty: Faculty):
        while True:
            header("FACULTY DASHBOARD")
            menu = faculty.dashboard_menu()
            for i, item in enumerate(menu, start=1):
                print(f"{i}. {item}")
            choice = safe_int_input("Enter choice: ", 1, len(menu))
            action = menu[choice - 1]

            if action == "Profile":
                faculty.display_profile()
            elif action == "My Courses":
                self._faculty_courses(faculty)
            elif action == "Timetable":
                self._faculty_timetable(faculty)
            elif action == "Students":
                self._faculty_students(faculty)
            elif action == "Attendance":
                self._faculty_attendance(faculty)
            elif action == "Marks":
                self._faculty_marks(faculty)
            elif action == "Leave Requests":
                self._faculty_leave_requests(faculty)
            elif action == "Notices":
                self._faculty_notices(faculty)
            elif action == "Course Statistics":
                self._faculty_statistics(faculty)
            elif action == "Logout":
                print("Logged out successfully.")
                break
            pause()

    def _faculty_course_list(self, faculty):
        return [c for c in self.ffcs.list_courses() if c.faculty_id == faculty.person_id]

    def _faculty_courses(self, faculty):
        sub_header("MY COURSES")
        courses = self._faculty_course_list(faculty)
        if not courses:
            print("No courses assigned.")
        for c in courses:
            print(c)

    def _faculty_timetable(self, faculty):
        sub_header("TIMETABLE")
        courses = self._faculty_course_list(faculty)
        days = ["MON", "TUE", "WED", "THU", "FRI"]
        for i, c in enumerate(courses):
            print(f"{days[i % len(days)]:6}{c.slot:6}{c.course_code:10}{c.room:8}")

    def _select_faculty_course(self, faculty):
        courses = self._faculty_course_list(faculty)
        if not courses:
            print("You have no assigned courses.")
            return None
        for c in courses:
            print(c)
        code = non_empty_input("Enter course code: ").upper()
        course = next((c for c in courses if c.course_code == code), None)
        if not course:
            print("[ERROR] Invalid course code for this faculty.")
        return course

    def _faculty_students(self, faculty):
        sub_header("STUDENT LIST")
        course = self._select_faculty_course(faculty)
        if not course:
            return
        for sid in course.registered_students:
            s = self._load_student(sid)
            if s:
                print(f"{s.person_id} | {s.name} | {s.registration_number} | Sec {s.section}")

    def _faculty_attendance(self, faculty):
        sub_header("MARK / UPDATE ATTENDANCE")
        course = self._select_faculty_course(faculty)
        if not course:
            return
        date_str = non_empty_input("Enter date (YYYY-MM-DD): ")
        for sid in course.registered_students:
            s = self._load_student(sid)
            if not s:
                continue
            status_input = non_empty_input(f"{s.name} ({sid}) - Present/Absent [P/A]: ").upper()
            status = "Present" if status_input.startswith("P") else "Absent"
            self.attendance_mgr.mark_attendance(course.course_code, sid, date_str, status)
        print("[SUCCESS] Attendance recorded for the class.")
        print("Recalculating percentages...")
        for sid in course.registered_students:
            _, _, pct = self.attendance_mgr.course_attendance_for_student(sid, course.course_code)
            print(f"  {sid}: {pct}%")

    def _faculty_marks(self, faculty):
        sub_header("ENTER / UPDATE MARKS")
        course = self._select_faculty_course(faculty)
        if not course:
            return
        exam_options = {"1": "CAT-1", "2": "CAT-2", "3": "FAT", "4": "Continuous Assessment"}
        print("1. CAT-1  2. CAT-2  3. FAT  4. Continuous Assessment")
        choice = input("Select component to enter: ").strip()
        component = exam_options.get(choice)
        if not component:
            print("[ERROR] Invalid selection.")
            return
        marks_data = self.fm.load_data(FILES["marks"])
        for sid in course.registered_students:
            s = self._load_student(sid)
            if not s:
                continue
            score = safe_float_input(f"{s.name} - {component} marks (0-100): ", 0, 100)
            record = next((m for m in marks_data if m["student_id"] == sid
                           and m["course_code"] == course.course_code), None)
            if not record:
                record = {"student_id": sid, "course_code": course.course_code,
                          "cat1": 0, "cat2": 0, "fat": 0, "ca": 0,
                          "total": 0, "grade": "F", "grade_point": 0}
                marks_data.append(record)
            key_map = {"CAT-1": "cat1", "CAT-2": "cat2", "FAT": "fat",
                      "Continuous Assessment": "ca"}
            record[key_map[component]] = score
            total = self.grade_calc.compute_total(record["cat1"], record["cat2"],
                                                   record["fat"], record["ca"])
            letter, points = self.grade_calc.marks_to_grade(total)
            record["total"], record["grade"], record["grade_point"] = total, letter, points
        self.fm.save_data(FILES["marks"], marks_data)
        print("[SUCCESS] Marks updated and grades recalculated.")

    def _faculty_leave_requests(self, faculty):
        sub_header("STUDENT LEAVE REQUESTS")
        leaves = [lv for lv in self.fm.load_data(FILES["leaves"]) if lv["status"] == "PENDING"]
        if not leaves:
            print("No pending leave requests.")
            return
        for lv in leaves:
            s = self._load_student(lv["student_id"])
            name = s.name if s else lv["student_id"]
            print(f"{lv['leave_id']} | {name} | {lv['leave_type']} | "
                  f"{lv['start_date']} to {lv['end_date']} | Reason: {lv['reason']}")
        leave_id = non_empty_input("Enter Leave ID to act on (or blank to skip): ").upper()
        if not leave_id:
            return
        decision = non_empty_input("Approve or Reject (A/R): ").upper()
        status = "APPROVED" if decision.startswith("A") else "REJECTED"
        ok = self.fm.update_record(FILES["leaves"], "leave_id", leave_id, {"status": status})
        print("[SUCCESS] Leave updated." if ok else "[ERROR] Leave ID not found.")

    def _faculty_notices(self, faculty):
        sub_header("PUBLISH COURSE NOTICE")
        print("1. Publish New Notice")
        print("2. View Notices")
        choice = safe_int_input("Enter choice: ", 1, 2)
        if choice == 1:
            title = non_empty_input("Notice title: ")
            content = non_empty_input("Notice content: ")
            category = non_empty_input("Category (Academic/Examination/General): ")
            self.fm.add_record(FILES["notices"], {
                "notice_id": generate_id("NOT"), "category": category,
                "title": title, "content": content, "date": str(datetime.now().date()),
            })
            print("[SUCCESS] Notice published.")
        else:
            self._show_notices()

    def _faculty_statistics(self, faculty):
        sub_header("COURSE STATISTICS")
        course = self._select_faculty_course(faculty)
        if not course:
            return
        marks = [m["total"] for m in self.fm.load_data(FILES["marks"])
                 if m["course_code"] == course.course_code]
        if not marks:
            print("No marks recorded yet for this course.")
            return
        print(f"Enrolled Students : {len(course.registered_students)}")
        print(f"Average Marks     : {round(statistics.mean(marks), 2)}")
        print(f"Highest Marks     : {max(marks)}")
        print(f"Lowest Marks      : {min(marks)}")
        low_attendance = self.attendance_mgr.low_attendance_students(
            course.course_code, course.registered_students)
        if low_attendance:
            print("\nStudents with LOW attendance:")
            for sid, pct in low_attendance:
                s = self._load_student(sid)
                name = s.name if s else sid
                print(f"  {name} ({sid}): {pct}%")
        else:
            print("\nNo students currently below the attendance threshold.")

    # ---------------- ADMIN SESSION ----------------

    def _admin_session(self, admin: Administrator):
        while True:
            header("ADMINISTRATOR DASHBOARD")
            menu = admin.dashboard_menu()
            for i, item in enumerate(menu, start=1):
                print(f"{i}. {item}")
            choice = safe_int_input("Enter choice: ", 1, len(menu))
            action = menu[choice - 1]

            if action == "Student Management":
                self._admin_student_mgmt()
            elif action == "Faculty Management":
                self._admin_faculty_mgmt()
            elif action == "Course Management":
                self._admin_course_mgmt()
            elif action == "FFCS Management":
                self._admin_ffcs_mgmt()
            elif action == "Examination Management":
                self._admin_exam_mgmt()
            elif action == "Fee Management":
                self._admin_fee_mgmt()
            elif action == "Hostel Management":
                self._admin_hostel_mgmt()
            elif action == "Transport Management":
                self._admin_transport_mgmt()
            elif action == "Library Management":
                self._admin_library_mgmt()
            elif action == "Club Management":
                self._admin_club_mgmt()
            elif action == "Placement Management":
                self._admin_placement_mgmt()
            elif action == "Notice Management":
                self._admin_notice_mgmt()
            elif action == "System Statistics":
                self._admin_statistics()
            elif action == "Logout":
                print("Logged out successfully.")
                break
            pause()

    def _admin_student_mgmt(self):
        while True:
            sub_header("STUDENT MANAGEMENT")
            print("1. Add Student  2. Remove Student  3. Update Student "
                  "4. Search Student  5. View All  6. Back")
            choice = safe_int_input("Enter choice: ", 1, 6)
            if choice == 1:
                name = non_empty_input("Name: ")
                dob = non_empty_input("DOB (YYYY-MM-DD): ")
                gender = non_empty_input("Gender: ")
                email = non_empty_input("Email: ")
                if not Person.is_valid_email(email):
                    print("[ERROR] Invalid email format.")
                    continue
                phone = non_empty_input("Phone: ")
                address = non_empty_input("Address: ")
                reg_no = non_empty_input("Registration Number: ")
                school = non_empty_input("School: ")
                program = non_empty_input("Program: ")
                campus = non_empty_input("Campus: ")
                semester = safe_int_input("Semester: ", 1, 8)
                batch = non_empty_input("Batch (e.g. 2024-2028): ")
                section = non_empty_input("Section: ")
                student = Student(generate_id("STU"), name, dob, gender, email,
                                  phone, address, reg_no, school, program, campus,
                                  semester, batch, section)
                self.fm.add_record(FILES["students"], student.to_dict())
                username = non_empty_input("Set login username: ")
                password = non_empty_input("Set login password: ")
                ok, msg = self.auth.register_user(username, password, "Student", student.person_id)
                print(f"[{'SUCCESS' if ok else 'ERROR'}] Student added. {msg}")
            elif choice == 2:
                sid = non_empty_input("Enter Student ID to remove: ").upper()
                ok = self.fm.delete_record(FILES["students"], "person_id", sid)
                print("[SUCCESS] Student removed." if ok else "[ERROR] Student not found.")
            elif choice == 3:
                sid = non_empty_input("Enter Student ID to update: ").upper()
                s = self._load_student(sid)
                if not s:
                    print("[ERROR] Student not found.")
                    continue
                field = non_empty_input("Field to update (name/email/phone/semester/section): ").lower()
                if field not in {"name", "email", "phone", "semester", "section"}:
                    print("[ERROR] Unsupported field.")
                    continue
                value = non_empty_input(f"New value for {field}: ")
                if field == "semester":
                    try:
                        value = int(value)
                    except ValueError:
                        print("[ERROR] Semester must be numeric.")
                        continue
                self.fm.update_record(FILES["students"], "person_id", sid, {field: value})
                print("[SUCCESS] Student updated.")
            elif choice == 4:
                keyword = non_empty_input("Search by name or reg number: ").lower()
                matches = [s for s in self.fm.load_data(FILES["students"])
                          if keyword in s["name"].lower()
                          or keyword in s["registration_number"].lower()]
                for m in matches:
                    print(f"{m['person_id']} | {m['name']} | {m['registration_number']} "
                          f"| Sem {m['semester']} | Sec {m['section']}")
                if not matches:
                    print("No matches found.")
            elif choice == 5:
                for s in self.fm.load_data(FILES["students"]):
                    print(f"{s['person_id']} | {s['name']} | {s['registration_number']} "
                          f"| CGPA {s['cgpa']}")
            elif choice == 6:
                break

    def _admin_faculty_mgmt(self):
        while True:
            sub_header("FACULTY MANAGEMENT")
            print("1. Add Faculty  2. Remove Faculty  3. Update Faculty "
                  "4. Search Faculty  5. View All  6. Back")
            choice = safe_int_input("Enter choice: ", 1, 6)
            if choice == 1:
                name = non_empty_input("Name: ")
                dob = non_empty_input("DOB (YYYY-MM-DD): ")
                gender = non_empty_input("Gender: ")
                email = non_empty_input("Email: ")
                phone = non_empty_input("Phone: ")
                address = non_empty_input("Address: ")
                emp_id = non_empty_input("Employee ID: ")
                school = non_empty_input("School: ")
                designation = non_empty_input("Designation: ")
                specialization = non_empty_input("Specialization: ")
                fac = Faculty(generate_id("FAC"), name, dob, gender, email, phone,
                             address, emp_id, school, designation, specialization)
                self.fm.add_record(FILES["faculty"], fac.to_dict())
                username = non_empty_input("Set login username: ")
                password = non_empty_input("Set login password: ")
                ok, msg = self.auth.register_user(username, password, "Faculty", fac.person_id)
                print(f"[{'SUCCESS' if ok else 'ERROR'}] Faculty added. {msg}")
            elif choice == 2:
                fid = non_empty_input("Enter Faculty ID to remove: ").upper()
                ok = self.fm.delete_record(FILES["faculty"], "person_id", fid)
                print("[SUCCESS] Faculty removed." if ok else "[ERROR] Faculty not found.")
            elif choice == 3:
                fid = non_empty_input("Enter Faculty ID to update: ").upper()
                f = self._load_faculty(fid)
                if not f:
                    print("[ERROR] Faculty not found.")
                    continue
                field = non_empty_input("Field to update (name/email/phone/designation): ").lower()
                if field not in {"name", "email", "phone", "designation"}:
                    print("[ERROR] Unsupported field.")
                    continue
                value = non_empty_input(f"New value for {field}: ")
                self.fm.update_record(FILES["faculty"], "person_id", fid, {field: value})
                print("[SUCCESS] Faculty updated.")
            elif choice == 4:
                keyword = non_empty_input("Search by name or employee ID: ").lower()
                matches = [f for f in self.fm.load_data(FILES["faculty"])
                          if keyword in f["name"].lower() or keyword in f["employee_id"].lower()]
                for m in matches:
                    print(f"{m['person_id']} | {m['name']} | {m['employee_id']} | {m['designation']}")
                if not matches:
                    print("No matches found.")
            elif choice == 5:
                for f in self.fm.load_data(FILES["faculty"]):
                    print(f"{f['person_id']} | {f['name']} | {f['designation']} | {f['school']}")
            elif choice == 6:
                break

    def _admin_course_mgmt(self):
        while True:
            sub_header("COURSE MANAGEMENT")
            print("1. Add Course  2. Remove Course  3. Update Course "
                  "4. Assign Faculty  5. View All  6. Back")
            choice = safe_int_input("Enter choice: ", 1, 6)
            if choice == 1:
                code = non_empty_input("Course Code: ").upper()
                if self.ffcs.find_course(code):
                    print("[ERROR] Course code already exists.")
                    continue
                name = non_empty_input("Course Name: ")
                credits = safe_int_input("Credits: ", 1, 6)
                faculty_list = self.fm.load_data(FILES["faculty"])
                for f in faculty_list:
                    print(f"{f['person_id']} | {f['name']}")
                fac_id = non_empty_input("Assign Faculty ID: ").upper()
                fac = next((f for f in faculty_list if f["person_id"] == fac_id), None)
                if not fac:
                    print("[ERROR] Invalid faculty ID.")
                    continue
                slot = non_empty_input("Slot: ")
                room = non_empty_input("Room: ")
                capacity = safe_int_input("Capacity: ", 1, 200)
                course = Course(code, name, credits, fac["person_id"], fac["name"],
                               slot, room, capacity)
                self.fm.add_record(FILES["courses"], course.to_dict())
                print("[SUCCESS] Course added.")
            elif choice == 2:
                code = non_empty_input("Enter course code to remove: ").upper()
                ok = self.fm.delete_record(FILES["courses"], "course_code", code)
                print("[SUCCESS] Course removed." if ok else "[ERROR] Course not found.")
            elif choice == 3:
                code = non_empty_input("Enter course code to update: ").upper()
                course = self.ffcs.find_course(code)
                if not course:
                    print("[ERROR] Course not found.")
                    continue
                field = non_empty_input("Field to update (course_name/credits/room/capacity): ").lower()
                if field not in {"course_name", "credits", "room", "capacity"}:
                    print("[ERROR] Unsupported field.")
                    continue
                value = non_empty_input(f"New value for {field}: ")
                if field in {"credits", "capacity"}:
                    try:
                        value = int(value)
                    except ValueError:
                        print("[ERROR] Must be numeric.")
                        continue
                self.fm.update_record(FILES["courses"], "course_code", code, {field: value})
                print("[SUCCESS] Course updated.")
            elif choice == 4:
                code = non_empty_input("Enter course code: ").upper()
                course = self.ffcs.find_course(code)
                if not course:
                    print("[ERROR] Course not found.")
                    continue
                fac_id = non_empty_input("Enter new Faculty ID: ").upper()
                fac = self._load_faculty(fac_id)
                if not fac:
                    print("[ERROR] Invalid faculty ID.")
                    continue
                self.fm.update_record(FILES["courses"], "course_code", code,
                                      {"faculty_id": fac.person_id, "faculty_name": fac.name})
                print("[SUCCESS] Faculty reassigned.")
            elif choice == 5:
                for c in self.ffcs.list_courses():
                    print(c)
            elif choice == 6:
                break

    def _admin_ffcs_mgmt(self):
        while True:
            sub_header("FFCS MANAGEMENT")
            status = "OPEN" if self.settings.get("ffcs_registration_open") else "CLOSED"
            print(f"Current status: {status}")
            print("1. Open Registration  2. Close Registration "
                  "3. View Registrations  4. Drop a Registration  5. Back")
            choice = safe_int_input("Enter choice: ", 1, 5)
            if choice == 1:
                self.settings["ffcs_registration_open"] = True
                self.fm.save_data(FILES["settings"], self.settings)
                print("[SUCCESS] FFCS registration opened.")
            elif choice == 2:
                self.settings["ffcs_registration_open"] = False
                self.fm.save_data(FILES["settings"], self.settings)
                print("[SUCCESS] FFCS registration closed.")
            elif choice == 3:
                for e in self.fm.load_data(FILES["enrollments"]):
                    print(f"{e['enrollment_id']} | {e['student_id']} | {e['course_code']} "
                          f"| {e['status']}")
            elif choice == 4:
                sid = non_empty_input("Student ID: ").upper()
                code = non_empty_input("Course Code: ").upper()
                ok, msg = self.ffcs.drop(sid, code)
                print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 5:
                break

    def _admin_exam_mgmt(self):
        while True:
            sub_header("EXAMINATION MANAGEMENT")
            print("1. Create Exam  2. Update Exam  3. View Exam Schedule  4. Back")
            choice = safe_int_input("Enter choice: ", 1, 4)
            if choice == 1:
                code = non_empty_input("Course code: ").upper()
                if not self.ffcs.find_course(code):
                    print("[ERROR] Invalid course code.")
                    continue
                exam_type = non_empty_input("Exam type (CAT-1/CAT-2/FAT): ")
                date_str = non_empty_input("Date (YYYY-MM-DD): ")
                self.fm.add_record(FILES["exams"], {
                    "exam_id": generate_id("EXM"), "course_code": code,
                    "exam_type": exam_type, "date": date_str, "max_marks": 100,
                })
                print("[SUCCESS] Exam created.")
            elif choice == 2:
                exam_id = non_empty_input("Exam ID to update: ").upper()
                date_str = non_empty_input("New date (YYYY-MM-DD): ")
                ok = self.fm.update_record(FILES["exams"], "exam_id", exam_id, {"date": date_str})
                print("[SUCCESS] Exam updated." if ok else "[ERROR] Exam not found.")
            elif choice == 3:
                for e in self.fm.load_data(FILES["exams"]):
                    print(f"{e['exam_id']} | {e['course_code']} | {e['exam_type']} | {e['date']}")
            elif choice == 4:
                break

    def _admin_fee_mgmt(self):
        while True:
            sub_header("FEE MANAGEMENT")
            print("1. Add Fee Record  2. Record Payment  3. View Pending Fees  4. Back")
            choice = safe_int_input("Enter choice: ", 1, 4)
            if choice == 1:
                sid = non_empty_input("Student ID: ").upper()
                if not self._load_student(sid):
                    print("[ERROR] Student not found.")
                    continue
                tuition = safe_float_input("Tuition Fee: ", 0)
                hostel = safe_float_input("Hostel Fee: ", 0)
                transport = safe_float_input("Transport Fee: ", 0)
                self.fee_mgr.create_fee_record(sid, tuition, hostel, transport)
                print("[SUCCESS] Fee record created.")
            elif choice == 2:
                sid = non_empty_input("Student ID: ").upper()
                amount = safe_float_input("Amount: Rs.", 0.01)
                ok, msg = self.fee_mgr.pay(sid, amount)
                print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 3:
                for r in self.fm.load_data(FILES["fees"]):
                    pending = self.fee_mgr.total_due(r) - r["paid_amount"]
                    if pending > 0:
                        print(f"{r['student_id']} | Pending: Rs.{pending:.2f} "
                              f"| Status: {self.fee_mgr.status(r)}")
            elif choice == 4:
                break

    def _admin_hostel_mgmt(self):
        while True:
            sub_header("HOSTEL MANAGEMENT")
            print("1. Add Hostel Room  2. Allocate Room  3. Vacate Room  "
                  "4. View Occupancy  5. Back")
            choice = safe_int_input("Enter choice: ", 1, 5)
            if choice == 1:
                block = non_empty_input("Block: ")
                room_no = non_empty_input("Room Number: ")
                room_type = non_empty_input("Room Type (Single/Double/Triple): ")
                capacity = safe_int_input("Capacity: ", 1, 5)
                self.hostel_mgr.add_room(block, room_no, room_type, capacity)
                print("[SUCCESS] Room added.")
            elif choice == 2:
                sid = non_empty_input("Student ID: ").upper()
                if not self._load_student(sid):
                    print("[ERROR] Student not found.")
                    continue
                for r in self.hostel_mgr.list_rooms():
                    print(f"{r['room_id']} | {r['block']}-{r['room_no']} "
                          f"| {len(r['occupants'])}/{r['capacity']}")
                room_id = non_empty_input("Room ID: ").upper()
                ok, msg = self.hostel_mgr.allocate(sid, room_id)
                print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 3:
                sid = non_empty_input("Student ID: ").upper()
                room_id = non_empty_input("Room ID: ").upper()
                ok, msg = self.hostel_mgr.vacate(sid, room_id)
                print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 4:
                occ, cap = self.hostel_mgr.occupancy_stats()
                pct = round((occ / cap) * 100, 2) if cap else 0
                print(f"Occupied: {occ}/{cap} ({pct}%)")
            elif choice == 5:
                break

    def _admin_transport_mgmt(self):
        while True:
            sub_header("TRANSPORT MANAGEMENT")
            print("1. Add Bus Route  2. Assign Student to Route  3. View Routes  4. Back")
            choice = safe_int_input("Enter choice: ", 1, 4)
            if choice == 1:
                bus_number = non_empty_input("Bus Number: ")
                route_name = non_empty_input("Route Name: ")
                pickup_point = non_empty_input("Pickup Point: ")
                pickup_time = non_empty_input("Pickup Time: ")
                drop_time = non_empty_input("Drop Time: ")
                fee = safe_float_input("Fee: ", 0)
                self.transport_mgr.add_route(bus_number, route_name, pickup_point,
                                            pickup_time, drop_time, fee)
                print("[SUCCESS] Route added.")
            elif choice == 2:
                sid = non_empty_input("Student ID: ").upper()
                if not self._load_student(sid):
                    print("[ERROR] Student not found.")
                    continue
                for r in self.transport_mgr.list_routes():
                    print(f"{r['route_id']} | {r['route_name']} | {r['bus_number']}")
                route_id = non_empty_input("Route ID: ").upper()
                ok, msg = self.transport_mgr.assign_student(sid, route_id)
                print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 3:
                for r in self.transport_mgr.list_routes():
                    print(f"{r['route_id']} | {r['route_name']} | {r['bus_number']} "
                          f"| Riders: {len(r['assigned_students'])}")
            elif choice == 4:
                break

    def _admin_library_mgmt(self):
        while True:
            sub_header("LIBRARY MANAGEMENT")
            print("1. Add Book  2. Remove Book  3. Search Book  4. Issue Book  "
                  "5. Return Book  6. Calculate Fine  7. Back")
            choice = safe_int_input("Enter choice: ", 1, 7)
            if choice == 1:
                title = non_empty_input("Title: ")
                author = non_empty_input("Author: ")
                isbn = non_empty_input("ISBN: ")
                copies = safe_int_input("Number of Copies: ", 1, 500)
                self.library_mgr.add_book(title, author, isbn, copies)
                print("[SUCCESS] Book added.")
            elif choice == 2:
                book_id = non_empty_input("Book ID to remove: ").upper()
                ok = self.fm.delete_record(FILES["books"], "book_id", book_id)
                print("[SUCCESS] Book removed." if ok else "[ERROR] Book not found.")
            elif choice == 3:
                keyword = non_empty_input("Search keyword: ")
                for b in self.library_mgr.search_books(keyword):
                    print(f"{b['book_id']} | {b['title']} | {b['author']}")
            elif choice == 4:
                sid = non_empty_input("Student ID: ").upper()
                book_id = non_empty_input("Book ID: ").upper()
                ok, msg = self.library_mgr.borrow(sid, book_id)
                print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 5:
                sid = non_empty_input("Student ID: ").upper()
                txn_id = non_empty_input("Transaction ID: ").upper()
                ok, msg = self.library_mgr.return_book(sid, txn_id)
                print(("[SUCCESS] " if ok else "[ERROR] ") + msg)
            elif choice == 6:
                txn_id = non_empty_input("Transaction ID: ").upper()
                txn = self.fm.find_one(FILES["library_transactions"], "txn_id", txn_id)
                if txn:
                    print(f"Fine: Rs.{self.library_mgr.calculate_fine(txn)}")
                else:
                    print("[ERROR] Transaction not found.")
            elif choice == 7:
                break

    def _admin_club_mgmt(self):
        while True:
            sub_header("CLUB MANAGEMENT")
            print("1. Add Club  2. Remove Club  3. Add Event  4. View Members  5. Back")
            choice = safe_int_input("Enter choice: ", 1, 5)
            clubs = self.fm.load_data(FILES["clubs"])
            if choice == 1:
                name = non_empty_input("Club Name: ")
                self.fm.add_record(FILES["clubs"], {
                    "club_id": generate_id("CLB"), "club_name": name,
                    "members": [], "events": [],
                })
                print("[SUCCESS] Club added.")
            elif choice == 2:
                club_id = non_empty_input("Club ID to remove: ").upper()
                ok = self.fm.delete_record(FILES["clubs"], "club_id", club_id)
                print("[SUCCESS] Club removed." if ok else "[ERROR] Club not found.")
            elif choice == 3:
                club_id = non_empty_input("Club ID: ").upper()
                club = next((c for c in clubs if c["club_id"] == club_id), None)
                if not club:
                    print("[ERROR] Club not found.")
                    continue
                event_name = non_empty_input("Event Name: ")
                date_str = non_empty_input("Event Date (YYYY-MM-DD): ")
                club["events"].append({"event_id": generate_id("EVT"),
                                       "event_name": event_name, "date": date_str})
                self.fm.save_data(FILES["clubs"], clubs)
                print("[SUCCESS] Event added.")
            elif choice == 4:
                club_id = non_empty_input("Club ID: ").upper()
                club = next((c for c in clubs if c["club_id"] == club_id), None)
                if not club:
                    print("[ERROR] Club not found.")
                    continue
                for mid in club["members"]:
                    s = self._load_student(mid)
                    print(f"{mid} - {s.name if s else 'Unknown'}")
            elif choice == 5:
                break

    def _admin_placement_mgmt(self):
        while True:
            sub_header("PLACEMENT MANAGEMENT")
            print("1. Add Company  2. Set Eligibility  3. View Applications  "
                  "4. Update Application Status  5. Back")
            choice = safe_int_input("Enter choice: ", 1, 5)
            if choice == 1:
                name = non_empty_input("Company Name: ")
                role_title = non_empty_input("Role Title: ")
                min_cgpa = safe_float_input("Minimum CGPA: ", 0, 10)
                package = safe_float_input("Package (LPA): ", 0)
                self.placement_mgr.add_company(name, role_title, min_cgpa, package)
                print("[SUCCESS] Company added.")
            elif choice == 2:
                company_id = non_empty_input("Company ID: ").upper()
                min_cgpa = safe_float_input("New Minimum CGPA: ", 0, 10)
                ok = self.fm.update_record(FILES["placements"], "company_id", company_id,
                                          {"min_cgpa": min_cgpa})
                print("[SUCCESS] Eligibility updated." if ok else "[ERROR] Company not found.")
            elif choice == 3:
                apps_file = FILES.get("placement_applications", "placement_applications.json")
                for a in self.fm.load_data(apps_file):
                    print(f"{a['application_id']} | {a['student_id']} | {a['company_id']} "
                          f"| {a['status']}")
            elif choice == 4:
                app_id = non_empty_input("Application ID: ").upper()
                status = non_empty_input("New Status (SHORTLISTED/REJECTED/SELECTED): ").upper()
                ok = self.placement_mgr.update_status(app_id, status)
                print("[SUCCESS] Status updated." if ok else "[ERROR] Application not found.")
            elif choice == 5:
                break

    def _admin_notice_mgmt(self):
        while True:
            sub_header("NOTICE MANAGEMENT")
            print("1. Create Notice  2. Delete Notice  3. View Notices  4. Back")
            choice = safe_int_input("Enter choice: ", 1, 4)
            if choice == 1:
                title = non_empty_input("Title: ")
                content = non_empty_input("Content: ")
                category = non_empty_input("Category (Academic/Examination/Placement/General): ")
                self.fm.add_record(FILES["notices"], {
                    "notice_id": generate_id("NOT"), "category": category,
                    "title": title, "content": content, "date": str(datetime.now().date()),
                })
                print("[SUCCESS] Notice created.")
            elif choice == 2:
                notice_id = non_empty_input("Notice ID to delete: ").upper()
                ok = self.fm.delete_record(FILES["notices"], "notice_id", notice_id)
                print("[SUCCESS] Notice deleted." if ok else "[ERROR] Notice not found.")
            elif choice == 3:
                self._show_notices()
            elif choice == 4:
                break

    def _admin_statistics(self):
        sub_header("SYSTEM STATISTICS")
        students = self.fm.load_data(FILES["students"])
        faculty = self.fm.load_data(FILES["faculty"])
        courses = self.fm.load_data(FILES["courses"])
        books = self.fm.load_data(FILES["books"])
        occ, cap = self.hostel_mgr.occupancy_stats()
        fees = self.fm.load_data(FILES["fees"])
        apps_file = FILES.get("placement_applications", "placement_applications.json")
        apps = self.fm.load_data(apps_file)

        print(f"Total Students        : {len(students)}")
        print(f"Total Faculty         : {len(faculty)}")
        print(f"Total Courses         : {len(courses)}")
        print(f"Total Books           : {len(books)}")
        occ_pct = round((occ / cap) * 100, 2) if cap else 0
        print(f"Hostel Occupancy      : {occ}/{cap} ({occ_pct}%)")
        if students:
            avg_cgpa = round(statistics.mean(s["cgpa"] for s in students), 2)
            print(f"Average CGPA          : {avg_cgpa}")
        total_fee_collected = sum(f["paid_amount"] for f in fees)
        total_fee_due = sum(self.fee_mgr.total_due(f) for f in fees)
        print(f"Fee Collection        : Rs.{total_fee_collected:.2f} / Rs.{total_fee_due:.2f}")
        print(f"Placement Applications: {len(apps)}")
        selected = len([a for a in apps if a["status"] == "SELECTED"])
        print(f"Students Placed       : {selected}")

    # ---------------- Utility (backup / reset) ----------------

    def backup_data(self):
        backup_dir = f"cms_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        for filename in FILES.values():
            data = self.fm.load_data(filename)
            with open(os.path.join(backup_dir, filename), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        print(f"[SUCCESS] Backup created at ./{backup_dir}/")


# ==================================================================
# ENTRY POINT
# ==================================================================

def main():
    try:
        system = CollegeManagementSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\nSession interrupted. Goodbye!")
    except Exception as exc:  # top-level safety net
        print(f"\n[FATAL ERROR] An unexpected error occurred: {exc}")


if __name__ == "__main__":
    main()
