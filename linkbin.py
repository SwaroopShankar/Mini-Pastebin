from flask import Flask , render_template ,request , redirect , url_for 
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)

database_uri = "sqlite:///linkbin.db"
engine = create_engine(database_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#creation of databse
class Linkbin(Base):
    __tablename__ = "linkbin"   
    id = Column(Integer , primary_key=True)
    content = Column(String(500), nullable=False) 
    date_created = Column(DateTime , default=datetime.utcnow)

    def __init__(self,content):
        self.content = content

    def __repr__(self) -> str:
        return f"{self.id} - {self.content}"

#home page
app.debug=True
@app.route("/")
def index():
    return render_template("linkbin.html")

#about page
@app.route('/about')
def about():
    return render_template("about.html")

# retuns the content when the paste_url is visited
@app.route('/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    db_session =SessionLocal()
    b = db_session.get(Linkbin,post_id).content
    return b

#returns the paste url when save is clicked
@app.route('/post_user' , methods=['POST'])
def post_user():
    bin = Linkbin(request.form['content'])
    db_session =SessionLocal()
    db_session.add(bin)
    db_session.commit()
    db_session.refresh(bin)
    paste_url = f"{request.root_url}{bin.id}"
    return render_template("linkbin-url.html",paste_url=paste_url)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)