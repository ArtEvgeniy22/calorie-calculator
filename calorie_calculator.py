import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import pymysql
from config import db_host, db_user, db_password, db_name

# Tkinter window
root = tk.Tk()
root.geometry('400x650')
root.title('Calorie Calculator')

# Active user
active_user = None
active_user_data = {}

# User's data
users = {}


# Log in screen
def login_screen():
    # Log in title
    title_reg = tk.Label(root, text='Log In', font='Arial 15 bold')
    title_reg.grid(row=0, column=1, sticky='we', columnspan=2, rowspan=2)
    # Name input
    name_title = tk.Label(text='Name', font='Arial 12')
    name_title.grid(row=2, column=0, sticky='we')
    name_input = tk.Entry()
    name_input.grid(row=2, column=1, sticky='we', columnspan=2)
    # Password input
    password_title = tk.Label(text='Password', font='Arial 12')
    password_title.grid(row=3, column=0, sticky='we')
    password_input = tk.Entry(show='*')
    password_input.grid(row=3, column=1, sticky='we', columnspan=2)
    # Log in button
    login_btn = tk.Button(text='Log In', background='#D3D3D3',
                          command=lambda: [login_checking(), login_destroy()])
    login_btn.grid(row=4, column=1, columnspan=2, sticky='we')
    # Sign in button
    signin_btn = tk.Button(text='Sign In', background='#D3D3D3',
                           command=lambda: [login_destroy(), signin_screen()])
    signin_btn.grid(row=5, column=1, columnspan=2, sticky='we')

    # Column settings
    root.grid_columnconfigure(0, minsize=100)
    root.grid_columnconfigure(1, minsize=100)
    root.grid_columnconfigure(2, minsize=100)
    root.grid_columnconfigure(3, minsize=100)

    # Row settings
    root.grid_rowconfigure(0, minsize=100)
    root.grid_rowconfigure(2, minsize=30)
    root.grid_rowconfigure(3, minsize=30)
    root.grid_rowconfigure(4, minsize=60)
    root.grid_rowconfigure(5, minsize=20)

    # Destroy login screen
    def login_destroy():
        title_reg.destroy()
        name_title.destroy()
        name_input.destroy()
        password_title.destroy()
        password_input.destroy()
        login_btn.destroy()
        signin_btn.destroy()

    # Log in checking
    def login_checking():
        name = name_input.get()
        password = password_input.get()

        # Checking name and password availability
        if name == '':
            if password == '':
                messagebox.showwarning('Attention!', 'Please, enter your name and password')
                login_screen()
                print('No name and password')
            else:
                messagebox.showwarning('Attention!', 'Please, enter your name')
                login_screen()
                print('No name')
        elif password == '':
            if name == '':
                messagebox.showwarning('Attention!', 'Please, enter your name and password')
                login_screen()
                print('No name and password')
            else:
                messagebox.showwarning('Attention!', 'Please, enter your password')
                login_screen()
                print('No password')
        else:
            # Log in (MySQL database)
            try:
                # Connection with the server
                connection = pymysql.connect(
                    host=db_host,
                    user=db_user,
                    port=3306,
                    password=db_password,
                    database=db_name,
                    cursorclass=pymysql.cursors.DictCursor
                )
                print('#' * 40)
                print()
                print('[INFO] Successfully connected.')
                print()
                print('#' * 40)

                # Taking users data from database
                try:
                    with connection.cursor() as cursor:
                        select_all_rows = "SELECT * FROM `accounts`"
                        cursor.execute(select_all_rows)

                        # Searching of user in database
                        rows = cursor.fetchall()
                        user_status = False
                        for row in rows:
                            if row['name'] == name:
                                if row['password'] == password:
                                    messagebox.showwarning('info', f'Hello, {name}!')
                                    user_status = True
                                    global active_user
                                    active_user = row['name']
                                    global active_user_data
                                    active_user_data = row
                                    print(f'Active user is {active_user}')
                                    print(active_user_data)
                                    main_screen()
                                    break
                                else:
                                    messagebox.showerror('info', f'Incorrect password')
                                    login_screen()
                                    user_status = True
                                    break
                            else:
                                user_status = False

                        if user_status:
                            pass
                        else:
                            messagebox.showerror('info', f'User is not found!')
                            login_screen()
                finally:
                    connection.close()

            except Exception as ex:
                print('[ERROR] Connection refused...')
                print(ex)


