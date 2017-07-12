import tornado.ioloop
import tornado.web
import sqlite3
import json
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class UsersList(tornado.web.RequestHandler):
    def get(self):
        query = "SELECT * FROM 'users';"
        users = self.application.db.execute(query).fetchall()
        list_json_users = []
        for user in users:
            json_user = {
                "id": user[0],
                "first_name": user[1],
                "last_name": user[2],
                "age": user[3]
            }
            list_json_users.append(json_user)

        self.write(str(json.dumps(list_json_users)))


def make_app():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    }
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/users", UsersList),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.db = sqlite3.connect("data_base.db")
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
