import tornado.web 
import tornado.ioloop
import json
import os

class mainRequstHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

# class ManCityListRequstHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render("index.html")

class numberQueryParamHandler(tornado.web.RequestHandler):
    def get(self):
        num = self.get_argument("num")
        if(num.isdigit()):
            result = "ODD" if int(num) % 2 else "Even"
            self.write(f"{num} is {result}")
        else : 
            self.write("Write Valid Number please.")

class playersResParamHandler(tornado.web.RequestHandler):
    def get(self, playerName , playerNumber):
        self.write(f"Player Name is {playerName} and his number is {playerNumber}")

class playerListRequestHandler(tornado.web.RequestHandler):

    def get(self):
        List = open("playerList.txt")
        playersList = List.read().splitlines()
        List.close()
        self.write(json.dumps(playersList))

    def post(self):
        addPlayer = self.get_argument("addPlayer")
        playerList = open("playerList.txt",'a')
        playerList.write(f'{addPlayer}\n')
        playerList.close()
        self.write(json.dumps({"massage" : "Player added succefully"}))

    def delete(self):
        deletePlayer = self.get_argument("deletePlayer")
        playerList = open("playerList.txt",'r')
        players = playerList.read().splitlines()
        playerList.close()
        if(deletePlayer in players):
            players.remove(deletePlayer)
            playerList = open("playerList.txt", "w")
            for p in players:
                playerList.write(f"{p}\n")
            playerList.close()
            self.write(json.dumps({"message": f"Player '{deletePlayer}' deleted successfully"}))
        else:
            self.write(json.dumps({"error": "Player Not Found"}))

    def put(self):
        oldPlayer = self.get_argument("oldPlayer")  
        newPlayer = self.get_argument("newPlayer")
        playerList = open("playerList.txt",'r')
        player = playerList.read().splitlines()
        playerList.close
        if(oldPlayer in player) : 
            index = player.index(oldPlayer)
            player[index] = newPlayer
            playerList = open("playerList.txt", "w")
            for p in player:
                playerList.write(f"{p}\n")
            playerList.close()
            self.write(json.dumps({"message": f"Player '{oldPlayer}' updated to '{newPlayer}'"}))
        else:
            self.write(json.dumps({"error": "Player Not Found"}))

if __name__ == "__main__":

    app = tornado.web.Application([
        (r'/',mainRequstHandler),
        # (r'/ManCity',ManCityListRequstHandler),
        (r'/isEven',numberQueryParamHandler),
        (r"/players/([A-z]+)/([0-9]+)", playersResParamHandler),
        (r'/playersList',playerListRequestHandler)
    ],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static")
    )

    port = 8000
    app.listen(port)
    
    print(f"Server is runing in port {port}")
    tornado.ioloop.IOLoop.current().start()