CREATE TABLE MATERIALS (
    material_id      INTEGER
                     PRIMARY KEY
                     AUTOINCREMENT,
    material         TEXT
                     NOT NULL,
    amount           INTEGER
                     DEFAULT 0,
    report           INTEGER
                     DEFAULT 0,
    order_number     TEXT
                     NOT NULL,
    storage_location TEXT
                     NOT NULL,
    comment          TEXT,

    UNIQUE (material, order_number)
);

CREATE TABLE LECTURERS (
    lecturer_id INTEGER
                PRIMARY KEY
                AUTOINCREMENT,
    first_name  TEXT
                NOT NULL,
    last_name   TEXT
                NOT NULL,

    UNIQUE (first_name, last_name)
);

CREATE TABLE COURSES (
    course_id   INTEGER
                PRIMARY KEY
                AUTOINCREMENT,
    course      TEXT
                NOT NULL
                UNIQUE,
    comment     TEXT
);

CREATE TABLE LECTURERS_COURSES (
    lecturers_course_id INTEGER
                        PRIMARY KEY
                        AUTOINCREMENT,
    lecturer_id         INTEGER
                        NOT NULL,
    course_id           INTEGER
                        NOT NULL,

    FOREIGN KEY (lecturer_id) REFERENCES lecturers (lecturer_id),
    FOREIGN KEY (course_id)   REFERENCES courses   (course_id),
    UNIQUE      (lecturer_id, course_id)
);

CREATE TABLE REQUIREMENTS (
    requirement_id      INTEGER
                        PRIMARY KEY
                        AUTOINCREMENT,
    lecturers_course_id INTEGER
                        NOT NULL,
    material_id         INTEGER
                        NOT NULL,
    requirement         INTEGER
                        NOT NULL
                        DEFAULT 0,
    is_static           INTEGER
                        NOT NULL
                        DEFAULT 0
                        CHECK (is_static IN (0, 1)),

    FOREIGN KEY (lecturers_course_id) REFERENCES lecturers_courses (lecturers_course_id),
    FOREIGN KEY (material_id)         REFERENCES materials         (material_id),
    UNIQUE      (lecturers_course_id, material_id)
);
