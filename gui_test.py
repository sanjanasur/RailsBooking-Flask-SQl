import tkinter as tk
from tkinter import font
from tkinter import ttk
from datetime import datetime, timedelta
import sqlite3

# Establish a connection to the SQLite database and create a cursor
conn = sqlite3.connect('railway_reservation.db')
cursor = conn.cursor()


# Function to execute SQL queries based on user input
def execute_query(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result


# Function to handle both queries
def handle_queries():
    last_name = last_name_entry.get()
    first_name = first_name_entry.get()
    date = date_entry.get()
    age_start = int(age_start_entry.get())
    age_end = int(age_end_entry.get())


    train_name = train_name_entry.get()

    # SQL query to retrieve trains a passenger is booked on based on last name and first name
    query_trains = f"SELECT DISTINCT Train.* FROM Train " \
                   f"JOIN Booked ON Train.Train_Number = Booked.Train_Number " \
                   f"JOIN Passenger ON Booked.Passenger_ssn = Passenger.SSN " \
                   f"WHERE Passenger.last_name = '{last_name}' AND Passenger.first_name = '{first_name}'"

    # SQL query to retrieve passengers traveling on the entered date with confirmed tickets
    query_passengers = f"SELECT DISTINCT Passenger.* "\
f"FROM Passenger "\
f"JOIN Booked ON Passenger.SSN = Booked.Passenger_ssn "\
f"JOIN Train ON Booked.Train_Number = Train.Train_Number "\
f"JOIN Train_Status ON Train.Train_Name = Train_Status.TrainName "\
f"WHERE strftime('%m/%d/%Y', Train_Status.TrainDate) = '{date}' AND Booked.Status = 'Booked'"
    # SQL query to retrieve train names along with the count of passengers INTEGER)) BETWEEN {age_start} AND {age_end} "

    query_passengers_by_age = f"SELECT DISTINCT Train.Train_Number, Train.Train_Name, Train.Source_Station, Train.Destination_Station, " \
         f"Passenger.first_name || ' ' || Passenger.last_name AS Name, " \
         f"Passenger.address, Booked.Ticket_Type, Booked.Status " \
         f"FROM Passenger " \
         f"JOIN Booked ON Passenger.SSN = Booked.Passenger_ssn " \
         f"JOIN Train ON Train.Train_Number = Booked.Train_Number " \
         f"WHERE CAST(strftime('%Y', 'now') AS INTEGER) - CAST('19' || substr(bdate, -2) AS INTEGER) BETWEEN {age_start} AND {age_end}"
             


    # SQL query to retrieve train names along with the count of passengers for each train
    query_passengers_count_by_train = f"SELECT Train.Train_Name, COUNT(Booked.Passenger_ssn) AS Passenger_Count " \
                                      f"FROM Train " \
                                      f"LEFT JOIN Booked ON Train.Train_Number = Booked.Train_Number " \
                                      f"GROUP BY Train.Train_Name"

    # SQL query to retrieve passengers with confirmed status in the entered train
    query_passengers_by_train_name = f"SELECT distinct Passenger.* FROM Passenger " \
                                     f"JOIN Booked ON Passenger.SSN = Booked.Passenger_ssn " \
                                     f"JOIN Train ON Train.Train_Number = Booked.Train_Number " \
                                     f"WHERE Train.Train_Name = '{train_name}' AND Booked.Status = 'Booked'"

    result_trains = execute_query(query_trains)
    result_passengers = execute_query(query_passengers)
    result_passengers_by_age = execute_query(query_passengers_by_age)
    result_passengers_count_by_train = execute_query(query_passengers_count_by_train)
    result_passengers_by_train_name = execute_query(query_passengers_by_train_name)



    # Display the fetched train information in the GUI
    if result_trains:

        result_label_trains.config(text=f"Trains booked for {first_name} {last_name}")
        display_table_trains(result_trains)
    else:
        result_label_trains.config(text="No trains found for this passenger")

    # Display the fetched passenger information in the GUI
    if result_passengers:

        result_label_passengers.config(text=f"Passengers with booked status on {date}")
        display_table_passengers(result_passengers)
    else:
        result_label_passengers.config(text="No passengers found for this date")

    if result_passengers_by_age:


     display_table_age(result_passengers_by_age)
    else:
        result_label_passengers_by_age.config(text="No passengers found for this age range")

    # Display the fetched information in the GUI
    if result_passengers_count_by_train:
        # Prepare the result to display each row in a new line
        formatted_result_passengers_count_by_train = "\n".join(
            ", ".join(map(str, row)) for row in result_passengers_count_by_train)
        result_label_passengers_count_by_train.config(
            text=f"Train names along with passenger counts:\n{formatted_result_passengers_count_by_train}")
    else:
        result_label_passengers_count_by_train.config(text="No information found")

    if result_passengers_by_train_name:
        # Prepare the result to display each row in a new line
        formatted_result_passengers_by_train_name = "\n".join(
            ", ".join(map(str, row)) for row in result_passengers_by_train_name)
        result_label_passengers_by_train_name.config(
            text=f"Passengers with confirmed status in {train_name}:\n{formatted_result_passengers_by_train_name}")
    else:
        result_label_passengers_by_train_name.config(text="No passengers found for this train")

def display_table_passengers(result):
    table_window = tk.Toplevel(root)
    table_window.title("Booked Passenger Information by date")

    tree = ttk.Treeview(table_window)
    tree['columns'] = tuple(['First_Name', 'Last_Name', 'Address', 'City', 'County','Phone','SSN','Bdate'])  # Replace with your column names

    for col in tree['columns']:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col, anchor=tk.CENTER)

    for row in result:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill='both')

