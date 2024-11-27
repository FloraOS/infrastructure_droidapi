import sys
import os

from droidapi.helpers.authorization import generate_token
from droidapi.db import get_db_session
from droidapi.app import app

def main() -> int:
    """
    C-style main
    :return: exit code
    """
    session = get_db_session()
    model, token = generate_token(os.environ["SECRET_KEY"])
    session.add(model)
    session.commit()
    print("Your authorization token is:", token)
    return 0

if __name__ == "__main__":
    with app.app_context():
        sys.exit(main())
