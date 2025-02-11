from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("mysql://root:Farheen2005@localhost:3306/kps_knowledge_base")
print(db.dialect)
print(db.get_usable_table_names())
print(db.run("SELECT * FROM resources ;"))