def display_table_trains(result):
    table_window = tk.Toplevel(root)
    table_window.title("Trains Information")

    tree = ttk.Treeview(table_window)
    tree['columns'] = tuple(['Train_Number', 'Train_Name', 'Source_Station', 'Destination_Station'])  

    for col in tree['columns']:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col, anchor=tk.CENTER)

    for row in result:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill='both')

def display_table_age(result):
    table_window = tk.Toplevel(root)
    table_window.title("Age related Information")

    tree = ttk.Treeview(table_window)
    tree['columns'] = tuple(['Train_Number', 'Train_Name', 'Source_Station', 'Destination_Station', 'Name','Address', 'Category', 'Status'])  # Replace with your column names

    for col in tree['columns']:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col, anchor=tk.CENTER)

    for row in result:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill='both')
# Function to open the cancel ticket window
def open_cancel_ticket_window():
    cancel_window = tk.Toplevel(root)
    cancel_window.title("Cancel Ticket and Confirm Waiting Passenger")

    def cancel_ticket():
        passenger_ssn = ssn_entry.get()
        train_number = train_number_entry.get()

        # Remove the canceled ticket record
        delete_query = f"DELETE FROM Booked WHERE Passenger_ssn = '{passenger_ssn}' AND Train_Number = '{train_number}'"
        execute_query(delete_query)

        # Find a passenger on the waiting list for that train
        waiting_passenger_query = f"SELECT Passenger_ssn FROM Booked WHERE Train_Number = '{train_number}' AND Status = 'WaitL' LIMIT 1"
        waiting_passenger = execute_query(waiting_passenger_query)

        if waiting_passenger:
            # Update the waiting passenger's status to 'confirmed'
            waiting_passenger_ssn = waiting_passenger[0][0]
            update_query = f"UPDATE Booked SET Status = 'confirmed' WHERE Passenger_ssn = '{passenger_ssn}' AND Train_Number = '{train_number}'"
            execute_query(update_query)

            result_label.config(
                text=f"Ticket canceled for {passenger_ssn}. Passenger {waiting_passenger_ssn} from the waiting list confirmed.")
        else:
            result_label.config(text=f"No waiting passengers for train {train_number}")

    global ssn_entry, train_number_entry, result_label

    # Input fields for Passenger SSN and Train Number
    ssn_label = tk.Label(cancel_window, text="Enter Passenger SSN:")
    ssn_label.pack()
    ssn_entry = tk.Entry(cancel_window)
    ssn_entry.pack()

    train_number_label = tk.Label(cancel_window, text="Enter Train Number:")
    train_number_label.pack()
    train_number_entry = tk.Entry(cancel_window)
    train_number_entry.pack()

    # Button to trigger canceling a ticket and confirming a waiting passenger
    cancel_button = tk.Button(cancel_window, text="Cancel Ticket", command=cancel_ticket)
    cancel_button.pack()

    # Label to display the result
    result_label = tk.Label(cancel_window, text="")
    result_label.pack()


