from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
from dbcode import *
from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Users')

@app.route('/')
def home():
    results = show_movies()
    return render_template('home.html',results=results)




#---CRUD dynamo routes----

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
