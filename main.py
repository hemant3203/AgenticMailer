from generate_emails import execute_tasks

if __name__ == "__main__":
    data_file = "contacts.csv"  # Change to "contacts.pdf" if using PDF
    execute_tasks(data_file)
    print("Emails have been successfully generated and saved!")
