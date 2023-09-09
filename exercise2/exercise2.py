import mysql.connector

conn = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password"
)


cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS stephen_king_adaptations")
cursor.execute("USE stephen_king_adaptations")


cursor.execute('''CREATE TABLE IF NOT EXISTS adaptations
                  (id INT AUTO_INCREMENT PRIMARY KEY,
                   movie_name VARCHAR(255),
                   release_year INT,
                   rating FLOAT)''')
with open("stephen_king_adaptations.txt", "r") as file:
    adaptations_list = file.readlines()

for adaptation in adaptations_list:
    movie_name, release_year, rating = adaptation.strip().split(',')
    cursor.execute("INSERT INTO adaptations (movie_name, release_year, rating) VALUES (%s, %s, %s)",
                   (movie_name, int(release_year), float(rating)))

conn.commit()
while True:
    print("Please select the action to perform:")
    print("1. Query movie names")
    print("2. Query movie year")
    print("3. Query movie ratings")
    print("4. cease")

    choice = input("Please enter an option: ")

    if choice == '1':
        movie_name = input("Please enter the movie name to query: ")
        cursor.execute("SELECT * FROM adaptations WHERE movie_name=%s", (movie_name,))
        result = cursor.fetchone()

        if result:
            print("Movie Title:", result[1])
            print("Film Year:", result[2])
            print("Movie rating:", result[3])
        else:
            print("We cannot find this movie in our database.")

    elif choice == '2':
        year = input("Please enter the year of the movie you want to query: ")
        cursor.execute("SELECT * FROM adaptations WHERE release_year=%s", (year,))
        results = cursor.fetchall()

        if results:
            for result in results:
             print("Movie Title:", result[1])
            print("Film Year:", result[2])
            print("Movie rating:", result[3])
        else:
            print("No movies of that year were found in our database.")

    elif choice == '3':
        rating = float(input("Please enter the movie rating you want to query:"))
        cursor.execute("SELECT * FROM adaptations WHERE rating >= %s", (rating,))
        results = cursor.fetchall()

        if results:
            for result in results:
             print("Movie Title:", result[1])
            print("Film Year:", result[2])
            print("Movie rating:", result[3])
        else:
            print("There are no movies found in our database that have a rating higher than this.")

    elif choice == '4':
        break

    else:
        print("Invalid option, please re-enter.")

# 关闭数据库连接
conn.close()