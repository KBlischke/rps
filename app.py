"""Webanwendung zur Verwaltung von Materiallagern in Bildungseinrichtungen"""

import json
import sqlite3

from flask import Flask, redirect, render_template, request, session
from flask_session import Session

from database import management, users


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


with open("config.json", "r", encoding="utf-8") as file:
    data = json.load(file)

    COMPANY = data["company"]
    COLOR = f"style='background-color: {data['color']};'"
    if data["font_color"] == "Dunkelblau":
        FONT_COLOR = "link-primary"
    elif data["font_color"] == "Grau":
        FONT_COLOR = "link-secondary"
    elif data["font_color"] == "Grün":
        FONT_COLOR = "link-success"
    elif data["font_color"] == "Rot":
        FONT_COLOR = "link-danger"
    elif data["font_color"] == "Gelb":
        FONT_COLOR = "link-warning"
    elif data["font_color"] == "Hellblau":
        FONT_COLOR = "link-info"
    elif data["font_color"] == "Weiß":
        FONT_COLOR = "link-light"
    elif data["font_color"] == "Schwarz":
        FONT_COLOR = "link-dark"


@app.route("/", methods=["GET"])
def index():
    """Begrüßungsseite für den Nutzer"""
    if not session.get("user"):
        return redirect("/login")

    return render_template(
        "index.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
        name=session.get("user"),
    )


@app.route("/buchen", methods=["GET", "POST"])
def book():
    """Seite zur Buchung von Kursen"""
    if not session.get("user"):
        return redirect("/login")

    if request.method == "POST":
        lecturer = None
        lecturer_id = int(request.form.get("lecturer", None))
        for entry in management.get_lecturers():
            if entry["lecturer_id"] == lecturer_id:
                lecturer = f"{entry['last_name']}, {entry['first_name']}"
                break

        course = {}
        course["course_id"] = int(request.form.get("course", None))
        for entry in management.get_courses():
            if entry["course_id"] == course["course_id"]:
                course["course"] = entry["course"]
                course["comment"] = entry["comment"]
                break

        attendents = int(request.form.get("attendents", None))

        materials = management.get_materials()
        requirements = management.get_lecturers_requirements(lecturer_id)
        consumption = []
        for material in materials:
            for requirement in requirements:
                if (
                    requirement["course_id"] == course["course_id"]
                    and requirement["material_id"] == material["material_id"]
                ):
                    consumption.append(
                        {
                            "material_id": material["material_id"],
                            "consumption": (
                                requirement["requirement"] * attendents
                                if requirement["is_static"] == 0
                                else requirement["requirement"]
                            ),
                        }
                    )

        for entry in consumption:
            management.update_materials_amount(
                entry["material_id"], entry["consumption"]
            )

        return render_template(
            "booking/balance.html",
            company=COMPANY,
            color=COLOR,
            font_color=FONT_COLOR,
            lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
            lecturer=lecturer,
            course=course,
            attendents=attendents,
            requirements=sorted(requirements, key=lambda x: x["material"]),
            materials=sorted(materials, key=lambda x: x["material"]),
        )

    return render_template(
        "booking/book.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
        courses=sorted(management.get_courses(), key=lambda x: x["course"]),
    )


@app.route("/dozierenden_kurse", methods=["GET"])
def book_courses():
    """API um alle Kurse eines/einer Dzenten/Dozentin zu erhalten"""
    if not session.get("user"):
        return redirect("/login")

    lecturer = int(request.args.get("dozent", None))
    available_courses = management.get_lecturers_courses()
    lecturers_courses = []
    for course in available_courses:
        if lecturer == course["lecturer_id"]:
            lecturers_courses.append(course)

    return render_template(
        "booking/lecturers_courses.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
        courses=sorted(lecturers_courses, key=lambda x: x["course"]),
    )


@app.route("/lager", methods=["GET", "POST"])
def stock():
    """Seite zur Darstellung aller vorhandenen Materialien"""
    if not session.get("user"):
        return redirect("/login")

    if request.method == "POST":
        if "edit" in request.form:
            return redirect("lager/bearbeiten")
        if "add" in request.form:
            return redirect("lager/hinzufuegen")
        management.delete_materials(request.form.get("delete"))

    return render_template(
        "stock/stock.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
        materials=sorted(management.get_materials(), key=lambda x: x["material"]),
    )


