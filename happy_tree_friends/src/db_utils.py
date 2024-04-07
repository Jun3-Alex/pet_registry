from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()  # Загружает переменные среды из .env файла

# Глобальная переменная для хранения соединения с БД
global_db_connection = None


def connect_to_db():
    global global_db_connection
    try:
        global_db_connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        return global_db_connection
    except mysql.connector.Error as err:
        print(f"Ошибка при подключении к базе данных: {err}")
        return None


def create_tables(mydb):
    mycursor = global_db_connection.cursor()  # Создание курсора для выполнения SQL-запросов

    # Создание таблицы animal_types
    mycursor.execute("CREATE TABLE IF NOT EXISTS animal_types "
                     "(type_id INT AUTO_INCREMENT PRIMARY KEY, "
                     "type_name VARCHAR(255))")

    # Создание таблицы animals
    mycursor.execute("CREATE TABLE IF NOT EXISTS animals "
                     "(animal_id INT AUTO_INCREMENT PRIMARY KEY, "
                     "type_id INT, "
                     "name VARCHAR(255), "
                     "birth_date DATE, "
                     "FOREIGN KEY (type_id) REFERENCES animal_types(type_id))")

    # Создание таблицы pets
    mycursor.execute("CREATE TABLE IF NOT EXISTS pets "
                     "(pet_id INT AUTO_INCREMENT PRIMARY KEY, "
                     "animal_id INT, "
                     "commands VARCHAR(255), "
                     "FOREIGN KEY (animal_id) REFERENCES animals(animal_id))")

    # Создание таблицы dogs
    mycursor.execute("CREATE TABLE IF NOT EXISTS dogs "
                     "(dog_id INT AUTO_INCREMENT PRIMARY KEY, "
                     "breed VARCHAR(255), "
                     "pet_id INT, "
                     "FOREIGN KEY (pet_id) REFERENCES pets(pet_id))")

    # Создание таблицы cats
    mycursor.execute("CREATE TABLE IF NOT EXISTS cats "
                     "(cat_id INT AUTO_INCREMENT PRIMARY KEY, "
                     "breed VARCHAR(255), "
                     "pet_id INT, "
                     "FOREIGN KEY (pet_id) REFERENCES pets(pet_id))")

    # Создание таблицы hamsters
    mycursor.execute("CREATE TABLE IF NOT EXISTS hamsters "
                     "(hamster_id INT AUTO_INCREMENT PRIMARY KEY, "
                     "cage_size INT, "
                     "pet_id INT, "
                     "FOREIGN KEY (pet_id) REFERENCES pets(pet_id))")

    # Создание таблицы pack_animals
    mycursor.execute("CREATE TABLE IF NOT EXISTS pack_animals "
                     "(pack_animal_id INT AUTO_INCREMENT PRIMARY KEY, "
                     "animal_id INT, "
                     "load_capacity INT, "
                     "FOREIGN KEY (animal_id) REFERENCES animals(animal_id))")

    # Создание таблицы horses
    mycursor.execute("CREATE TABLE IF NOT EXISTS horses "
                     "(horse_id INT AUTO_INCREMENT PRIMARY KEY, "
                     "load_capacity INT, "
                     "pack_animal_id INT, "
                     "FOREIGN KEY (pack_animal_id) REFERENCES pack_animals(pack_animal_id))")

    # Создание таблицы camels
    mycursor.execute("CREATE TABLE IF NOT EXISTS camels "
                     "(camel_id INT AUTO_INCREMENT PRIMARY KEY, "
                     "load_capacity INT, "
                     "pack_animal_id INT, "
                     "FOREIGN KEY (pack_animal_id) REFERENCES pack_animals(pack_animal_id))")

    # Создание таблицы donkey
    mycursor.execute("CREATE TABLE IF NOT EXISTS donkey "
                     "(donkey_id INT AUTO_INCREMENT PRIMARY KEY, "
                     "load_capacity INT, "
                     "pack_animal_id INT, "
                     "FOREIGN KEY (pack_animal_id) REFERENCES pack_animals(pack_animal_id))")

    # Создание таблицы commands
    mycursor.execute("CREATE TABLE IF NOT EXISTS commands "
                     "(command_id INT AUTO_INCREMENT PRIMARY KEY, "
                     "command_name VARCHAR(255))")

    # Создание таблицы pet_commands
    mycursor.execute("CREATE TABLE IF NOT EXISTS pet_commands "
                     "(pet_id INT, "
                     "command_id INT, "
                     "FOREIGN KEY (pet_id) REFERENCES pets(pet_id), "
                     "FOREIGN KEY (command_id) REFERENCES commands(command_id))")


# Функция для добавления нового животного
def add_animal(name, type_name, birth_date):
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        connect_to_db()

    mycursor = global_db_connection.cursor()
    # Добавление нового типа животного, если он еще не существует
    mycursor.execute("SELECT type_id FROM animal_types WHERE type_name = %s", (type_name,))
    result = mycursor.fetchone()
    if result is None:
        mycursor.execute("INSERT INTO animal_types (type_name) VALUES (%s)", (type_name,))
        type_id = mycursor.lastrowid
        global_db_connection.commit()
    else:
        type_id = result[0]

    # Теперь добавляем информацию о животном
    mycursor.execute("INSERT INTO animals (name, type_id, birth_date) VALUES (%s, %s, %s)", (name, type_id, birth_date))
    animal_id = mycursor.lastrowid
    global_db_connection.commit()
    mycursor.close()

    return animal_id