# Sign in screen
def signin_screen():
    # Sign in title
    title_signin = tk.Label(root, text='Sign In', font='Arial 15 bold')
    title_signin.grid(row=0, column=2, sticky='we', columnspan=2, rowspan=2)

    # Create name
    name_title_signin = tk.Label(text='Name:', font='Arial 10')
    name_title_signin.grid(row=2, column=1, sticky='e')
    name_input_signin = tk.Entry()
    name_input_signin.grid(row=2, column=3, sticky='we', columnspan=2)

    # Create password
    password_title_signin = tk.Label(text='Password:', font='Arial 10')
    password_title_signin.grid(row=3, column=1, sticky='e')
    password_input_signin = tk.Entry()
    password_input_signin.grid(row=3, column=3, sticky='we', columnspan=2)

    # Sex
    sex_var = tk.IntVar()

    def select_sex():
        sex_choice = sex_var.get()
        if sex_choice == 1:
            sex = 'Male'
            users['sex'] = sex
        else:
            sex = 'Female'
            users['sex'] = sex
    title_sex = tk.Label(root, text='Sex:', font='Arial 10')
    title_sex.grid(row=4, column=1, sticky='e')
    sex1 = tk.Radiobutton(text='Male', variable=sex_var, value=1, command=select_sex)
    sex1.grid(row=4, column=3, sticky='w')
    sex2 = tk.Radiobutton(text='Female', variable=sex_var, value=2, command=select_sex)
    sex2.grid(row=5, column=3, sticky='w')

    # Select body mass
    mass_title = tk.Label(text='Body weight:', font='Arial 10')
    mass_title.grid(row=6, column=1, sticky='e')
    mass_input = tk.Entry()
    mass_input.grid(row=6, column=3, sticky='we', columnspan=2)

    # Activity level
    activity_var = tk.IntVar()

    def select_activity():
        activity_choice = activity_var.get()
        if activity_choice == 3:
            activity = 'Extra active'
            users['activity'] = activity
        elif activity_choice == 4:
            activity = 'Very active'
            users['activity'] = activity
        elif activity_choice == 5:
            activity = 'Moderately active'
            users['activity'] = activity
        elif activity_choice == 6:
            activity = 'Lightly active'
            users['activity'] = activity
        else:
            activity = 'Sedentary'
            users['activity'] = activity
    activity_title = tk.Label(text='Activity:', font='Arial 10')
    activity_title.grid(row=7, column=1, sticky='e')
    a1 = tk.Radiobutton(text='Extra active', variable=activity_var, value=3, command=select_activity)
    a1.grid(row=7, column=3, sticky='w')
    a2 = tk.Radiobutton(text='Very active', variable=activity_var, value=4, command=select_activity)
    a2.grid(row=8, column=3, sticky='w')
    a3 = tk.Radiobutton(text='Moderately active', variable=activity_var, value=5, command=select_activity)
    a3.grid(row=9, column=3, sticky='w')
    a4 = tk.Radiobutton(text='Lightly active', variable=activity_var, value=6, command=select_activity)
    a4.grid(row=10, column=3, sticky='w')
    a5 = tk.Radiobutton(text='Sedentary', variable=activity_var, value=7, command=select_activity)
    a5.grid(row=11, column=3, sticky='w')

    # Goal
    goal_var = tk.IntVar()

    def select_goal():
        goal_choice = goal_var.get()
        if goal_choice == 1:
            goal = 'Gain weight'
            users['goal'] = goal
        elif goal_choice == 2:
            goal = 'Keep fit'
            users['goal'] = goal
        else:
            goal = 'Lose weight'
            users['goal'] = goal
    goal_title = tk.Label(text='Your goal:', font='Arial 10')
    goal_title.grid(row=13, column=1, sticky='e')
    goal1 = tk.Radiobutton(text='Gain weight', variable=goal_var, value=1, command=select_goal)
    goal1.grid(row=13, column=3, sticky='w')
    goal2 = tk.Radiobutton(text='Keep fit', variable=goal_var, value=2, command=select_goal)
    goal2.grid(row=14, column=3, sticky='w')
    goal3 = tk.Radiobutton(text='Lose weight', variable=goal_var, value=3, command=select_goal)
    goal3.grid(row=15, column=3, sticky='w')

    # Height
    height_title = tk.Label(text='Height (cm):', font='Arial 10')
    height_title.grid(row=16, column=1, sticky='e')
    height_input = tk.Entry()
    height_input.grid(row=16, column=3, sticky='we', columnspan=2)

    # Age
    age_title = tk.Label(text='Your age:', font='Arial 10')
    age_title.grid(row=17, column=1, sticky='e')
    age_input = tk.Entry()
    age_input.grid(row=17, column=3, sticky='we', columnspan=2)

    # Registration button
    signin_btn = tk.Button(text='Sign In', background='#D3D3D3',
                           command=lambda: [load_data(), signin_destroy(), login_screen()])
    signin_btn.grid(row=18, column=2, columnspan=2, sticky='we')

    # Column settings
    root.grid_columnconfigure(0, minsize=50)
    root.grid_columnconfigure(1, minsize=50)
    root.grid_columnconfigure(2, minsize=50)
    root.grid_columnconfigure(3, minsize=50)
    root.grid_columnconfigure(4, minsize=50)
    root.grid_columnconfigure(5, minsize=50)
    root.grid_columnconfigure(6, minsize=50)
    root.grid_columnconfigure(7, minsize=50)

    # Row settings
    root.grid_rowconfigure(0, minsize=100)
    root.grid_rowconfigure(2, minsize=30)
    root.grid_rowconfigure(3, minsize=30)
    root.grid_rowconfigure(4, minsize=30)
    root.grid_rowconfigure(5, minsize=30)
    root.grid_rowconfigure(6, minsize=30)
    root.grid_rowconfigure(7, minsize=30)
    root.grid_rowconfigure(8, minsize=30)
    root.grid_rowconfigure(9, minsize=30)
    root.grid_rowconfigure(10, minsize=30)
    root.grid_rowconfigure(11, minsize=30)
    root.grid_rowconfigure(12, minsize=30)
    root.grid_rowconfigure(13, minsize=30)
    root.grid_rowconfigure(14, minsize=30)
    root.grid_rowconfigure(15, minsize=30)
    root.grid_rowconfigure(16, minsize=30)
    root.grid_rowconfigure(17, minsize=30)
    root.grid_rowconfigure(18, minsize=60)

    # Destroy registration screen
    def signin_destroy():
        title_signin.destroy()
        name_title_signin.destroy()
        name_input_signin.destroy()
        password_title_signin.destroy()
        password_input_signin.destroy()
        title_sex.destroy()
        sex1.destroy()
        sex2.destroy()
        mass_title.destroy()
        mass_input.destroy()
        activity_title.destroy()
        a1.destroy()
        a2.destroy()
        a3.destroy()
        a4.destroy()
        a5.destroy()
        goal_title.destroy()
        goal1.destroy()
        goal2.destroy()
        goal3.destroy()
        height_title.destroy()
        height_input.destroy()
        age_title.destroy()
        age_input.destroy()
        signin_btn.destroy()

    # Data uploading
    def load_data():
        users['name'] = name_input_signin.get()
        users['password'] = password_input_signin.get()
        users['mass'] = mass_input.get()
        users['height'] = height_input.get()
        users['age'] = age_input.get()

        # Data uploading (MySQL database)
        try:
            connection = pymysql.connect(
                host=db_host,
                user=db_user,
                port=3306,
                password=db_password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )

            print('#' * 40)
            print()
            print('[INFO] Successfully connected.')
            print()
            print('#' * 40)

            try:
                # Insert data
                with connection.cursor() as cursor:
                    data = "INSERT INTO `accounts` (name, password, sex, mass, activity, goal, height, age)" \
                           f" VALUES ('{users['name']}', '{users['password']}', '{users['sex']}', '{users['mass']}'," \
                           f" '{users['activity']}', '{users['goal']}', '{users['height']}', '{users['age']}');"
                    cursor.execute(data)
                    connection.commit()

                # Print all users in database
                print('All users:')
                with connection.cursor() as cursor:
                    select_all_rows = "SELECT * FROM `accounts`"
                    cursor.execute(select_all_rows)

                    rows = cursor.fetchall()
                    for row in rows:
                        print(row)
            finally:
                connection.close()

        except Exception as ex:
            print('[ERROR] Connection refused...')
            print(ex)

        # Data uploading (CSV-file)
        '''file = open('data.csv', 'a')
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            [users['name'], users['password'], users['sex'], users['mass'], users['activity'], users['goal']]
        )
        print(f'[INFO] User {users["name"]} is created.')'''


