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
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.created_now = self.createFileIfNotExists()

    def createFileIfNotExists(self) -> bool:
        if not os.path.isfile(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write("")
                return True
        return False

    def checkIfFileIsEmpty(self):
        with open(self.filename, "r") as f:
            return f.read() == ""

    def saveFile(self, content: dict):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(content))

    def addUser(self, chat_id, username, user_id):
        chat_id = str(chat_id)
        username = str(username)
        user_id = str(user_id)
        
        if self.checkIfFileIsEmpty():
            json_dict = {chat_id: [{"username": username, "id": user_id}]}
            self.saveFile(json_dict)
            return True
        if self.getUser(chat_id, username, user_id):
            return False
        with open(self.filename, "r", encoding="utf-8") as f:
            json_dict = json.loads(f.read())
            if chat_id not in json_dict.keys():
                json_dict[chat_id] = [{"username": username, "id": user_id}]
            elif chat_id in json_dict.keys():
                user_names = [x['username'] for x in json_dict[chat_id]]
                user_ids = [x["id"] for x in json_dict[chat_id]]
                if username not in user_names or user_id not in user_ids:
                    json_dict[chat_id].append({"username": username, "id": user_id})
            self.saveFile(json_dict)
            return True

    def removeUser(self, chat_id, username, user_id):
        chat_id = str(chat_id)
        username = str(username)
        user_id = str(user_id)

        if self.checkIfFileIsEmpty():
            return {"status": False, "message": "Erro! Nenhum usuario salvo!"}
        if not self.getUser(chat_id, username, user_id):
            return {"status": False, "message": "Erro! Usuário não está salvo!"}
        with open(self.filename, "r", encoding="utf-8") as f:
            json_dict = json.loads(f.read())
            if chat_id not in json_dict.keys():
                return {"status": False, "message": "Erro! Nenhum usuario salvo!"}
            elif chat_id in json_dict.keys():
                new_dict = {}
                new_dict[chat_id] = []
                for x in json_dict[chat_id]:
                    if username != x['username'] and user_id != x['id']:
                        new_dict[chat_id].append(x)
                self.saveFile(new_dict)
                return {"status": True, "message": "Usuario removido com sucesso!"}
        return {"status": False, "message": "Erro! Algo deu errado!"}

    def getUser(self, chat_id, username, user_id):
        """[{'username': 'kamuridesu', 'id': '1253085705'}, {'username': 'asd', 'id': '0'}]"""
        chat_id = str(chat_id)
        username = str(username)
        user_id = str(user_id)
        json_dict = {}
        with open(self.filename, "r", encoding="utf-8") as file:
            json_dict = json.loads(file.read())
        for key, value in json_dict.items():
            if key == chat_id:
                for x in value:
                    if x["username"] == username or x["id"] == user_id:
                        return x
        return None

    def getAllUsers(self, chat_id):
        chat_id = str(chat_id)
        json_dict = {}
        with open(self.filename, "r", encoding="utf-8") as file:
            json_dict = json.loads(file.read())
        for k, v in json_dict.items():
            if k == chat_id:
                return v
        return None

    def clearFile(self):
        with open(self.filename, "w", encoding="utf-8") as f:
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
