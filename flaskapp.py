from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
from dbcode import *
from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Users')

#Displaying Home Page
@app.route('/')
def home():
    results = show_movies()
    return render_template('home.html',results=results)

#Displaying a list of movies
@app.route('/movies')
def movies():
    movies_list = show_movies()  # [{ 'title': '…' }, …]
    return render_template('movies.html', movies=movies_list)

# ─── New Route: Recommend Movies by FavGenre ────────────────
@app.route('/recommend-movies', methods=['GET', 'POST'])
def recommend_movies():
    if request.method == 'POST':
        name = request.form['name']
        # 1) get FavGenre from Dynamo
        try:
            resp = table.get_item(Key={'Name': name})
            user = resp.get('Item')
            if not user:
                flash('User not found.', 'danger')
                return redirect(url_for('recommend_movies'))
            fav_genre = user['FavGenre']
        except ClientError as e:
            flash(f"Error fetching user: {e.response['Error']['Message']}", 'danger')
            return redirect(url_for('recommend_movies'))

        # 2) query SQL for 5 movies matching that genre
        sql = """
            SELECT m.title
              FROM movie m
              JOIN movie_genres mg ON m.movie_id = mg.movie_id
              JOIN genre g       ON mg.genre_id = g.genre_id
             WHERE g.genre_name = %s
             LIMIT 5
        """
        recs = execute_query(sql, str(fav_genre,))  # [{ 'title': '…' }, …]
        return render_template(
            'recommendations.html',
            name=name,
            genre=fav_genre,
            movies=recs
        )

    # GET → show form
    return render_template('recommend_movies.html')


#---CRUD dynamo routes----

#Create
@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['firstname']
        genre = request.form['genre']

        try:
            table.put_item(
                Item={'Name': name, 'FavGenre': genre},
                ConditionExpression='attribute_not_exists(#n)',
                ExpressionAttributeNames={'#n': 'Name'}
            )
            flash('User added successfully!', 'success')
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                flash('User already exists.', 'danger')
            else:
                flash(f"Error: {e.response['Error']['Message']}", 'danger')
        return redirect(url_for('home'))
    return render_template('add_user.html')

#Delete
@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        name = request.form['name']
        try:
            table.delete_item(
                Key={'Name': name},
                ConditionExpression='attribute_exists(#n)',
                ExpressionAttributeNames={'#n': 'Name'}
            )
            flash('User deleted successfully!', 'warning')
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                flash('User does not exist.', 'danger')
            else:
                flash(f"Error: {e.response['Error']['Message']}", 'danger')
        return redirect(url_for('home'))
    return render_template('delete_user.html')

#Read
@app.route('/display-users')
def display_users():
    try:
        response = table.scan()
        items = response.get('Items', [])
        users_list = []
        for item in items:
            name = item.get('Name', '')
            fav_genre = item.get('FavGenre', '')
            
            users_list.append((name, fav_genre))
    except ClientError as e:
        flash(f"Error fetching users: {e.response['Error']['Message']}", 'danger')
        users_list = []
    return render_template('display_users.html', users=users_list)

#Update
@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        name = request.form['name']
        new_genre = request.form['genre']

        try:
            response = table.update_item(
                Key={'Name': name},
                UpdateExpression='SET FavGenre = :g',
                ConditionExpression='attribute_exists(#n)',
                ExpressionAttributeNames={'#n': 'Name'},
                ExpressionAttributeValues={':g': new_genre},
                ReturnValues='UPDATED_NEW'
            )
            flash('User updated successfully!', 'info')
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                flash('User does not exist.', 'danger')
            else:
                flash(f"Error: {e.response['Error']['Message']}", 'danger')
        return redirect(url_for('home'))
    return render_template('update_user.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