@app.route("/lager/bearbeiten", methods=["GET", "POST"])
def stock_edit():
    """Seite zum Bearbeiten aller vrhandenen Materialien"""
    if not session.get("user"):
        return redirect("/login")

    if request.method == "POST":
        if "save" in request.form:
            for entry in management.get_materials():
                material = request.form.get(f"{entry['material_id']}_material")
                amount = request.form.get(f"{entry['material_id']}_amount")
                report = request.form.get(f"{entry['material_id']}_report")
                order_number = request.form.get(f"{entry['material_id']}_order_number")
                storage_location = request.form.get(
                    f"{entry['material_id']}_storage_location"
                )
                comment = request.form.get(f"{entry['material_id']}_comment")
                try:
                    management.update_materials(
                        entry["material_id"],
                        material,
                        amount,
                        report,
                        order_number,
                        storage_location,
                        comment,
                    )
                except sqlite3.IntegrityError:
                    pass
        return redirect("/lager")

    return render_template(
        "stock/stock_edit.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
        materials=sorted(management.get_materials(), key=lambda x: x["material"]),
    )


@app.route("/lager/hinzufuegen", methods=["GET", "POST"])
def stock_add():
    """Seite zum Hinzufügen eines Materials"""
    if not session.get("user"):
        return redirect("/login")

    if request.method == "POST":
        if "save" in request.form:
            material = request.form.get("material", None)
            amount = request.form.get("amount", None)
            report = request.form.get("report", None)
            order_number = request.form.get("order_number", None)
            storage_location = request.form.get("storage_location", None)
            comment = request.form.get("comment", None)
            try:
                management.insert_materials(
                    material, amount, report, order_number, storage_location, comment
                )
            except sqlite3.IntegrityError:
                pass
        return redirect("/lager")

    return render_template(
        "stock/stock_add.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
        materials=sorted(management.get_materials(), key=lambda x: x["material"]),
    )


@app.route("/kurse", methods=["GET", "POST"])
def courses():
    """Seite zum Darstellen aller vorhandenen Kurse"""
    if not session.get("user"):
        return redirect("/login")

    if request.method == "POST":
        if "edit" in request.form:
            return redirect("/kurse/bearbeiten")
        if "add" in request.form:
            return redirect("/kurse/hinzufuegen")
        management.delete_courses(request.form.get("delete"))

    return render_template(
        "courses/courses.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
        courses=sorted(management.get_courses(), key=lambda x: x["course"]),
        lecturers_courses=sorted(
            management.get_lecturers_courses(), key=lambda x: x["last_name"]
        ),
    )


@app.route("/kurse/bearbeiten", methods=["GET", "POST"])
def courses_edit():
    """Seite zum Bearbeiten aller vorhandenen Kurse"""
    if not session.get("user"):
        return redirect("/login")

    if request.method == "POST":
        if "save" in request.form:
            for entry in management.get_courses():
                course = request.form.get(f"{entry['course_id']}_course")
                comment = request.form.get(f"{entry['course_id']}_comment")
                try:
                    management.update_courses(entry["course_id"], course, comment)
                except sqlite3.IntegrityError:
                    pass
        return redirect("/kurse")

    return render_template(
        "courses/courses_edit.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
        courses=sorted(management.get_courses(), key=lambda x: x["course"]),
    )


@app.route("/kurse/hinzufuegen", methods=["GET", "POST"])
def courses_add():
    """Seite zum Hinzufügen eines neuen Kurses"""
    if not session.get("user"):
        return redirect("/login")

    if request.method == "POST":
        if "save" in request.form:
            course = request.form.get("course", None)
            comment = request.form.get("comment", None)
            try:
                management.insert_courses(course, comment)
            except sqlite3.IntegrityError:
                pass
        return redirect("/kurse")

    return render_template(
        "courses/courses_add.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
        courses=sorted(management.get_courses(), key=lambda x: x["course"]),
    )


