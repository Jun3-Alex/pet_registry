from db_utils import *
from counter import Counter, CounterError


def show_menu():
    while True:
        print("\nМеню:")
        print("1. Добавить новое животное")
        print("2. Получить список животных")
        print("3. Получить команды домашнего животного")
        print("4. Обновить команды домашнего животного")
        print("5. Удалить животное")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            add_new_animal()
        elif choice == "2":
            all_animals()
        elif choice == "3":
            get_pet_commands()
        elif choice == "4":
            update_pet_commands()
        elif choice == "5":
            delete_animal()
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Неверный номер действия. Попробуйте еще раз.")


def add_new_animal():
    print("Добавление нового животного")
    name = input("Введите имя животного: ")
    print("Выберите тип животного:")
    print("1. Собака")
    print("2. Кошка")
    print("3. Хомяк")
    print("4. Лошадь")
    print("5. Верблюд")
    print("6. Осёл")
    type_name = input("Введите номер типа животного: ")
    birth_date = input("Введите дату рождения животного (ГГГГ-ММ-ДД): ")

    try:
        with Counter() as counter:
            if type_name.lower() == "1":
                type_name = "dog"
                breed = input("Введите породу собаки: ")
                commands = input("Введите команды, которые выполняет собака (через запятую): ")

                # Сначала добавляем данные о животном и получаем animal_id
                animal_id = add_animal(name, type_name, birth_date)

                # Затем добавляем данные о питомце и получаем pet_id
                pet_id = add_pet(animal_id, commands)

                # Наконец, добавляем данные о собаке
                dog_id = add_dog(pet_id, breed)
                print(f"Собака с ID {dog_id} была успешно добавлена.")
                counter.add()
            elif type_name.lower() == "2":
                type_name = "cat"
                breed = input("Введите породу кошки: ")
                commands = input("Введите команды, которые выполняет кошка (через запятую): ")

                # Сначала добавляем данные о животном и получаем animal_id
                animal_id = add_animal(name, type_name, birth_date)

                # Затем добавляем данные о питомце и получаем pet_id
                pet_id = add_pet(animal_id, commands)

                # Наконец, добавляем данные о кошке
                cat_id = add_cat(breed, pet_id)
                print(f"Кошка с ID {cat_id} была успешно добавлена.")
                counter.add()
            elif type_name.lower() == "3":
                type_name = "hamster"
                cage_size = int(input("Введите размер клетки для хомяка(см3): "))
                commands = input("Введите команды, которые выполняет хомяк (через запятую): ")

                # Сначала добавляем данные о животном и получаем animal_id
                animal_id = add_animal(name, type_name, birth_date)

                # Затем добавляем данные о питомце и получаем pet_id
                pet_id = add_pet(animal_id, commands)

                # Наконец, добавляем данные о хомяке
                hamster_id = add_hamster(pet_id, cage_size)
                print(f"Хомяк с ID {hamster_id} был успешно добавлен.")
                counter.add()
            elif type_name.lower() == "4":
                type_name = "horse"
                load_capacity = int(input("Введите грузоподъемность лошади: "))

                # Добавление животного и получение animal_id
                animal_id = add_animal(name, type_name, birth_date)

                # Добавление вьючного животного и получение pack_animal_id
                pack_animal_id = add_pack_animal(animal_id, load_capacity)

                # Добавление информации специфичной для лошади
                horse_id = add_horse(pack_animal_id, load_capacity)

                print(f"Лошадь с ID {horse_id} была успешно добавлена.")
                counter.add()
            elif type_name.lower() == "5":
                type_name = "camel"
                load_capacity = int(input("Введите грузоподъемность верблюда: "))

                # Добавление животного и получение animal_id
                animal_id = add_animal(name, type_name, birth_date)

                # Добавление вьючного животного и получение pack_animal_id
                pack_animal_id = add_pack_animal(animal_id, load_capacity)

                # Добавление информации специфичной для верблюда
                camel_id = add_camel(pack_animal_id, load_capacity)

                print(f"Верблюд с ID {camel_id} была успешно добавлена.")
                counter.add()
            elif type_name.lower() == "6":
                type_name = "donkey"
                load_capacity = int(input("Введите грузоподъемность осла: "))

                # Добавление животного и получение animal_id
                animal_id = add_animal(name, type_name, birth_date)

                # Добавление вьючного животного и получение pack_animal_id
                pack_animal_id = add_pack_animal(animal_id, load_capacity)

                # Добавление информации специфичной для верблюда
                donkey_id = add_donkey(pack_animal_id, load_capacity)

                print(f"Осёл с ID {donkey_id} была успешно добавлена.")
                counter.add()
            else:
                print("Неверный тип животного.")

            print(f"Всего добавлено животных: {counter.value}")
    except CounterError as e:
        print(f"Ошибка: {e}")


def all_animals():
    animals = get_animals()
    if animals:
        print("Список животных:")
        for animal in animals:
            print(f"{animal[0]} ({animal[1]})")
    else:
        print("Нет животных в базе данных.")


