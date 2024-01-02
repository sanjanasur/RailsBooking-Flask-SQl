import tkinter as tk
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import font
from tkinter import ttk
from datetime import datetime, timedelta

# Establish a connection to the SQLite database and create a cursor
conn = sqlite3.connect('railway_reservation.db')
cursor = conn.cursor()

# Function to execute SQL queries based on user input
def execute_query(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result

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

def display_table_passengers(result):
    table_window = tk.Toplevel(root)
    table_window.title("Booked Passenger Information ")

    tree = ttk.Treeview(table_window)
    tree['columns'] = tuple(['first_name', 'last_name', 'address', 'city', 'county','phone','SSN','bdate'])  # Replace with your column names

    for col in tree['columns']:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col, anchor=tk.CENTER)

    for row in result:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill='both')

def display_table_passengers_count_by_train(result):
    table_window = tk.Toplevel(root)
    table_window.title("Trains and count of passengers")

    tree = ttk.Treeview(table_window)
    tree['columns'] = tuple(['Trian_Name', 'Count of Passengers'])  # Replace with your column names

    for col in tree['columns']:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col, anchor=tk.CENTER)

    for row in result:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill='both')

def display_table_passengers_by_age(result):
    table_window = tk.Toplevel(root)
    table_window.title("Booked Passenger Information ")

    tree = ttk.Treeview(table_window)
    tree['columns'] = tuple(['Train_Number', 'Train_Name', 'Source_Station','Destination_Station','Passenger_Name','Address','Ticket_type','Status'])  # Replace with your column names

    for col in tree['columns']:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col, anchor=tk.CENTER)

    for row in result:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=True, fill='both')











def handle_queries(last_name_entry, first_name_entry,result_label_trains):
    last_name = last_name_entry.get()
    first_name = first_name_entry.get()
    



    # SQL query to retrieve trains a passenger is booked on based on last name and first name
    query_trains = f"SELECT DISTINCT Train.Train_Number, Train.Train_Name, Train.Source_Station, Destination_Station FROM Train " \
                   f"JOIN Booked ON Train.Train_Number = Booked.Train_Number " \
                   f"JOIN Passenger ON Booked.Passenger_ssn = Passenger.SSN " \
                   f"WHERE Passenger.last_name = '{last_name}' AND Passenger.first_name = '{first_name}'"
    result_trains = execute_query(query_trains)
     # Display the fetched train information in the GUI
    if result_trains:

        result_label_trains.config(text=f"Trains booked for {first_name} {last_name}")
        display_table_trains(result_trains)
    else:
        result_label_trains.config(text="No trains found for this passenger")









    # if result_trains:
    #     formatted_result_trains = "\n".join(", ".join(map(str, row)) for row in result_trains)
    #     result_label_trains.config(text=f"Trains booked for {first_name} {last_name}:\n{formatted_result_trains}")
    # else:
    #     result_label_trains.config(text="No trains found for this passenger")

def handle_queries2(date_entry,result_label_passengers_by_date):

    date = date_entry.get()
    
    # Format the date to 'YYYY-MM-DD' format
    try:
        formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")
    except ValueError:
       result_label_passengers_by_date.config(text="Invalid date format. Please use MM/DD/YY.")
       return
    
    
    query_passengers =f"SELECT DISTINCT Passenger.* "\
f"FROM Passenger "\
f"JOIN Booked ON Passenger.SSN = Booked.Passenger_ssn "\
f"JOIN Train ON Booked.Train_Number = Train.Train_Number "\
f"JOIN Train_Status ON Train.Train_Name = Train_Status.TrainName "\
f"WHERE Train_Status.TrainDate = '{formatted_date}' AND Booked.Status = 'Booked'"

    result_passengers_by_date = execute_query(query_passengers)
    if result_passengers_by_date:

        result_label_passengers_by_date.config(text=f"Passengers with booked status on {date}")
        display_table_passengers(result_passengers_by_date)
    else:
        result_label_passengers_by_date.config(text="No passengers found for this date")
    

def handle_queries3(result_label_passengers_count_by_train):
    query_passengers_count_by_train = f"SELECT Train.Train_Name, COUNT(Booked.Passenger_ssn) AS Passenger_Count " \
                                      f"FROM Train " \
                                      f"LEFT JOIN Booked ON Train.Train_Number = Booked.Train_Number " \
                                      f"GROUP BY Train.Train_Name"
    result_passengers_count_by_train = execute_query(query_passengers_count_by_train)

    if result_passengers_count_by_train:
        # Prepare the result to display each row in a new line
        display_table_passengers_count_by_train(result_passengers_count_by_train)
    else:
        result_label_passengers_count_by_train.config(text="No information found")


