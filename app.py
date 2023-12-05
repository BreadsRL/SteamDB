from flask import Flask, render_template, request, redirect, url_for, session, jsonify, current_app
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = '123456'


# Database initialization
# def init_db():
#     with app.app_context():
#         db = get_db()
#         with app.open_resource('init.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()

# Database connection
def get_db():
    db = sqlite3.connect('Steam.db')
    db.row_factory = sqlite3.Row
    return db

# init_db()

##################################################################################################
#Login Portion

@app.route('/')
def root():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        cursor.execute('SELECT * FROM User WHERE Email = ? AND Password = ?', (email,password))
        user = cursor.fetchone()

        if user:
            session['username'] = user['Username']
            return redirect(url_for('welcome_page'))
        else:
            # Authentication failed, render an error message
            return render_template('login.html', message='Sorry, this account is wrong or doesn\'t exist.')
##################################################################################################
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('root'))
##################################################################################################
#Registration Portion
@app.route('/register', methods=['GET'])
def show_registration_page():
    return render_template('register.html')

# Registration route
@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO User (Username, Email, Password) VALUES (?, ?, ?)',
                           (username, email, password))
            db.commit()

            # Flash success message
            flash('Successfully registered account, please sign in now!', 'success')
            return redirect(url_for('root'))
        except sqlite3.IntegrityError:
            db.rollback()
            flash('Username or Email already exists.', 'error')
            return redirect(url_for('show_registration_page'))
##################################################################################################
#Index Portion
@app.route('/welcome')
def welcome_page():
    if 'username' in session:
        # User is logged in, render the welcome page
        return render_template('welcome.html', username=session['username'])
    else:
        # User is not logged in, redirect to the login page
        return redirect(url_for('root'))
##################################################################################################
#Updating Email Portion
@app.route('/update_email')
def update_email_page():
    return render_template('update_email.html')

# Function to update email in the database
def update_email_in_database(old_email, new_email):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE User SET Email = ? WHERE Email = ?', (new_email, old_email))
            conn.commit()
    except sqlite3.IntegrityError:
        # Handle the case where the new email already exists in the database
        flash('Error: Email already is being used by another user!', 'error')