# Main screen
def main_screen():
    try:
        # Connection with the server
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            port=3306,
            password=db_password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        # Taking users data from database
        try:
            with connection.cursor() as cursor:
                select_all_rows = "SELECT * FROM `accounts`"
                cursor.execute(select_all_rows)

                # Searching of user in database
                rows = cursor.fetchall()
                for row in rows:
                    if row['name'] == active_user:

                        # Frames
                        frame_data = tk.Frame(root, bg='#F0F0F0', padx=10, pady=10,
                                              highlightbackground="black", highlightthickness=1)
                        frame_add_food = tk.Frame(root, bg='#F0F0F0', padx=10, pady=10,
                                                  highlightbackground="black", highlightthickness=0.5)
                        frame_food_table = tk.Frame(root, bg='#F0F0F0',
                                                    highlightbackground="black", highlightthickness=0.5)

                        frame_data.grid(row=0, column=0, columnspan=2, sticky='we')
                        frame_add_food.grid(row=1, column=0, columnspan=2, sticky='we')
                        frame_food_table.grid(row=2, column=0, columnspan=2, sticky='we')

                        # Body weight index calculation
                        def bwi(mass, height):
                            index = round(mass / ((height / 100) ** 2), 1)
                            return index

                        # BMR calculation
                        def bmr(sex, mass, height, age):
                            if sex == 'Male':
                                bmr_val = 88.362 + (13.397 * mass) + (4.799 * height) + (5.677 * age)
                            else:
                                bmr_val = 447.593 + (9.247 * mass) + (3.097 * height) + (4.33 * age)
                            return round(bmr_val, 2)

                        # Daily amount of calories calculation
                        def dac(activity):
                            if activity == 'Extra active':
                                dac_val = bmr(row['sex'], row['mass'], row['height'], row['age']) * 1.9
                            elif activity == 'Very active':
                                dac_val = bmr(row['sex'], row['mass'], row['height'], row['age']) * 1.725
                            elif activity == 'Moderately active':
                                dac_val = bmr(row['sex'], row['mass'], row['height'], row['age']) * 1.55
                            elif activity == 'Lightly active':
                                dac_val = bmr(row['sex'], row['mass'], row['height'], row['age']) * 1.375
                            else:
                                dac_val = bmr(row['sex'], row['mass'], row['height'], row['age']) * 1.2
                            return round(dac_val, 2)

                        # Body weight index
                        bwi_title = tk.Label(frame_data, text='Body weight index:', font='Arial 11')
                        bwi_title.grid(row=0, column=1, padx=10, pady=10)
                        bwi_value = tk.Label(frame_data, text=bwi(row['mass'], row['height']),
                                             font='Arial 11', fg='blue')
                        bwi_value.grid(row=0, column=2, padx=10, pady=10)

                        # BMR
                        bmr_title = tk.Label(frame_data, text='BMR:', font='Arial 11')
                        bmr_title.grid(row=1, column=1, padx=10, pady=10)
                        bmr_value = tk.Label(frame_data, text=bmr(row['sex'], row['mass'], row['height'], row['age']),
                                             font='Arial 11', fg='blue')
                        bmr_value.grid(row=1, column=2, padx=10, pady=10)

                        # Daily amount of calories
                        dac_title = tk.Label(frame_data, text='Daily calories:', font='Arial 11')
                        dac_title.grid(row=2, column=1, padx=10, pady=10)
                        dac_value = tk.Label(frame_data, text=dac(row['activity']), font='Arial 11', fg='red')
                        dac_value.grid(row=2, column=2, padx=10, pady=10)

                        # Back button
                        back_btn = ttk.Button(frame_data, text='Back', command=lambda: [main_screen_destroy(),
                                                                                        login_screen()])
                        back_btn.grid(row=0, column=0, padx=10, pady=10)

                        # Uploading of food data
                        def upload_food_data():
                            # Checking filled areas
                            if food_name_input.get() and calendar.get() and amount_input.get() \
                                    and calories_input.get() != '':

                                food = food_name_input.get()
                                date = calendar.get()
                                amount = round(float(amount_input.get()))
                                calories = round(float(calories_input.get()))
                                print(f"{food} is saved")

                                # Connection with the server
                                try:
                                    connection_2 = pymysql.connect(
                                        host=db_host,
                                        user=db_user,
                                        port=3306,
                                        password=db_password,
                                        database=db_name,
                                        cursorclass=pymysql.cursors.DictCursor
                                    )
                                    # Connection with the table 'menu'
                                    try:
                                        with connection_2.cursor() as cursor_2:
                                            food_data = "INSERT INTO `menu` (user_id, food, date, amount, calories)" \
                                                        f" VALUES ('{active_user_data['id']}', '{food}'," \
                                                        f" '{date}', '{amount}', '{calories}');"
                                            cursor_2.execute(food_data)
                                            connection_2.commit()

                                            # Searching of user in database
                                            menu_rows = cursor_2.fetchall()
                                            for meal in menu_rows:
                                                print(meal)
                                    finally:
                                        connection_2.close()

                                except Exception as ex_2:
                                    print(ex_2)
                            else:
                                messagebox.showwarning('Attention!', 'Please, fill all inputs')

                        # ADD FOOD
                        add_food_title = ttk.Label(frame_add_food, text='Add food', font='Arial 12')
                        add_food_title.grid(row=0, column=1, padx=10, pady=10)
                        # Food name
                        food_name = ttk.Label(frame_add_food, text='Food:', font='Arial 11')
                        food_name.grid(row=1, column=0, padx=10, pady=10, sticky='e')
                        food_name_input = ttk.Entry(frame_add_food)
                        food_name_input.grid(row=1, column=2, padx=10, pady=10, sticky='e')
                        # Date
                        date_title = ttk.Label(frame_add_food, text='Date:', font='Arial 11')
                        date_title.grid(row=2, column=0, padx=10, pady=10, sticky='e')
                        calendar = DateEntry(frame_add_food, date_pattern='YYYY-mm-dd')
                        calendar.grid(row=2, column=2, padx=10, pady=10, sticky='e')
                        # Amount
                        amount_title = ttk.Label(frame_add_food, text='Amount (g):', font='Arial 11')
                        amount_title.grid(row=3, column=0, padx=10, pady=10, sticky='e')
                        amount_input = ttk.Entry(frame_add_food)
                        amount_input.grid(row=3, column=2, padx=10, pady=10, sticky='e')
                        # Calories per 100g
                        calories_title = ttk.Label(frame_add_food, text='Calories per 100g:', font='Arial 11')
                        calories_title.grid(row=4, column=0, padx=10, pady=10, sticky='e')
                        calories_input = ttk.Entry(frame_add_food)
                        calories_input.grid(row=4, column=2, padx=10, pady=10, sticky='e')
                        # Save button
                        submit_btn = ttk.Button(frame_add_food, text='Submit', command=upload_food_data)
                        submit_btn.grid(row=5, column=1, padx=10, pady=10)
                        # Update button
                        update_btn = ttk.Button(frame_add_food, text='Update', command=main_screen)
                        update_btn.grid(row=5, column=2, padx=10, pady=10)

                        # HISTORY TABLE

                        # Creating table
                        table = ttk.Treeview(frame_food_table, show='headings')
                        table.pack(expand=tk.YES, fill=tk.BOTH)
                        heads = ['food', 'date', 'amount', 'calories']
                        table['columns'] = heads

                        # Scrolling
                        scroll_pane = ttk.Scrollbar(frame_food_table, command=table.yview)
                        table.configure(yscrollcommand=scroll_pane.set)
                        scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)

                        # Some style
                        style = ttk.Style()
                        style.theme_use('clam')
                        style.configure('Treeview', background='#D4D4D4', foreground='black',
                                        filedbackground='#D4D4D4')
                        style.map('Treeview', background=[('selected', 'blue')])

                        for header in heads:
                            table.heading(header, text=header, anchor='center')
                            table.column(header, anchor='center', width=30)

                        # Connection with the server
                        try:
                            connection_3 = pymysql.connect(
                                host=db_host,
                                user=db_user,
                                port=3306,
                                password=db_password,
                                database=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                            )
                            # Connection with the table 'menu'
                            try:
                                with connection_3.cursor() as cursor_3:
                                    taken_food_data = "SELECT * FROM `menu`"
                                    cursor_3.execute(taken_food_data)

                                    food_rows = cursor_3.fetchall()
                                    food_rows.reverse()
                                    for food_row in food_rows:
                                        if active_user_data['id'] == food_row['user_id']:
                                            table.insert('', tk.END, values=(food_row['food'],
                                                                             food_row['date'], food_row['amount'],
                                                                             food_row['calories']))
                            finally:
                                connection_3.close()

                        except Exception as ex_3:
                            print(ex_3)

                        # Main screen destroying
                        def main_screen_destroy():
                            frame_data.destroy()
                            frame_food_table.destroy()
                            frame_add_food.destroy()
                            bwi_title.destroy()
                            bwi_value.destroy()
                            bmr_title.destroy()
                            bmr_value.destroy()
                            dac_title.destroy()
                            dac_value.destroy()
                            back_btn.destroy()
                            add_food_title.destroy()
                            food_name.destroy()
                            food_name_input.destroy()
                            date_title.destroy()
                            calendar.destroy()
                            amount_title.destroy()
                            amount_input.destroy()
                            calories_title.destroy()
                            calories_input.destroy()
                            submit_btn.destroy()
                            update_btn.destroy()
                            table.destroy()
                            scroll_pane.destroy()

        finally:
            connection.close()

    except Exception as ex:
        print('[ERROR] Connection refused...')
        print('[ERROR] Server is not active right now')
        print(ex)


def main():
    login_screen()
    root.mainloop()


if __name__ == '__main__':
    main()