root = tk.Tk()
root.title("Railway Reservation System")

# Customizing button font and appearance
button_font = font.Font(family='Helvetica', size=12, weight='bold')

# Section for retrieving trains booked by a specific passenger last name and first name
trains_frame = tk.Frame(root)
trains_frame.pack()

last_name_label = tk.Label(trains_frame, text="Enter Last Name:")
last_name_label.pack()
last_name_entry = tk.Entry(trains_frame)
last_name_entry.pack()

first_name_label = tk.Label(trains_frame, text="Enter First Name:")
first_name_label.pack()
first_name_entry = tk.Entry(trains_frame)
first_name_entry.pack()

query_button_trains = tk.Button(trains_frame, text="Retrieve Trains", command=handle_queries, font=button_font, bg="#3477eb", fg="blue")
query_button_trains.pack()

result_label_trains = tk.Label(trains_frame, text="", font=button_font)
result_label_trains.pack()

# Section for retrieving passengers with a specific booking date
passengers_frame = tk.Frame(root)
passengers_frame.pack()

date_label_passengers = tk.Label(passengers_frame, text="Enter Date (MM/DD/YY):")
date_label_passengers.pack()
date_entry = tk.Entry(passengers_frame)
date_entry.pack()

query_button_passengers = tk.Button(passengers_frame, text="Retrieve Passengers", command=handle_queries, font=button_font, bg="#3477eb", fg="blue")
query_button_passengers.pack()

result_label_passengers = tk.Label(passengers_frame, text="", font=button_font)
result_label_passengers.pack()


# # Section for retrieving passengers based on their age
# # Input fields for age range
passengers_by_age_frame = tk.Frame(root)
passengers_by_age_frame.pack()

age_start_label = tk.Label(passengers_by_age_frame, text="Enter age start")
age_start_label.pack()
age_start_entry = tk.Entry(passengers_by_age_frame)
age_start_entry.pack()

age_end_label = tk.Label(passengers_by_age_frame, text="Enter age end")
age_end_label.pack()
age_end_entry = tk.Entry(passengers_by_age_frame)
age_end_entry.pack()

# # Button to trigger query execution
query_button_passengers_by_age = tk.Button(passengers_by_age_frame, text="Retrieve passenger Information based on Ages`", command=handle_queries, font=button_font,fg="blue")
query_button_passengers_by_age.pack()

# # Label to display the query result
result_label_passengers_by_age = tk.Label(passengers_by_age_frame, text="")
result_label_passengers_by_age.pack()

# Section for retrieving Train and passengers count
passengers_count_by_train_frame = tk.Frame(root)
passengers_count_by_train_frame.pack()
# Button to trigger query execution
query_button_passengers_count_by_train = tk.Button(passengers_count_by_train_frame, text="Retrieve Information",
                                                   command=handle_queries,font=button_font,fg="blue")
query_button_passengers_count_by_train.pack()

# Label to display the query result
result_label_passengers_count_by_train = tk.Label(passengers_count_by_train_frame, text="")
result_label_passengers_count_by_train.pack()

# section to retrive passengers information by train name
passengers_by_train_name_frame = tk.Frame(root)
passengers_by_train_name_frame.pack()

# Input field for entering the train name
train_name_label = tk.Label(passengers_by_train_name_frame, text="Enter Train Name:")
train_name_label.pack()
train_name_entry = tk.Entry(passengers_by_train_name_frame)
train_name_entry.pack()
# Button to trigger query execution
query_button_passengers_by_train_name_frame = tk.Button(passengers_by_train_name_frame, text="Retrieve Passengers",
                                                        command=handle_queries, font=button_font,fg="blue")
query_button_passengers_by_train_name_frame.pack()

# Label to display the query result
result_label_passengers_by_train_name = tk.Label(passengers_by_train_name_frame, text="")
result_label_passengers_by_train_name.pack()

# cancel ticket
cancel_ticket_frame = tk.Frame(root)
cancel_ticket_frame.pack()
cancel_ticket_button = tk.Button(root, text="Cancel Ticket", command=open_cancel_ticket_window, font=button_font,fg="blue")
cancel_ticket_button.pack()

root.mainloop()
