from flask import Flask,request,jsonify
import psycopg2
import graphene
from flask_graphql import GraphQLView


app = Flask(__name__)

## DATABASE details ##

db_name = "vhpimhhs"
db_user = "vhpimhhs"
db_pass = "k3CiOaI6T3Z4ijDKanhunq2doaYFJTXl"
db_host = "rajje.db.elephantsql.com"
db_port = "5432"

## Connnecting DATABASE ##

connection = psycopg2.connect(database = db_name, user = db_user, password = db_pass, host = db_host, port = db_port)

print("database connected")

### Creating tables ###

# curr = connection.cursor()
# tab = """CREATE TABLE newtable (ID INT PRIMARY KEY NOT NULL,
#                             TITLE TEXT NOT NULL,
#                             DESCRIPTION TEXT NOT NULL,
#                             DONE BOOLEAN NOT NULL)"""
# curr.execute(tab)
# connection.commit()
# print("table created")


# Models
class Task_items(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String(name=graphene.String(default_value="Task"))
    description = graphene.String(required=True)
    done = graphene.Boolean(status=graphene.Boolean(default_value=False))

    def task(self, tasks):
        curr = connection.cursor()
        req = "SELECT * FROM newtable"
        curr.execute(req)
        data = curr.fetchall()
        connection.commit()
        connection.close()
        task = []
        for i in range(len(data)):
            task.append({'id':data[i][0],'title':data[i][1],'description':data[i][2],'done':bool(data[i][3])})
        return jsonify(task)

class Query_items(graphene.ObjectType):
    todo_items = graphene.List(Task_items)
    todo_item = graphene.Field(Task_items, id=graphene.Int())

    def resolve_fields(self, task):
        curr = connection.cursor()
        req = "SELECT * FROM newtable"
        curr.execute(req)
        data = curr.fetchall()
        connection.commit()
        connection.close()
        task = []
        for i in range(len(data)):
            task.append({'id':data[i][0],'title':data[i][1],'description':data[i][2],'done':bool(data[i][3])})
        return jsonify(task)

# Schema Objects
schema = graphene.Schema(query=Query_items)

app.add_url_rule('/', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__ == '__main__':
     app.run(debug=True)