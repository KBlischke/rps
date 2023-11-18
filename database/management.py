"""Modul zur Interaktion mit der 'management'-Datenbank"""


import sqlite3


PATH = "database/management.db"


def get_materials() -> list:
    """Erhalte alle vorhandenen Materialien"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM MATERIALS")
    entries = cursor.fetchall()

    materials = []
    for entry in entries:
        materials.append(
            {
                "material_id": entry[0],
                "material": entry[1],
                "amount": entry[2],
                "report": entry[3],
                "order_number": entry[4],
                "storage_location": entry[5],
                "comment": entry[6],
            }
        )

    connection.commit()
    connection.close()

    return materials


def update_materials_amount(material_id: int, consumption: int) -> None:
    """Passe die Menge eines Materials an"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE MATERIALS
        SET amount = CASE
            WHEN (amount - ?) < 0 THEN 0
            ELSE amount - ?
            END
        WHERE material_id = ?
    """,
        (
            consumption,
            consumption,
            material_id,
        ),
    )

    connection.commit()
    connection.close()


def update_materials(
    material_id: int,
    material: str,
    amount: int,
    report: int,
    order_number: str,
    storage_location: str,
    comment: str,
) -> None:
    """Passe ein Material an"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE MATERIALS
        SET
            material = ?,
            amount = ?,
            report = ?,
            order_number = ?,
            storage_location = ?,
            comment = ?
        WHERE material_id = ?
    """,
        (
            material,
            amount,
            report,
            order_number,
            storage_location,
            comment,
            material_id,
        ),
    )

    connection.commit()
    connection.close()


def insert_materials(
    material: str,
    amount: int,
    report: int,
    order_number: str,
    storage_location: str,
    comment: str,
) -> None:
    """Füge ein neues Material ein"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO MATERIALS
        (material, amount, report, order_number, storage_location, comment)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            material,
            amount,
            report,
            order_number,
            storage_location,
            comment,
        ),
    )

    connection.commit()
    connection.close()


def delete_materials(material_id: int) -> None:
    """Entferne ein Material"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM MATERIALS
        WHERE material_id = ?
    """,
        (material_id,),
    )
    cursor.execute(
        """
        DELETE FROM REQUIREMENTS
        WHERE material_id = ?
    """,
        (material_id,),
    )

    connection.commit()
    connection.close()


def get_lecturers() -> list:
    """Erhalte alle vorhandenen Dozenten/Dozentinnen"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM LECTURERS")
    entries = cursor.fetchall()

    lecturers = []
    for entry in entries:
        lecturers.append(
            {"lecturer_id": entry[0], "first_name": entry[1], "last_name": entry[2]}
        )

    connection.commit()
    connection.close()

    return lecturers


def insert_lecturers(
    first_name: str,
    last_name: str,
) -> None:
    """Füge eine/n neue/n Dozent/in ein"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO LECTURERS
        (first_name, last_name)
        VALUES (?, ?)
    """,
        (
            first_name,
            last_name,
        ),
    )

    connection.commit()
    connection.close()


def delete_lecturers(lecturer_id: int) -> None:
    """Entferne eine/n Dozent/in"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM LECTURERS
        WHERE lecturer_id = ?
    """,
        (lecturer_id,),
    )
    cursor.execute(
        """
        DELETE FROM LECTURERS_COURSES
        WHERE lecturer_id = ?
    """,
        (lecturer_id,),
    )

    for entry in get_lecturers_courses():
        if entry["lecturer_id"] == lecturer_id:
            cursor.execute(
                """
                DELETE FROM REQUIREMENTS
                WHERE lecturers_course_id = ?
            """,
                (entry["lecturers_course_id"],),
            )
            break

    connection.commit()
    connection.close()


def get_courses() -> list:
    """Erhalte alle vorhandenen Kurse"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM COURSES")
    entries = cursor.fetchall()

    courses = []
    for entry in entries:
        courses.append(
            {
                "course_id": entry[0],
                "course": entry[1],
                "comment": entry[2],
            }
        )

    connection.commit()
    connection.close()

    return courses


def update_courses(
    course_id: int,
    course: str,
    comment: str,
) -> None:
    """Passe einen Kurs an"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE COURSES
        SET
            course = ?,
            comment = ?
        WHERE course_id = ?
    """,
        (
            course,
            comment,
            course_id,
        ),
    )

    connection.commit()
    connection.close()


def insert_courses(course: str, comment: str) -> None:
    """Füge einen neuen Kurs ein"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO COURSES
        (course, comment)
        VALUES (?, ?)
    """,
        (
            course,
            comment,
        ),
    )

    connection.commit()
    connection.close()


def delete_courses(course_id: int) -> None:
    """Entferne einen Kurs"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM COURSES
        WHERE course_id = ?
    """,
        (course_id,),
    )
    cursor.execute(
        """
        DELETE FROM LECTURERS_COURSES
        WHERE course_id = ?
    """,
        (course_id,),
    )

    connection.commit()
    connection.close()