# Function to check if provided credentials are valid
def check_credentials(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE Username = ? AND Password = ?', (username, password))
    user = cursor.fetchone()
    return user is not None


def get_old_email_from_database(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT Email FROM User WHERE Username = ?', (username,))
    user = cursor.fetchone()
    old_email = user[0] if user else None

    return old_email

@app.route('/update_email', methods=['GET', 'POST'])
def update_email():
    if request.method == 'POST':
        new_email = request.form['new_email']
        username = request.form['username']
        password = request.form['password']


        old_email = get_old_email_from_database(username)

        # Check if the provided username and password match
        if check_credentials(username, password, old_email) == False:
            flash("Invalid credentials! Nice try, hacker!", 'error')
            return redirect(url_for('root'))
        else:
            # Update the email in the database
            update_email_in_database(old_email, new_email)
            if "error":
                return redirect(url_for('root')) 

    flash('Email has been successfully changed!', 'success')
    return redirect(url_for('root'))  # Assuming you have a template for this route

# Route for showing a success message
@app.route('/update_success')
def update_success():
    return 'Email updated successfully!'

##################################################################################################
#Updating Username Portion
@app.route('/update_username')
def update_username_page():
    return render_template('update_username.html')

# Function to update username in the database
def update_username_in_database(old_username, new_username):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE User SET Username = ? WHERE Username = ?', (new_username, old_username))
            cursor.execute('UPDATE Wishlist SET Username = ? WHERE Username = ?', (new_username, old_username))
            cursor.execute('UPDATE Review SET Username = ? WHERE Username = ?', (new_username, old_username))
            conn.commit()
    except sqlite3.IntegrityError:
        flash('Error: Username already is being used by another user!', 'error')

# Route for updating username
@app.route('/update_username', methods=['GET', 'POST'])
def update_username():
    if request.method == 'POST':
        new_username = request.form['new_username']
        email = request.form['email']
        password = request.form['password']

        if not check_credentials_email(email, password):
            flash("Invalid credentials! Nice try, hacker!", 'error')
            return redirect(url_for('root')) 
        else:
            old_username = get_old_username_from_database(email)
            update_username_in_database(old_username, new_username)
            flash('Username has been successfully changed!', 'success')
            # Redirect to the login page
            return redirect(url_for('root'))
    return render_template('update_username.html')


def check_credentials_email(email, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE Email = ? AND Password = ?', (email, password))
    user = cursor.fetchone()
    return user is not None

def get_old_username_from_database(email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT Username FROM User WHERE Email = ?', (email,))
    user = cursor.fetchone()
    old_username = user[0] if user else None
    return old_username

##################################################################################################
#Update Password Portion
# Route for updating password
@app.route('/update_password', methods=['GET', 'POST'])
def update_password():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        if not check_credentials(username, old_password, email):
            flash("Invalid credentials! Nice try, hacker!", 'error')
            return redirect(url_for('root')) 
        else:
            update_password_in_database(username, new_password)
            flash('Password has been successfully changed!', 'success')
            return redirect(url_for('root'))
    return render_template('update_password.html')

def update_password_in_database(username, new_password):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE User SET Password = ? WHERE Username = ?', (new_password, username))
            conn.commit()
    except sqlite3.Error:
        flash('Error updating password in the database.', 'error')

def check_credentials(username, password, email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE Username = ? AND Password = ? AND Email = ?', (username, password, email))
    user = cursor.fetchone()
    return user is not None
##################################################################################################
#Searching Game Portion
@app.route('/search-game', methods=['GET', 'POST'])
def search_game_page():
    if request.method == 'POST':
        print("Search form submitted!")
        search_type = request.form['search_type']

        if search_type == 'name':
            game_name = request.form['game_name']
            game_list = get_search_results_by_name(game_name)
            print("Game List (by name):", game_list)
            return render_template('game_list.html', game_list=game_list)

        elif search_type == 'tags':
            tags = request.form.get('tags').split('|')
            print('Tags:', tags)

            # tags = request.form.getlist('tags')  # Use getlist to retrieve all values
            game_list = get_search_results_by_tags(tags)
            print("Game List (by tags):", game_list)
            return render_template('game_list.html', game_list=game_list)

    # Render the search_game.html template for GET requests
    return render_template('search_game.html')




def get_search_results_by_name(game_name):
    db = get_db()
    cursor = db.cursor()

    # Use the LIKE operator to search for GameTitle containing the provided substring
    cursor.execute('SELECT * FROM Game WHERE GameTitle LIKE ?', ('%' + game_name + '%',))
    game_list = cursor.fetchall()

    # Format the data before returning it to the template
    formatted_game_list = format_search_results(game_list)

    return formatted_game_list

def get_search_results_by_tags(tags):
    if not tags:
        return []  # No tags selected, return an empty list

    db = get_db()
    cursor = db.cursor()

    query = '''
        SELECT DISTINCT G.* FROM Game G
        JOIN GameTag GT ON G.GameID = GT.GameID
        JOIN Tag T ON GT.TagID = T.TagID
        WHERE T.TagName IN ({})
    '''.format(','.join(['?'] * len(tags)))

    cursor.execute(query, tags)
    game_list = cursor.fetchall()

    # Format the data before returning it to the template
    formatted_game_list = format_search_results(game_list)

    return formatted_game_list

def format_search_results(game_list):
    formatted_list = []

    for game in game_list:
        # Convert sqlite3.Row to a dictionary
        game_dict = dict(game)

        # Retrieve the tags for the game
        tags = get_tags_for_game(game_dict.get('GameID', ''))

        # Retrieve the PublisherName using LEFT JOIN
        db = get_db()
        cursor = db.cursor()

        query = '''
            SELECT G.GameID, G.GameTitle, G.ReleaseDate, P.PublisherName
            FROM Game G
            LEFT JOIN Publisher P ON G.PublisherID = P.PublisherID
            WHERE G.GameID = ?
        '''

        cursor.execute(query, (game_dict.get('GameID', ''),))
        game_info = cursor.fetchone()

        # Close the database connection
        db.close()

        if game_info:
            formatted_game = {
                'GameID': game_info['GameID'],
                'GameTitle': game_info['GameTitle'],
                'ReleaseDate': game_info['ReleaseDate'],
                'PublisherName': game_info['PublisherName'],
                'Tags': tags
            }
            formatted_list.append(formatted_game)

    return formatted_list


def get_tags_for_game(game_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT T.TagName
        FROM GameTag GT
        JOIN Tag T ON GT.TagID = T.TagID
        WHERE GT.GameID = ?
    ''', (game_id,))

    tags = cursor.fetchall()
    
    # Log statements for debugging
    print(f"GameID: {game_id}")
    print(f"Tags retrieved: {tags}")

    tag_list = [tag['TagName'] for tag in tags]

    return tag_list


@app.route('/get-tags')
def get_tags():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT TagName FROM Tag')
    tags = cursor.fetchall()

    tag_list = [tag['TagName'] for tag in tags]

    return jsonify(tag_list)
##################################################################################################
#Game Information Section (Basically shows review)

@app.route('/game-info/<int:game_id>')
def game_info_page(game_id):
    # Retrieve game information
    game_info = get_game_info(game_id)

    # Print game_info for debugging
    print(f"game_info: {game_info}")

    if game_info:
        # Retrieve reviews for the game
        reviews = get_reviews_for_game(game_id)
        return render_template('game_info.html', game_info=game_info, reviews=reviews)

    # Handle case where game information is not found
    flash('Game not found.', 'error')
    return render_template('game_info.html', game_info=None, reviews=None)


def get_game_info(game_id):
    db = get_db()
    cursor = db.cursor()

    query = '''
        SELECT G.GameID, G.GameTitle, G.ReleaseDate, P.PublisherName
        FROM Game G
        LEFT JOIN Publisher P ON G.PublisherID = P.PublisherID
        WHERE G.GameID = ?
    '''

    cursor.execute(query, (game_id,))
    game_info = cursor.fetchone()

    # Close the database connection
    db.close()

    return game_info



def get_reviews_for_game(game_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT Username, Rating, Comment, ReviewDate
        FROM Review
        WHERE GameID = ?
    ''', (game_id,))

    reviews = cursor.fetchall()

    # Close the database connection
    db.close()

    return reviews
##################################################################################################
#Wishlist Portion
@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist_page():
    if 'username' not in session:
        # Redirect to login if the user is not logged in
        return redirect(url_for('login_user'))

    username = session['username']

    if request.method == 'POST':
        # Handle adding and removing games from the wishlist
        if 'add_game' in request.form:
            game_id_to_add = request.form['add_game']
            print(f"Adding game {game_id_to_add} to wishlist for user {username}")
            add_game_to_wishlist(username, game_id_to_add)
        elif 'delete_game' in request.form:
            game_id_to_delete = request.form['delete_game']
            print(f"Deleting game {game_id_to_delete} from wishlist for user {username}")
            delete_game_from_wishlist(username, game_id_to_delete)

    # Fetch wishlist items from the database for the logged-in user
    wishlist_items = get_wishlist_items(username)
    print(f"Wishlist items: {wishlist_items}")

    # Fetch available games (not in the wishlist) for the dropdown
    available_wishlist_games = get_available_wishlist_games(username)
    print(f"Available wishlist games: {available_wishlist_games}")

    return render_template('wishlist.html', wishlist_items=wishlist_items, available_games=available_wishlist_games)

def add_game_to_wishlist(username, game_id):
    # Implement the logic to add a game to the user's wishlist in the database
    # Perform an SQL INSERT into the Wishlist table
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO Wishlist (Username, GameID) VALUES (?, ?)', (username, game_id))
    db.commit()

def delete_game_from_wishlist(username, game_id):
    # Implement the logic to delete a game from the user's wishlist in the database
    # Perform an SQL DELETE from the Wishlist table
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM Wishlist WHERE Username = ? AND GameID = ?', (username, game_id))
    db.commit()

def get_wishlist_items(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT Game.GameID, GameTitle, PublisherName, ReleaseDate, WishlistID
        FROM Wishlist
        JOIN Game ON Wishlist.GameID = Game.GameID
        LEFT JOIN Publisher ON Game.PublisherID = Publisher.PublisherID
        WHERE Wishlist.Username = ?
    ''', (username,))
    wishlist_items = cursor.fetchall()
    cursor.close()
    return wishlist_items


def get_available_wishlist_games(username):

    db = get_db()
    cursor = db.cursor()

    query = '''
        SELECT GameID, GameTitle
        FROM Game
        WHERE GameID NOT IN (
            SELECT GameID
            FROM Wishlist
            WHERE Username = ?
        )
    '''

    cursor.execute(query, (username,))
    available_wishlist_games = cursor.fetchall()
    return available_wishlist_games



def get_available_games(username, data_type='review'):
    db = get_db()
    cursor = db.cursor()

    if data_type == 'review':
        query = '''
            SELECT GameID, GameTitle
            FROM Game
            WHERE GameID NOT IN (
                SELECT GameID
                FROM Review
                WHERE Username = ?
            )
        '''
    elif data_type == 'wishlist':
        query = '''
            SELECT GameID, GameTitle
            FROM Game
            WHERE GameID NOT IN (
                SELECT GameID
                FROM Wishlist
                WHERE Username = ?
            )
        '''
    else:
        # Handle invalid data_type parameter
        return []

    cursor.execute(query, (username,))
    available_games = cursor.fetchall()
    return available_games
##################################################################################################
#Review Portion

@app.route('/review', methods=['GET', 'POST'])
def review_page():
    if 'username' not in session:
        # Redirect to login if the user is not logged in
        return redirect(url_for('login_user'))

    username = session['username']

    if request.method == 'POST':
        game_id_to_add = request.form['game_id']
        rating = int(request.form['rating'])
        comment = request.form['comment']

        # Check if the user already has a review for the selected game
        if has_existing_review(username, game_id_to_add):
            return redirect(url_for('review_page'))

        # Submit the review
        submit_review(username, game_id_to_add, rating, comment)

        # Redirect back to the review page
        return redirect(url_for('review_page'))

    # Fetch user reviews and available games
    user_reviews = get_user_reviews(username)
    available_games = get_available_games(username)

    return render_template('review.html', user_reviews=user_reviews, available_games=available_games)


def get_user_reviews(username):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT Review.ReviewID, Game.GameTitle, Review.Rating, Review.Comment, Review.ReviewDate
        FROM Review
        JOIN Game ON Review.GameID = Game.GameID
        WHERE Review.Username = ?
    ''', (username,))

    reviews = cursor.fetchall()

    return reviews


@app.route('/submit_review', methods=['POST'])
def submit_review():
    if 'username' not in session:
        # Redirect to login if the user is not logged in
        return redirect(url_for('login_user'))

    username = session['username']
    game_id = request.form['game_id']

    # Check if the user already has a review for the selected game
    if has_existing_review(username, game_id):
        return redirect(url_for('review_page'))

    db = get_db()
    cursor = db.cursor()

    rating = int(request.form['rating'])
    comment = request.form['comment']
    
    # Get the current date and time in the local timezone
    local_tz = pytz.timezone('America/Los_Angeles')  # replace with your actual timezone
    current_date = datetime.now(local_tz).strftime("%Y-%m-%d")

    try:
        cursor.execute('''
            INSERT INTO Review (Username, GameID, Rating, Comment, ReviewDate)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, game_id, rating, comment, current_date))
        db.commit()
    except Exception as e:
        # Handle database error, perhaps log the error
        db.rollback()
        print(f"Error submitting review: {e}")

    finally:
        cursor.close()

    # Redirect back to the review page
    return redirect(url_for('review_page'))

def has_existing_review(username, game_id):
    # Check if the user already has a review for the selected game
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Review WHERE Username = ? AND GameID = ?', (username, game_id))
    existing_review = cursor.fetchone()
    cursor.close()

    return existing_review is not None


@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # If the form is submitted, update the review in the database
        rating = int(request.form['rating'])
        comment = request.form['comment']

        try:
            cursor.execute('''
                UPDATE Review
                SET Rating = ?, Comment = ?
                WHERE ReviewID = ?
            ''', (rating, comment, review_id))
            db.commit()
        except Exception as e:
            # Handle database error, perhaps log the error
            db.rollback()
            print(f"Error updating review: {e}")

        finally:
            cursor.close()

        # Redirect back to the review page
        return redirect(url_for('review_page'))

    # Fetch the review data for the given ID
    cursor.execute('''
        SELECT ReviewID, Rating, Comment, GameTitle
        FROM Review
        JOIN Game ON Review.GameID = Game.GameID
        WHERE ReviewID = ?
    ''', (review_id,))
    review = cursor.fetchone()

    cursor.close()

    # Pass the review data to the template for editing
    return render_template('edit_review.html', review=review)

@app.route('/delete_review/<int:review_id>')
def delete_review(review_id):
    # Implement logic to delete the review with the given ID
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute('DELETE FROM Review WHERE ReviewID = ?', (review_id,))
        db.commit()
    except Exception as e:
        # Handle database error, perhaps log the error
        db.rollback()
        print(f"Error deleting review: {e}")

    finally:
        cursor.close()

    # Redirect back to the review page
    return redirect(url_for('review_page'))

def get_review_items(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT Review.GameID, GameTitle, PublisherName, ReleaseDate, Rating, Comment, ReviewDate
        FROM Review
        JOIN Game ON Review.GameID = Game.GameID
        LEFT JOIN Publisher ON Game.PublisherID = Publisher.PublisherID
        WHERE Review.Username = ?
    ''', (username,))
    review_items = cursor.fetchall()
    cursor.close()
    return review_items

##################################################################################################
#Sale Portion

@app.route('/sale_page')
def sale_page():
    db = get_db()
    cursor = db.cursor()
    
    # Fetch sales data from the Sale table with game title
    query = '''
        SELECT Game.GameTitle, Sale.Start_Date, Sale.End_Date, Sale.DiscountPercent
        FROM Sale
        JOIN Game ON Sale.GameID = Game.GameID;
    '''
    cursor.execute(query)
    sales_data = cursor.fetchall()

    return render_template('sale.html', sales_data=sales_data)


if __name__ == '__main__':
    app.run(debug=True)