def handle_queries4(train_name_entry,result_label_passengers_by_train_name):

    train_name = train_name_entry.get()
    query_passengers_by_train_name = f"SELECT distinct Passenger.* FROM Passenger " \
            f"JOIN Booked ON Passenger.SSN = Booked.Passenger_ssn " \
            f"JOIN Train ON Train.Train_Number = Booked.Train_Number " \
            f"WHERE Train.Train_Name = '{train_name}' AND Booked.Status = 'Booked'"
    
    result_passengers_by_train_name = execute_query(query_passengers_by_train_name)
    
    if result_passengers_by_train_name:
        # Prepare the result to display each row in a new line
    #     formatted_result_passengers_by_train_name = "\n".join(", ".join(map(str, row)) for row in result_passengers_by_train_name)
    #     result_label_passengers_by_train_name.config(text=f"Passengers with confirmed status in {train_name}:\n{formatted_result_passengers_by_train_name}")
          display_table_passengers(result_passengers_by_train_name)
    
    else:
        result_label_passengers_by_train_name.config(text="No passengers found for this train")

def handle_queries5(age_start_entry, age_end_entry,result_label_trains):
    age_start = int(age_start_entry.get())
    age_end = int(age_end_entry.get())
    



    # SQL query to retrieve trains a passenger is booked on based on last name and first name
    query_passengers_by_age = f"SELECT DISTINCT Train.Train_Number, Train.Train_Name, Train.Source_Station, Train.Destination_Station, " \
         f"Passenger.first_name || ' ' || Passenger.last_name AS Name, " \
         f"Passenger.address, Booked.Ticket_Type, Booked.Status " \
         f"FROM Passenger " \
         f"JOIN Booked ON Passenger.SSN = Booked.Passenger_ssn " \
         f"JOIN Train ON Train.Train_Number = Booked.Train_Number " \
         f"WHERE CAST(strftime('%Y', 'now') AS INTEGER) - CAST('19' || substr(bdate, -2) AS INTEGER) BETWEEN {age_start} AND {age_end}"
    query1 = f"SELECT * FROM Booked"
    print(query1)


    result_passengers_by_age = execute_query(query_passengers_by_age)
     # Display the fetched train information in the GUI

    if result_passengers_by_age:
        # formatted_passenger_info = "\n".join(", ".join(map(str, row)) for row in result_passengers_by_age)
        # result_label_trains.config(text=f"Passenger Information (Age 50-60):\n{formatted_passenger_info}")
        display_table_passengers_by_age(result_passengers_by_age)
    else:
        result_label_trains.config(text="No passengers found in this age range")





# Function to open the cancel ticket window
def open_cancel_ticket_window():
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

            result_label.config(text=f"Ticket canceled for {passenger_ssn}. Passenger {waiting_passenger_ssn} from the waiting list confirmed.")
        else:
            result_label.config(text=f"No waiting passengers for train {train_number}")

    cancel_window = tk.Toplevel(root)
    cancel_window.title("Cancel Ticket and Confirm Waiting Passenger")

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




# GUI setup
root = tk.Tk()
root.title("")  # Clear the default title

    # Custom title label with different colors and fonts
title_label = tk.Label(root, text="RailsBooking System", font=("Arial", 20, "bold"), fg="black")
title_label.pack()

# Load the image (Replace 'train.gif' with the path to your image)
train_image = tk.PhotoImage(file=r'/Users/sanjana/Desktop/railwayReservation/gui/CHATTANOOGA-GIF2.gif')

# Create a label to display the image
image_label = tk.Label(root, image=train_image)
image_label.pack()


# def create_clickable_frame(parent, text, click_handler):
#     frame = tk.Frame(parent, bd=1, relief=tk.RAISED, width=200, height=30)
#     frame.pack(pady=5)

#     label = tk.Label(frame, text=text, cursor="hand2")
#     label.pack(expand=True, fill='both')
#     label.bind("<Button-1>", click_handler)
    
#     return frame

def create_clickable_frame(parent, text, click_handler):
    frame = tk.Frame(parent, bd=1, relief=tk.RAISED, width=300, height=50)  # Increase width and height for a bigger size
    frame.pack(pady=10)

    label = tk.Label(frame, text=text, cursor="hand2", fg="blue")  # Set text color to blue (or any other color)
    label.config(font=("Arial", 12))  # Set font size
    label.pack(expand=True, fill='both')
    label.bind("<Button-1>", click_handler)
    
    return frame




def on_trains_by_names_click(event):
    # Function to handle click on 'Trains' frame
    # Open a new window for 'Trains' functionality
    trains_window = tk.Toplevel(root)
    trains_window.title("Trains Information by Passenger names ")

    # Create UI elements for 'Trains' functionality in the new window
    first_name_label = tk.Label(trains_window, text="Enter First Name:")
    first_name_label.pack()

    first_name_entry = tk.Entry(trains_window)
    first_name_entry.pack()

    last_name_label = tk.Label(trains_window, text="Enter Last Name:")
    last_name_label.pack()

    last_name_entry = tk.Entry(trains_window)
    last_name_entry.pack()
        
    result_label_trains = tk.Label(trains_window, text="")
    result_label_trains.pack()

    query_button_trains = tk.Button(trains_window, text="Retrieve Trains", command=lambda: handle_queries(last_name_entry, first_name_entry, result_label_trains))
    query_button_trains.pack()