def add_pet(animal_id, commands):
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        connect_to_db()

    mycursor = global_db_connection.cursor()
    mycursor.execute("INSERT INTO pets (animal_id) VALUES (%s)", (animal_id,))
    pet_id = mycursor.lastrowid

    for command in commands.split(","):
        # Проверяем, существует ли команда
        mycursor.execute("SELECT command_id FROM commands WHERE command_name = %s", (command,))
        command_id = mycursor.fetchone()
        if command_id is None:
            # Если команды нет, добавляем ее
            mycursor.execute("INSERT INTO commands (command_name) VALUES (%s)", (command,))
            command_id = mycursor.lastrowid
        else:
            command_id = command_id[0]

        # Добавляем связь команды с питомцем
        mycursor.execute("INSERT INTO pet_commands (pet_id, command_id) VALUES (%s, %s)", (pet_id, command_id))

    global_db_connection.commit()
    mycursor.close()

    return pet_id


# Функция для добавления новой собаки
def add_dog(pet_id, breed):
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        connect_to_db()

    mycursor = global_db_connection.cursor()
    mycursor.execute("INSERT INTO dogs (breed, pet_id) VALUES (%s, %s)", (breed, pet_id))
    dog_id = mycursor.lastrowid
    global_db_connection.commit()
    mycursor.close()

    return dog_id


# Функция для добавления новой кошки
def add_cat(breed, pet_id):
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        connect_to_db()

    mycursor = global_db_connection.cursor()
    mycursor.execute("INSERT INTO cats (breed, pet_id) VALUES (%s, %s)", (breed, pet_id))
    cat_id = mycursor.lastrowid
    global_db_connection.commit()
    mycursor.close()
    return cat_id


# Функция для добавления нового хомяка
def add_hamster(pet_id, cage_size):
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        connect_to_db()

    mycursor = global_db_connection.cursor()
    mycursor.execute("INSERT INTO hamsters (cage_size, pet_id) VALUES (%s, %s)", (cage_size, pet_id))
    hamster_id = mycursor.lastrowid
    global_db_connection.commit()
    mycursor.close()

    return hamster_id


# Функция для добавления нового вьючного животного
def add_pack_animal(animal_id, load_capacity):
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        connect_to_db()

    mycursor = global_db_connection.cursor()
    mycursor.execute("INSERT INTO pack_animals (animal_id, load_capacity) VALUES (%s, %s)", (animal_id, load_capacity))
    pack_animal_id = mycursor.lastrowid
    global_db_connection.commit()
    mycursor.close()

    return pack_animal_id


# Функция для добавления новой лошади
def add_horse(pack_animal_id, load_capacity):
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        connect_to_db()

    mycursor = global_db_connection.cursor()
    mycursor.execute("INSERT INTO horses (load_capacity, pack_animal_id) VALUES (%s, %s)",
                     (load_capacity, pack_animal_id))
    horse_id = mycursor.lastrowid
    global_db_connection.commit()
    mycursor.close()

    return horse_id


# Функция для добавления нового верблюда
def add_camel(pack_animal_id, load_capacity):
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        connect_to_db()

    mycursor = global_db_connection.cursor()
    mycursor.execute("INSERT INTO camels (load_capacity, pack_animal_id) VALUES (%s, %s)",
                     (load_capacity, pack_animal_id))
    camel_id = mycursor.lastrowid
    global_db_connection.commit()
    mycursor.close()

    return camel_id


# Функция для добавления нового осла
def add_donkey(pack_animal_id, load_capacity):
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        connect_to_db()

    mycursor = global_db_connection.cursor()
    mycursor.execute("INSERT INTO donkey (load_capacity, pack_animal_id) VALUES (%s, %s)",
                     (load_capacity, pack_animal_id))
    donkey_id = mycursor.lastrowid
    global_db_connection.commit()
    mycursor.close()

    return donkey_id


# Функция для получения списка животных
def get_animals():
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        connect_to_db()

    mycursor = global_db_connection.cursor()
    mycursor.execute(
        "SELECT animals.name, animal_types.type_name FROM animals JOIN animal_types ON animals.type_id = "
        "animal_types.type_id")
    animals = mycursor.fetchall()
    mycursor.close()
    return animals


def delete_dog(animal_id):
    mycursor = global_db_connection.cursor()
    mycursor.execute("DELETE FROM dogs WHERE pet_id IN (SELECT pet_id FROM pets WHERE animal_id = %s)", (animal_id,))


def delete_cat(animal_id):
    mycursor = global_db_connection.cursor()
    mycursor.execute("DELETE FROM cats WHERE pet_id IN (SELECT pet_id FROM pets WHERE animal_id = %s)", (animal_id,))


def delete_hamster(animal_id):
    mycursor = global_db_connection.cursor()
    mycursor.execute("DELETE FROM hamsters WHERE pet_id IN (SELECT pet_id FROM pets WHERE animal_id = %s)",
                     (animal_id,))


def delete_horse(animal_id):
    mycursor = global_db_connection.cursor()
    mycursor.execute(
        "DELETE FROM horses WHERE pack_animal_id IN (SELECT pack_animal_id FROM pack_animals WHERE animal_id = %s)",
        (animal_id,))
    mycursor.execute("DELETE FROM pack_animals WHERE animal_id = %s", (animal_id,))


def delete_camel(animal_id):
    mycursor = global_db_connection.cursor()
    mycursor.execute(
        "DELETE FROM camels WHERE pack_animal_id IN (SELECT pack_animal_id FROM pack_animals WHERE animal_id = %s)",
        (animal_id,))
    mycursor.execute("DELETE FROM pack_animals WHERE animal_id = %s", (animal_id,))


def delete_donkey(animal_id):
    mycursor = global_db_connection.cursor()
    mycursor.execute(
        "DELETE FROM donkey WHERE pack_animal_id IN (SELECT pack_animal_id FROM pack_animals WHERE animal_id = %s)",
        (animal_id,))
    mycursor.execute("DELETE FROM pack_animals WHERE animal_id = %s", (animal_id,))