@app.route("/dozierende/<lecturer>", methods=["GET", "POST"])
def lecturers(lecturer: str):
    """Seite zum Darstellen aller vorhandenen Kurse eines/einer Dozenten/Dozentin"""
    if not session.get("user"):
        return redirect("/login")

    last_name, first_name = lecturer.split("_")
    lecturer_list = management.get_lecturers()
    for entry in lecturer_list:
        if entry["first_name"] == first_name and entry["last_name"] == last_name:
            lecturer_id = entry["lecturer_id"]

    if request.method == "POST":
        if "edit" in request.form:
            return redirect(
                f"/dozierende/{lecturer}/{request.form.get('course', None)}/bearbeiten"
            )
        if "add" in request.form:
            return redirect(
                f"/dozierende/{lecturer}/{request.form.get('course', None)}/hinzufuegen"
            )
        if "add_course" in request.form:
            return redirect(f"/dozierende/{lecturer}/hinzufuegen")
        if "delete" in request.form:
            course = request.form.get("course")
            for entry in management.get_lecturers_courses():
                if entry["course"] == course and entry["lecturer_id"] == lecturer_id:
                    management.delete_lecturers_courses(entry["lecturers_course_id"])
                    break
            return redirect(f"/dozierende/{lecturer}")
        if "delete_lecturer" in request.form:
            management.delete_lecturers(lecturer_id)
            return redirect("/kurse")

        management.delete_requirements(int(request.form.get("delete_requirement")))
        return redirect(f"/dozierende/{lecturer}")

    return render_template(
        "lecturers/lecturer.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturer={
            "lecturer_id": lecturer_id,
            "first_name": first_name,
            "last_name": last_name,
        },
        lecturers=sorted(lecturer_list, key=lambda x: x["last_name"]),
        courses=sorted(management.get_lecturers_courses(), key=lambda x: x["course"]),
        requirements=sorted(
            management.get_lecturers_requirements(lecturer_id),
            key=lambda x: x["material"],
        ),
    )


@app.route("/dozierende/hinzufuegen", methods=["GET", "POST"])
def add_lecturers():
    """Seite zum hinzufügen eines/einer neuen/neuer Dozenten/Dozentin"""
    if not session.get("user"):
        return redirect("/login")

    if request.method == "POST":
        if "save" in request.form:
            first_name = request.form.get("first_name", None)
            last_name = request.form.get("last_name", None)
            try:
                management.insert_lecturers(first_name, last_name)
            except sqlite3.IntegrityError:
                pass
        return redirect("/kurse")

    return render_template(
        "lecturers/add_lecturer.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
    )


@app.route("/dozierende/<lecturer>/<course>/bearbeiten", methods=["GET", "POST"])
def lecturers_edit(lecturer: str, course: str):
    """Seite zum Bearbeiten aller Materialien eines Kurses eines/einer Dozenten/Dozentin"""
    if not session.get("user"):
        return redirect("/login")

    last_name, first_name = lecturer.split("_")
    lecturer_list = management.get_lecturers()
    for entry in lecturer_list:
        if entry["first_name"] == first_name and entry["last_name"] == last_name:
            lecturer_id = entry["lecturer_id"]

    for entry in management.get_courses():
        if entry["course"] == course:
            course_id = entry["course_id"]

    if request.method == "POST":
        if "save" in request.form:
            course_id = int(request.form.get("course"))
            for entry in management.get_lecturers_courses():
                if (
                    entry["course_id"] == course_id
                    and entry["lecturer_id"] == lecturer_id
                ):
                    lecturers_course_id = entry["lecturers_course_id"]
                    break

            for entry in management.get_lecturers_requirements(lecturer_id):
                if entry["course_id"] == course_id:
                    material_id = int(
                        request.form.get(f"{entry['material_id']}_material")
                    )
                    requirement = int(
                        request.form.get(f"{entry['material_id']}_requirement")
                    )
                    is_static = int(
                        request.form.get(f"{entry['material_id']}_is_static")
                    )
                    try:
                        management.update_requirements(
                            lecturers_course_id, material_id, requirement, is_static
                        )
                    except sqlite3.IntegrityError:
                        pass
        return redirect(f"/dozierende/{lecturer}")

    return render_template(
        "lecturers/lecturer_edit_course.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturer={
            "lecturer_id": lecturer_id,
            "first_name": first_name,
            "last_name": last_name,
        },
        lecturers=sorted(lecturer_list, key=lambda x: x["last_name"]),
        course={"course_id": course_id, "course": course},
        materials=sorted(management.get_materials(), key=lambda x: x["material"]),
        requirements=sorted(
            management.get_lecturers_requirements(lecturer_id),
            key=lambda x: x["material"],
        ),
    )


