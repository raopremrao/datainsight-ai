from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # This will create the database file and tables if they don't exist
        db.create_all() 
    app.run(debug=True)