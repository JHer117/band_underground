
from config import app, db
from models import Users, Bands
import routes



if __name__ == "__main__":
    app.run(debug=True)
    