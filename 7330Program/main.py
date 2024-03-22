from dbOperation import process_command, create_db_connection, process_csv_file


def main():
    file_name = input("Enter the name of the CSV file: ")
    process_csv_file(file_name)


if __name__ == "__main__":
    main()