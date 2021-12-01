import json
import os

#### Structure of the JSON File ####
## {
##  "chat_id":
##            [
##             {
##              "username": username, "id": id,
##             },
##            ],
## }


class UsersToPing:
    # Class to manage the users to ping
    def __init__(self, filename="users.json"):
        # Initialize the class
        self.filename = filename
        self.created_now = self.createFileIfNotExists()

    def createFileIfNotExists(self) -> bool:
        # Create the file if it doesn't exist
        if not os.path.isfile(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                # Write an empty file
                f.write("")
                return True
        return False

    def checkIfFileIsEmpty(self):
        # Check if the file is empty
        with open(self.filename, "r") as f:
            return f.read() == ""

    def saveFile(self, content: dict):
        # Save the file
        with open(self.filename, "w", encoding="utf-8") as f:
            # Write the content
            f.write(json.dumps(content))

    def addUser(self, chat_id, username, user_id):
        # Add a user to the file if it doesn't exist
        chat_id = str(chat_id)
        username = str(username)
        user_id = str(user_id)
        
        if self.checkIfFileIsEmpty(): # If the file is empty
            json_dict = {chat_id: [{"username": username, "id": user_id}]} # Create a new dict
            self.saveFile(json_dict) # Save the file
            return True
        if self.getUser(chat_id, username, user_id): # If the user already exists
            return False # Return False
        with open(self.filename, "r", encoding="utf-8") as f: # If the file is not empty and the user doesn't exist
            json_dict = json.loads(f.read()) # Load the file
            if chat_id not in json_dict.keys(): # If the chat_id doesn't exist
                json_dict[chat_id] = [{"username": username, "id": user_id}] # Create a new dict with the new user
            elif chat_id in json_dict.keys(): # If the chat_id exists
                user_names = [x['username'] for x in json_dict[chat_id]] # Get all the usernames in the chat id
                user_ids = [x["id"] for x in json_dict[chat_id]] # Get all the ids in the chat id
                if username not in user_names or user_id not in user_ids: # If the username or the id doesn't exist
                    json_dict[chat_id].append({"username": username, "id": user_id}) # Add the new user
            self.saveFile(json_dict) # Save the file
            return True

    def removeUser(self, chat_id, username, user_id):
        # Remove a user from the file
        chat_id = str(chat_id)
        username = str(username)
        user_id = str(user_id)

        if self.checkIfFileIsEmpty(): # If the file is empty
            return {"status": False, "message": "Erro! Nenhum usuario salvo!"} # Return False
        if not self.getUser(chat_id, username, user_id): # If the user doesn't exist
            return {"status": False, "message": "Erro! Usuário não está salvo!"} # Return False
        with open(self.filename, "r", encoding="utf-8") as f: # If the file is not empty and the user exists
            json_dict = json.loads(f.read()) # Load the file
            if chat_id not in json_dict.keys(): # If the chat_id doesn't exist
                return {"status": False, "message": "Erro! Nenhum usuario salvo!"} # Return False
            elif chat_id in json_dict.keys(): # If the chat_id exists
                new_dict = {} # Create a new dict
                new_dict[chat_id] = [] # Create a new list
                for x in json_dict[chat_id]: # For each user in the chat id
                    if username != x['username'] and user_id != x['id']: # If the username and the id don't match
                        new_dict[chat_id].append(x) # Add the user to the new dict
                self.saveFile(new_dict) # Save the file
                return {"status": True, "message": "Usuario removido com sucesso!"} # Return True
        return {"status": False, "message": "Erro! Algo deu errado!"} # Return False

    def getUser(self, chat_id, username, user_id):
        # Get a user from the file
        """[{'username': 'kamuridesu', 'id': '1253085705'}, {'username': 'asd', 'id': '0'}]"""
        chat_id = str(chat_id)
        username = str(username)
        user_id = str(user_id)
        json_dict = {} # Create a new dict
        with open(self.filename, "r", encoding="utf-8") as file: # Load the file
            json_dict = json.loads(file.read()) # Load the file
        for key, value in json_dict.items(): # For each key and value in the dict
            if key == chat_id: # If the key is the chat id
                for x in value: # For each user in the chat id
                    if x["username"] == username or x["id"] == user_id: # If the username or the id match
                        return x # Return the user
        return None # If the user doesn't exist

    def getAllUsers(self, chat_id):
        # Get all the users from the file
        chat_id = str(chat_id) # Convert the chat_id to string
        json_dict = {}  # Create a new dict
        with open(self.filename, "r", encoding="utf-8") as file: # Load the file
            json_dict = json.loads(file.read()) # Load the file
        for k, v in json_dict.items(): # For each key and value in the dict
            if k == chat_id: # If the key is the chat id
                return v # Return the list of users
        return None # If the chat id doesn't exist

    def clearFile(self):
        # Clear the file
        with open(self.filename, "w", encoding="utf-8") as f:
            # Write an empty file
            f.write("")


if __name__ == "__main__":
    u = UsersToPing()
    u.clearFile()
    u.addUser("1253085705", "asd", "0")
    u.addUser("1253085705", "avs", "1")
    u.addUser("1253085705", "as", "2")
    print(u.getAllUsers('1253085705'))
    x = u.removeUser("1253085705", "as", "2")
    print(x)
    print(u.getAllUsers('1253085705'))