def on_trains_by_date_click(event):
    # Function to handle click on 'Trains' frame
    # Open a new window for 'Trains' functionality
    trains_window = tk.Toplevel(root)
    trains_window.title("Trains Information by Date")

    date_label_passengers = tk.Label(trains_window, text="Enter Date (MM/DD/YY):")
    date_label_passengers.pack()
    date_entry = tk.Entry(trains_window)
    date_entry.pack()

    result_label_passengers_by_date = tk.Label(trains_window, text="")
    result_label_passengers_by_date.pack()

    query_button_passengers = tk.Button(trains_window, text="Retrieve Passengers count by Travel date", command=lambda: handle_queries2(date_entry,result_label_passengers_by_date))
    query_button_passengers.pack()

def on_trains_by_count_click(event):
    # Function to handle click on 'Trains' frame
    # Open a new window for 'Trains' functionality
    trains_window = tk.Toplevel(root)
    trains_window.title("Trains Names and count of passengers")



    result_label_passengers_count_by_train = tk.Label(trains_window, text="")
    result_label_passengers_count_by_train.pack()

    query_button_passengers = tk.Button(trains_window, text="Retrieve Passengers", command=lambda: handle_queries3(result_label_passengers_count_by_train))
    query_button_passengers.pack()

def on_passengers_by_train_name_click(event):
    # Function to handle click on 'Trains' frame
    # Open a new window for 'Trains' functionality
    trains_window = tk.Toplevel(root)
    trains_window.title("Passengers Information by train name")

    train_name_label = tk.Label(trains_window, text="Enter Train Name:")
    train_name_label.pack()
    train_name_entry = tk.Entry(trains_window)
    train_name_entry.pack()

    result_label_passengers_by_train_name = tk.Label(trains_window, text="")
    result_label_passengers_by_train_name.pack()

    query_button_passengers_by_train_name = tk.Button(trains_window, text="Retrieve Passengers(confirmed) count by train names", command=lambda: handle_queries4(train_name_entry,result_label_passengers_by_train_name))
    query_button_passengers_by_train_name.pack()

def on_passengers_by_age_click(event):

    trains_window = tk.Toplevel(root)
    trains_window.title("Passengers Information by Age ")

    age_start_label = tk.Label(trains_window, text="Enter age start")
    age_start_label.pack()
    age_start_entry = tk.Entry(trains_window)
    age_start_entry.pack()

    age_end_label = tk.Label(trains_window, text="Enter age end")
    age_end_label.pack()
    age_end_entry = tk.Entry(trains_window)
    age_end_entry.pack()
        
    result_label_trains = tk.Label(trains_window, text="")
    result_label_trains.pack()

    query_button_trains = tk.Button(trains_window, text="Retrieve Trains", command=lambda: handle_queries5(age_start_entry, age_end_entry, result_label_trains))
    query_button_trains.pack()

def on_cancel_ticket_click(event):
    open_cancel_ticket_window()
   


# Section for retrieving trains booked by a specific passenger last name and first name
# Create a containing frame for the frames to be positioned side by side
# Create a containing frame for the frames to be positioned with space between them
side_by_side_frame = tk.Frame(root)
side_by_side_frame.pack()

# Create the first clickable frame and place it in the containing frame
trains_frame_1 = create_clickable_frame(side_by_side_frame, "Trains By passenger names", on_trains_by_names_click)
trains_frame_1.pack(side=tk.LEFT, padx=10)

# Create a spacer frame for additional space between the frames
spacer_frame = tk.Frame(side_by_side_frame, width=20)
spacer_frame.pack(side=tk.LEFT)

# Create the second clickable frame and place it in the containing frame
trains_frame_2 = create_clickable_frame(side_by_side_frame, "Trains By date", on_trains_by_date_click)
trains_frame_2.pack(side=tk.LEFT, padx=10)

spacer_frame = tk.Frame(side_by_side_frame, width=20)
spacer_frame.pack(side=tk.LEFT)

trains_frame_3 = create_clickable_frame(side_by_side_frame, "Trains By Count of passengers", on_trains_by_count_click)
trains_frame_3.pack(side=tk.LEFT, padx=10)

spacer_frame = tk.Frame(side_by_side_frame, width=20)
spacer_frame.pack(side=tk.LEFT)

trains_frame_4 = create_clickable_frame(side_by_side_frame, "Passengers by Train Name", on_passengers_by_train_name_click)
trains_frame_4.pack(side=tk.LEFT, padx=10)

spacer_frame = tk.Frame(side_by_side_frame, width=20)
spacer_frame.pack(side=tk.LEFT)

trains_frame_5 = create_clickable_frame(side_by_side_frame, "Passengers by Age", on_passengers_by_age_click)
trains_frame_5.pack(side=tk.LEFT, padx=10)


#cancel ticket
cancel_ticket_frame = create_clickable_frame(side_by_side_frame, "Cancel Ticket", on_cancel_ticket_click)
cancel_ticket_frame.pack(side=tk.LEFT, padx=10)




root.mainloop()

