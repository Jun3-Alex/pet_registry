from db_utils import connect_to_db, create_tables
from menu import show_menu


def main():
    # Подключение к базе данных
    mydb = connect_to_db()

    # Создание таблиц (если они не существуют)
    create_tables(mydb)

    # Запуск меню
    show_menu()

    # Закрытие соединения с базой данных
    mydb.close()


if __name__ == "__main__":
    main()