@app.route("/dozierende/<lecturer>/<course>/hinzufuegen", methods=["GET", "POST"])
def lecturers_add(lecturer: str, course: str):
    """Seite zum Hinzufügen eines Materials zum Kurs eines/einer Dozenten/Dozentin"""
    if not session.get("user"):
        return redirect("/login")

    last_name, first_name = lecturer.split("_")
    lecturer_list = management.get_lecturers()
    for entry in lecturer_list:
        if entry["first_name"] == first_name and entry["last_name"] == last_name:
            lecturer_id = entry["lecturer_id"]

    for entry in management.get_courses():
        if entry["course"] == course:
            course_id = entry["course_id"]

    used_materials = []
    for material in management.get_materials():
        for requirement in management.get_lecturers_requirements(lecturer_id):
            if (
                requirement["course"] == course
                and material["material"] == requirement["material"]
            ):
                used_materials.append(material)
    unused_materials = [
        material
        for material in management.get_materials()
        if material not in used_materials
    ]

    if request.method == "POST":
        if "save" in request.form:
            for entry in management.get_lecturers_courses():
                if (
                    entry["course_id"] == course_id
                    and entry["lecturer_id"] == lecturer_id
                ):
                    lecturers_course_id = entry["lecturers_course_id"]
                    break

            material_id = int(request.form.get("material", None))
            requirement = int(request.form.get("requirement", None))
            is_static = int(request.form.get("is_static", None))
            try:
                management.insert_requirements(
                    lecturers_course_id, material_id, requirement, is_static
                )
            except sqlite3.IntegrityError:
                pass
        return redirect(f"/dozierende/{lecturer}")

    return render_template(
        "lecturers/lecturer_add_material.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturer={
            "lecturer_id": lecturer_id,
            "first_name": first_name,
            "last_name": last_name,
        },
        lecturers=sorted(lecturer_list, key=lambda x: x["last_name"]),
        course={"course_id": course_id, "course": course},
        materials=sorted(unused_materials, key=lambda x: x["material"]),
    )


@app.route("/dozierende/<lecturer>/hinzufuegen", methods=["GET", "POST"])
def lecturers_add_course(lecturer: str):
    """Seite zum Hinzufügen eines neuen Kurses für eines/einer Dozenten/Dozentin"""
    if not session.get("user"):
        return redirect("/login")

    last_name, first_name = lecturer.split("_")
    lecturer_list = management.get_lecturers()
    for entry in lecturer_list:
        if entry["first_name"] == first_name and entry["last_name"] == last_name:
            lecturer_id = entry["lecturer_id"]

    used_courses = []
    for course in management.get_courses():
        for lecturers_course in management.get_lecturers_courses():
            print(f"{lecturers_course['course']}, {lecturer_id}")
            print(f"{lecturers_course['lecturer_id']}, {course}")
            if (
                lecturers_course["course"] == course["course"]
                and lecturers_course["lecturer_id"] == lecturer_id
            ):
                used_courses.append(course)
    unused_courses = [
        course for course in management.get_courses() if course not in used_courses
    ]

    if request.method == "POST":
        if "save" in request.form:
            try:
                management.insert_lecturers_courses(
                    lecturer_id, request.form.get("course", None)
                )
            except sqlite3.IntegrityError:
                pass
        return redirect(f"/dozierende/{lecturer}")

    return render_template(
        "lecturers/lecturer_add_course.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturer={
            "lecturer_id": lecturer_id,
            "first_name": first_name,
            "last_name": last_name,
        },
        lecturers=sorted(lecturer_list, key=lambda x: x["last_name"]),
        courses=sorted(unused_courses, key=lambda x: x["course"]),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Seite zum Anmelden"""
    if request.method == "POST":
        name = request.form.get("user")
        password = request.form.get("password")

        if users.check_user(name, password):
            session["user"] = name
        return redirect("/")
    return render_template(
        "login.html",
        company=COMPANY,
        color=COLOR,
        font_color=FONT_COLOR,
        lecturers=sorted(management.get_lecturers(), key=lambda x: x["last_name"]),
    )


@app.route("/logout", methods=["GET"])
def logout():
    """Logik zum Abmelden"""
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=False)
