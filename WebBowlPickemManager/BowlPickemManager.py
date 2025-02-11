import datetime
import tkinter as tk
import array
import pyodbc
import random
from Team import Team
from TeamPick import TeamPick
from Matchup import Matchup
from typing import List, Any
from tkinter import simpledialog, messagebox

class TeamApp:
        
    currentYear = 2024
    
    def __init__(self, root):
        self.root = root
        self.root.title("Team Apps")

        #self.team = Team
        #self.team_pick = TeamPick
        #self.matchup = Matchup

        self.entry_boxes = []
        self.selected_teams = []
        self.entered_values = []

        self.teams: List[Team] = []
        self.database_teams: List[Team] = []
        self.team_picks: List[TeamPick] = []
        self.database_team_picks: List[TeamPick] = []
        self.available_items = []
        self.matchups: List[Matchup] = []
        self.databaseMatchups: List[Matchup] = []
        
        self.current_scores_listbox = tk.Listbox(root)
        self.current_scores_listbox.pack(side="bottom", fill="both", expand=True, anchor=tk.SW, pady=20, padx=20)

        self.team_listbox = tk.Listbox(root, height = 20)
        self.team_listbox.pack(side="left", fill="both", expand=True, anchor=tk.N)
        self.team_listbox.bind("<<ListboxSelect>>", self.on_select)
        
        self.team_selection_listbox = tk.Listbox(root, height = 20)
        self.team_selection_listbox.pack(side="left", fill="both", expand=True, anchor=tk.N)

        self.add_team_button = tk.Button(root, text="Add Team", command=self.add_team)
        self.add_team_button.pack(side="top", fill="x")

        self.add_items_button = tk.Button(root, text="Add Items", command=self.add_items)
        self.add_items_button.pack(side="top", fill="x")

        self.add_item_to_team_button = tk.Button(root, text="Add Item to Team", command=self.add_item_to_team)
        self.add_item_to_team_button.pack(side="top", fill="x")

        self.show_teams_button = tk.Button(root, text="Save", command=self.save)
        self.show_teams_button.pack(side="top", fill="x")
        
        server = ''  # Or server address/instance name
        database = 'master'
        
        
        try:
            
            # Establish the connection
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes' # Use appropriate driver
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()
            
             # Fetch all the teams playing for the current year
            self.load_teams(cursor)

            # Fetch all the game selections for the current year
            self.load_game_selections(cursor)

        
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '28000':
                print("Invalid credentials")
            else:
                print(f"Error connecting to or fetching data: {ex}")
        except Exception as e:
            print(f"A general exception occurred: {e}")
        finally:
            if cnxn:
                cursor.close()
                cnxn.close()
                
    def load_teams(self, cursor):
        sql = f"SELECT * FROM dbo.Team WHERE YearPlaying = {TeamApp.currentYear}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for team in rows:
            self.team_listbox.insert("end", team.TeamName)
            self.team = Team(team.TeamIdentifier, team.TeamName, team.CurrentPoints, team.MaxPoints, team.YearPlaying)
            if team not in self.teams:
                self.database_teams.append(team)
                self.teams.append(team)
                
    def load_game_selections(self, cursor):
        sql = f"SELECT * FROM dbo.TeamPick WHERE YearPlaying = {TeamApp.currentYear}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for pick in rows:
            if pick.TeamIdentifier == self.team.teamId:
                self.team_selection_listbox.insert("end", f"{pick.PointValue}: {pick.TeamSelection}: {pick.IsCorrect}")
                self.team_pick = TeamPick(pick.PickIdentifier, pick.TeamIdentifier, pick.GameNumber, pick.TeamSelection, pick.PointValue, pick.IsCorrect, pick.YearPlaying)
                if pick not in self.team_picks:
                    self.database_team_picks.append(pick)
                    self.team_picks.append(pick)
                    
    def load_matchups(self, cursor):
        sql = f"SELECT * FROM dbo.Matchups WHERE YearPlaying = {TeamApp.currentYear}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for match in rows:
            self.matchup = Matchup(match.MatchupIdentifier, match.GameNumber, match.TeamOne, match.TeamTwo, match.Winner, match.YearPlaying)
            if match not in self.matchups:
                self.databaseMatchups.append(match)
                self.matchups.append(match)

    def on_select(self, event):
        # Get the index of the selected item
        selection = self.team_listbox.curselection()
        if selection:
            index = selection[0]
            # Get the value of the selected item
            value = self.team_listbox.get(index)
            selected_team = next((team for team in self.teams if team.TeamName == value), None)
            #print("Selected item:", value)
            for game in self.team_picks:
                if game.TeamIdentifier == selected_team.TeamIdentifier:
                    # Go through Team Picks here
                    
                    value = game.pointValue
                    selection = game.teamSelection
                    isCorrect = game.isCorrect
                    self.team_selection_listbox.insert("end", f"{value}:  {selection}:: {isCorrect}")

    def add_team(self):
        team_name = simpledialog.askstring("Team Name", "Enter the team name:")
        if team_name:
            self.team = Team(random.getrandbits(6),team_name, 0, 0, datetime.datetime.today().year-1)
            team = Team(self.team.teamId, self.team.teamName, self.team.currentPoints, self.team.maxPoints, self.team.yearPlaying)
            if team not in self.teams:
                self.teams.append(team)
                self.team_listbox.insert("end", team_name)

    def add_items(self):
        item1 = simpledialog.askstring("Item 1", "Enter the first item:")
        item2 = simpledialog.askstring("Item 2", "Enter the second item:")
        if item1 and item2:
            self.available_items.append((item1, item2))
            messagebox.showinfo("Items Added", f"Items '{item1}' and '{item2}' added to the list.")

    def add_item_to_team(self):
        selected_team_index = self.team_listbox.curselection()
        if not selected_team_index:
            messagebox.showerror("No Team Selected", "Please select a team first.")
            return

        selected_team = self.team_listbox.get(selected_team_index)
        if not self.available_items:
            messagebox.showerror("No Items Available", "Please add items first.")
            return

        current_team = self.teams[selected_team]
        #for game in self.available_items:
        self.create_popup(current_team, self.available_items)

        #item_pair = self.available_items.pop(0)
        #self.teams[selected_team].append(item_pair)
        #messagebox.showinfo("Item Added", f"Items '{item_pair[0]}' and '{item_pair[1]}' added to team '{selected_team}'.")

    def create_popup(self, selected_team, available_items):
        #Creates a popup window for a given pair."""

        popup = tk.Toplevel()
        popup.title(f"Matchup Selection")

        results = {}
            
        button_vars = {} # Dictionary to store button states
        entry_widgets = {} # Dictionary to store entry widgets


        def submit(buttonvars):
            #Handles submission and stores data in the results dictionary."""
            for pair, entry in entry_widgets.items():
                try:
                    int_value = int(entry.get())
                    results[pair] = int_value
                    selection = buttonvars[pair].get()
                    selected_team.append({"Selection": {selection}, "Value": {int_value}, "IsCorrect": -1 })
                except ValueError:
                    messagebox.showerror("Error", f"Please enter a valid integer for {pair[0]} - {pair[1]}.")
                    return # Stop submission if there is an error
            popup.destroy()
            # try:
            #     int_value = entry_value.get()
            #     messagebox.showinfo("Submission", f"Selected: {selected_value.get()}, Integer: {int_value}")
            #     selected_team.append({"Selection": {selected_value.get()}, "Value": {int_value}, "IsCorrect": -1 })
            #     popup.destroy() # Close the popup after submission
            # except tk.TclError: # Handle if non int is entered
            #     messagebox.showerror("Error", "Please Enter a Valid Integer")
            

        for pair in available_items:
            frame = tk.Frame(popup) # Frame to group buttons and entry for each pair
            frame.pack(pady=5)

            button_vars[pair] = tk.StringVar(value="")

            def button_click(pair, value):
                button_vars[pair].set(value)

            button1 = tk.Radiobutton(frame, text=pair[0], variable=button_vars[pair], value=pair[0], command=lambda p=pair, v=pair[0]: button_click(p, v))
            button2 = tk.Radiobutton(frame, text=pair[1], variable=button_vars[pair], value=pair[1], command=lambda p=pair, v=pair[1]: button_click(p, v))
            entry = tk.Entry(frame)
            entry_widgets[pair] = entry  # Store entry widget in the dictionary

            button1.pack(side=tk.LEFT)
            button2.pack(side=tk.LEFT)
            entry.pack(side=tk.LEFT, padx=5)

        submit_button = tk.Button(popup, text="Submit", command=lambda bv=button_vars: submit(bv))
        submit_button.pack(pady=10)


    def save(self):
        try:
            # Establish the connection
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;' # Use appropriate driver
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()

            # Insert or update Teams
            for team in self.teams:
                if team in self.database_teams:
                    # update the team
                    sql = f"UPDATE dbo.Team SET (TeamName, CurrentPoints, MaxPoints) = (?, ?, ?) WHERE TeamIdentifier = (?) AND YearPlaying = {TeamApp.currentYear}"
                    values = (team.teamName, team.currentPoints, team.maxPoints, self.team.teamId)
                    cursor.execute(sql, values)
                    cnxn.commit()  # Important: Commit the changes
                else:
                    # insert the team
                    sql = "INSERT INTO dbo.Team (TeamName, CurrentPoints, MaxPoints, YearPlaying) VALUES (?, ?, ?)"
                    values = (team.teamName, team.currentPoints, team.maxPoints, team.yearPlaying)
                    cursor.execute(sql, values)
                    cnxn.commit()  # Important: Commit the changes


            #Insert or update TeamPicks
            for pick in self.team_picks:
                if pick in self.databaseMatchups:
                    # update the team
                    sql = f"UPDATE dbo.TeamPick SET (TeamIdentifier, GameNumber, TeamSelection, PointValue, IsCorrect, YearPlaying) = (?, ?, ?, ?, ?, ?) WHERE PickIdentifier = (?) AND YearPlaying = {TeamApp.currentYear}"
                    values = (pick.teamId, pick.gameNumber, pick.teamSelection, pick.pointValue, pick.isCorrect, pick.yearPlaying, self.team_pick.pickId)
                    cursor.execute(sql, values)
                    cnxn.commit()  # Important: Commit the changes
                else:
                    # insert the team
                    sql = "INSERT INTO dbo.TeamPick (TeamIdentifier, GameNumber, TeamSelection, PointValue, IsCorrect, YearPlaying) = (?, ?, ?, ?, ?)"
                    values = (pick.teamId, pick.gameNumber, pick.teamSelection, pick.pointValue, pick.isCorrect, pick.yearPlaying)
                    cursor.execute(sql, values)
                    cnxn.commit()  # Important: Commit the changes
            


            #Insert or update Matchups
            for matchup in self.matchups:
                if matchup in self.databaseMatchups:
                    # update the team
                    sql = f"UPDATE dbo.Matchups SET (GameNumber, TeamOne, TeamTwo, Winner, YearPlaying) = (?, ?, ?, ?, ?) WHERE MatchupIdentifier = (?) AND YearPlaying = {TeamApp.currentYear}"
                    values = (matchup.gameNumber, matchup.teamOne, matchup.teamTwo, matchup.winner, matchup.yearPlaying, self.matchup.matchupId)
                    cursor.execute(sql, values)
                    cnxn.commit()  # Important: Commit the changes
                else:
                    # insert the team
                    sql = "INSERT INTO dbo.Matchups (GameNumber, TeamOne, TeamTwo, Winner, YearPlaying) = (?, ?, ?, ?, ?)"
                    values = (matchup.gameNumber, matchup.teamOne, matchup.teamTwo, matchup.winner, matchup.yearPlaying)
                    cursor.execute(sql, values)
                    cnxn.commit()  # Important: Commit the changes
            



            # # Example 2: Inserting multiple rows using executemany
            # customers_to_insert = [
            #     (7, 'Bob Williams', 'Austin'),
            #     (8, 'Eva Garcia', 'San Antonio')
            # ]
            # sql = "INSERT INTO Customers (CustomerID, Name, City) VALUES (?, ?, ?)"
            # cursor.executemany(sql, customers_to_insert)
            # cnxn.commit()

            print("Data inserted successfully.")

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '28000':
                print("Invalid credentials")
            else:
                print(f"Error connecting to or inserting data: {ex}")
        except Exception as e:
            print(f"A general exception occurred: {e}")
        finally:
            if cnxn:
                cursor.close()
                cnxn.close()
                

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1000x750+700+200')
    app = TeamApp(root)
    root.mainloop()