def get_lecturers_courses() -> list:
    """Erhalte alle vorhandenen Kurse aller vorhandenen Dozierenden"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT LECTURERS_COURSES.lecturers_course_id,
        LECTURERS_COURSES.lecturer_id,
        LECTURERS.first_name,
        LECTURERS.last_name,
        LECTURERS_COURSES.course_id,
        COURSES.course,
        COURSES.comment
        FROM LECTURERS_COURSES
        INNER JOIN LECTURERS ON LECTURERS_COURSES.lecturer_id = LECTURERS.lecturer_id
        INNER JOIN COURSES ON LECTURERS_COURSES.course_id = COURSES.course_id
    """
    )
    entries = cursor.fetchall()

    lecturers_courses = []
    for entry in entries:
        lecturers_courses.append(
            {
                "lecturers_course_id": entry[0],
                "lecturer_id": entry[1],
                "first_name": entry[2],
                "last_name": entry[3],
                "course_id": entry[4],
                "course": entry[5],
                "comment": entry[6],
            }
        )

    connection.commit()
    connection.close()

    return lecturers_courses


def insert_lecturers_courses(
    lecturer_id: int,
    course_id: int,
) -> None:
    """Füge einen neuen Kurs für eie/n Dzent/in ein"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO LECTURERS_COURSES
        (lecturer_id, course_id)
        VALUES (?, ?)
    """,
        (lecturer_id, course_id),
    )

    connection.commit()
    connection.close()


def delete_lecturers_courses(lecturers_course_id: int) -> None:
    """Entferne einen Kurs eines/einer Dozenten/Dozentin"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM LECTURERS_COURSES
        WHERE lecturers_course_id = ?
    """,
        (lecturers_course_id,),
    )
    cursor.execute(
        """
        DELETE FROM REQUIREMENTS
        WHERE lecturers_course_id = ?
    """,
        (lecturers_course_id,),
    )

    connection.commit()
    connection.close()


def get_lecturers_requirements(lecturer_id: int) -> list:
    """Erhalte alle Bedarfe eines/einer Dozenten/Dozentin"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT REQUIREMENTS.requirement_id,
        COURSES.course_id,
        COURSES.course,
        COURSES.comment,
        REQUIREMENTS.material_id,
        MATERIALS.material,
        MATERIALS.amount,
        MATERIALS.report,
        MATERIALS.order_number,
        MATERIALS.storage_location,
        MATERIALS.comment,
        REQUIREMENTS.requirement,
        REQUIREMENTS.is_static
        FROM REQUIREMENTS
        INNER JOIN LECTURERS_COURSES ON REQUIREMENTS.lecturers_course_id = LECTURERS_COURSES.lecturers_course_id
        INNER JOIN LECTURERS ON LECTURERS_COURSES.lecturer_id = LECTURERS.lecturer_id
        INNER JOIN COURSES ON LECTURERS_COURSES.course_id = COURSES.course_id
        INNER JOIN MATERIALS ON REQUIREMENTS.material_id = MATERIALS.material_id
        WHERE LECTURERS_COURSES.lecturer_id = ?
    """,
        (lecturer_id,),
    )
    entries = cursor.fetchall()

    lecturers_requirements = []
    for entry in entries:
        lecturers_requirements.append(
            {
                "requirement_id": entry[0],
                "course_id": entry[1],
                "course": entry[2],
                "course_comment": entry[3],
                "material_id": entry[4],
                "material": entry[5],
                "amount": entry[6],
                "report": entry[7],
                "order_number": entry[8],
                "storage_location": entry[9],
                "material_comment": entry[10],
                "requirement": entry[11],
                "is_static": entry[12],
            }
        )

    connection.commit()
    connection.close()

    return lecturers_requirements


def update_requirements(
    lecturers_course_id: int,
    material_id: int,
    requirement: int,
    is_static: int,
) -> None:
    """Passe einen Bedarf eines/einer Dozenten/Dozentin an"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE REQUIREMENTS
        SET
            requirement = ?,
            is_static = ?
        WHERE lecturers_course_id = ? AND material_id = ?
    """,
        (
            requirement,
            is_static,
            lecturers_course_id,
            material_id,
        ),
    )

    connection.commit()
    connection.close()


def insert_requirements(
    lecturers_course_id: int, material_id: int, requirement: int, is_static: int
) -> None:
    """Füge einen neuen Bedarf eines/einer Dozenten/Dozentin ein"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO REQUIREMENTS
        (lecturers_course_id, material_id, requirement, is_static)
        VALUES (?, ?, ?, ?)
    """,
        (
            lecturers_course_id,
            material_id,
            requirement,
            is_static,
        ),
    )

    connection.commit()
    connection.close()


def delete_requirements(requirement_id: int) -> None:
    """Entferne einen Bedarf eines/einer Dozenten/Dozentin"""
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM REQUIREMENTS
        WHERE requirement_id = ?
    """,
        (requirement_id,),
    )

    connection.commit()
    connection.close()