def get_pet_commands():
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        global_db_connection = connect_to_db()
        if global_db_connection is None:
            print("Не удалось установить соединение с базой данных.")
            return

    pet_name = input("Введите имя домашнего животного: ")

    mycursor = global_db_connection.cursor()
    mycursor.execute("""
        SELECT command_name 
        FROM commands 
        JOIN pet_commands ON commands.command_id = pet_commands.command_id 
        JOIN pets ON pet_commands.pet_id = pets.pet_id 
        JOIN animals ON pets.animal_id = animals.animal_id 
        WHERE animals.name = %s
    """, (pet_name,))

    commands = mycursor.fetchall()
    mycursor.close()

    if commands:
        commands_list = [command[0] for command in commands]
        print(f"Команды для {pet_name}: {', '.join(commands_list)}")
    else:
        print(f"Животное с именем {pet_name} не найдено или не является домашним животным.")


def update_pet_commands():
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        connect_to_db()

    pet_name = input("Введите имя домашнего животного: ")
    new_commands = input("Введите новые команды (через запятую): ").split(",")

    mycursor = global_db_connection.cursor()

    # Получаем pet_id для данного животного
    mycursor.execute(
        "SELECT pets.pet_id FROM pets JOIN animals ON pets.animal_id = animals.animal_id WHERE animals.name = %s",
        (pet_name,))
    pet_result = mycursor.fetchone()

    if pet_result:
        pet_id = pet_result[0]

        # Удаляем старые команды
        mycursor.execute("DELETE FROM pet_commands WHERE pet_id = %s", (pet_id,))

        # Добавляем новые команды
        for command in new_commands:
            command = command.strip()
            # Проверяем, существует ли команда
            mycursor.execute("SELECT command_id FROM commands WHERE command_name = %s", (command,))
            command_result = mycursor.fetchone()
            if command_result:
                command_id = command_result[0]
            else:
                mycursor.execute("INSERT INTO commands (command_name) VALUES (%s)", (command,))
                command_id = mycursor.lastrowid
                global_db_connection.commit()

            # Добавляем связь команды с питомцем
            mycursor.execute("INSERT INTO pet_commands (pet_id, command_id) VALUES (%s, %s)", (pet_id, command_id))
            global_db_connection.commit()

        print(f"Команды для {pet_name} успешно обновлены.")
    else:
        print(f"Животное с именем {pet_name} не найдено.")

    mycursor.close()


def delete_animal():
    global global_db_connection
    if global_db_connection is None or not global_db_connection.is_connected():
        global_db_connection = connect_to_db()
        if global_db_connection is None:
            print("Не удалось установить соединение с базой данных.")
            return

    pet_name = input("Введите имя удаляемого животного: ")
    mycursor = global_db_connection.cursor()

    # Получаем animal_id и type_name
    mycursor.execute("""
           SELECT animals.animal_id, animal_types.type_name
           FROM animals 
           JOIN animal_types ON animals.type_id = animal_types.type_id
           WHERE animals.name = %s
       """, (pet_name,))
    animals = mycursor.fetchall()

    if animals:
        if len(animals) > 1:
            print("Найдены следующие животные с именем", pet_name)
            for animal in animals:
                print(f"ID: {animal[0]}, Тип: {animal[1]}")
            animal_id = int(input("Введите ID животного, которое нужно удалить: "))

            # Получаем type_name для выбранного animal_id
            mycursor.execute("""
                        SELECT animal_types.type_name
                        FROM animals 
                        JOIN animal_types ON animals.type_id = animal_types.type_id
                        WHERE animals.animal_id = %s
                    """, (animal_id,))
            type_name_result = mycursor.fetchone()
            if type_name_result:
                type_name = type_name_result[0]
            else:
                print("Животное с таким ID не найдено.")
                return
        else:
            animal_id, type_name = animals[0]

        # Удаляем связанные записи из таблицы pet_commands
        mycursor.execute("DELETE FROM pet_commands WHERE pet_id IN (SELECT pet_id FROM pets WHERE animal_id = %s)",
                         (animal_id,))

        # Вызов соответствующей функции в зависимости от типа животного
        if type_name == 'dog':
            delete_dog(animal_id)
        elif type_name == 'cat':
            delete_cat(animal_id)
        elif type_name == 'hamster':
            delete_hamster(animal_id)
        elif type_name == 'horse':
            delete_horse(animal_id)
        elif type_name == 'camel':
            delete_camel(animal_id)
        elif type_name == 'donkey':
            delete_donkey(animal_id)

        # Удаляем запись из таблицы pets и animals
        mycursor.execute("DELETE FROM pets WHERE animal_id = %s", (animal_id,))
        mycursor.execute("DELETE FROM animals WHERE animal_id = %s", (animal_id,))
        global_db_connection.commit()

        print(f"Животное {pet_name} было удалено.")
    else:
        print("Животное не найдено.")

    mycursor.close()
