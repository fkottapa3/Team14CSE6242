########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv

#################################################################################

## Change to False to disable Sample
SHOW = True


############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample:
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print("\033[32m" + "Sample: " + "\033[m")

        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)", ("1", "test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())


######################################################################


class HW2_sql:
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))

        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)

    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "fkottapa3"
        return gt_username

    # Part 1.a.i Create Tables [2 points]
    def part_1_a_i(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_1_a_i_sql = """
        CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        score REAL
        );
        """
        ######################################################################

        return self.execute_query(connection, part_1_a_i_sql)

    def part_1_a_ii(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_1_a_ii_sql = """
        CREATE TABLE IF NOT EXISTS movie_cast (
        movie_id INTEGER,
        cast_id INTEGER,
        cast_name TEXT,
        birthday TEXT,
        popularity REAL,
        PRIMARY KEY (movie_id, cast_id)
        );
        """
        ######################################################################

        return self.execute_query(connection, part_1_a_ii_sql)

    # Part 1.b Import Data [2 points]
    def part_1_b_movies(self, connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        cursor = connection.cursor()
        try:
            with open(path, "r") as moviescsv:
                reader = csv.reader(moviescsv)
                # next(reader)
                for row in reader:
                    cursor.execute(
                        "INSERT INTO movies (id, title, score) \
                                VALUES (?, ?, ?)",
                        row,
                    )
            connection.commit()
        except Exception as e:
            print(f"Error in moviescsv connect: {e}")

        ######################################################################

        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    def part_1_b_movie_cast(self, connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        cursor = connection.cursor()
        try:
            with open(path, "r") as moviecastcsv:
                reader = csv.reader(moviecastcsv)
                # next(reader)
                for row in reader:
                    cursor.execute(
                        "INSERT INTO movie_cast (movie_id, cast_id, cast_name, birthday, popularity) \
                        VALUES (?, ?, ?, ?, ?)",
                        row,
                    )
            connection.commit()
        except Exception as e:
            print(f"Error in moviecastcsv connect: {e}")

        ######################################################################

        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part 1.c Vertical Database Partitioning [5 points]
    def part_1_c(self, connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_1_c_sql = """
            CREATE TABLE IF NOT EXISTS cast_bio (
            cast_id INTEGER,
            cast_name TEXT,
            birthday TEXT,
            popularity REAL,
            PRIMARY KEY (cast_id)
        );
        """
        ######################################################################
        try:
            self.execute_query(connection, part_1_c_sql)

            ############### CREATE IMPORT CODE BELOW ############################
            part_1_c_insert_sql = """
                INSERT INTO cast_bio (cast_id, cast_name, birthday, popularity)
                SELECT DISTINCT cast_id, cast_name, birthday, popularity
                FROM movie_cast;
            """
            ######################################################################

            self.execute_query(connection, part_1_c_insert_sql)

            sql = "SELECT COUNT(cast_id) FROM cast_bio;"
            cursor = connection.execute(sql)
            return cursor.fetchall()[0][0]
        except Exception as e:
            print(f"Error in insert for cast_bio: {e}")
            return 0

    # Part 2 Create Indexes [1 points]
    def part_2_a(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_2_a_sql = """
            CREATE INDEX IF NOT EXISTS movie_index ON movies(id);
        """
        ######################################################################
        return self.execute_query(connection, part_2_a_sql)

    def part_2_b(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_2_b_sql = """
            CREATE INDEX IF NOT EXISTS cast_index ON movie_cast(cast_id);
        """
        ######################################################################
        return self.execute_query(connection, part_2_b_sql)

    def part_2_c(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_2_c_sql = """
            CREATE INDEX IF NOT EXISTS cast_bio_index ON cast_bio(cast_id);
        """
        ######################################################################
        return self.execute_query(connection, part_2_c_sql)

    # Part 3 Calculate a Proportion [3 points]
    def part_3(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_3_sql = """ 
            SELECT
                ROUND(100.0 * 
                        (SELECT COUNT(*) FROM movies WHERE score BETWEEN 7 AND 20)
                            / 
                        (SELECT COUNT(*) FROM movies)
                     , 2);

        """
        ######################################################################
        cursor = connection.execute(part_3_sql)
        result = cursor.fetchall()

        formatted_result = f"{result[0][0]:.2f}"
        # return cursor.fetchall()[0][0]
        return formatted_result

    # Part 4 Find the Most Prolific Actors [4 points]
    def part_4(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_4_sql = """ 
            SELECT  mcast.cast_name, COUNT(mcast.movie_id) AS hinumappearcnt
                    FROM movie_cast mcast
                    INNER JOIN 
                    cast_bio castbio ON mcast.cast_id = castbio.cast_id
                    WHERE castbio.popularity > 10
                    GROUP BY  mcast.cast_name
                    ORDER BY  hinumappearcnt DESC, mcast.cast_name ASC
                    LIMIT 5;
        """
        ######################################################################
        cursor = connection.execute(part_4_sql)
        result = cursor.fetchall()
        # print("Raw result:", result)

        result_formatted = []

        # result_formatted = [
        #    (f"{cast_name},{appearance_count}", "")
        #    for cast_name, appearance_count in result
        # ]
        result_formatted = [
            (cast_name, appearance_count) for cast_name, appearance_count in result
        ]

        # for formatted in result_formatted:
        #    print(f"Formatted result: {formatted}")
        # result_formatted = result
        # return cursor.fetchall()
        return result_formatted
        # return result

    # Part 5 Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_5(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_5_sql = """
            SELECT movies.title, movies.score, COUNT(cast_id) AS cntcastid
            FROM movies
            LEFT JOIN
            movie_cast moviecast ON movies.id = moviecast.movie_id
            GROUP BY
            movies.id, movies.title, movies.score
            ORDER BY
            movies.score DESC,
            cntcastid ASC, 
            movies.title ASC
            LIMIT 5;
        """
        ######################################################################
        cursor = connection.execute(part_5_sql)
        result = cursor.fetchall()

        # formatted_result = f"{result[0][0]:.2f}"
        formatted_result = [
            (movie_title, f"{float(score):.2f}", cast_count)
            for movie_title, score, cast_count in result
        ]
        return formatted_result

    # Part 6 Get High Scoring Actors [4 points]
    def part_6(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_6_sql = """
        WITH movie_scores_ge_25 AS (
            SELECT
                mcast.cast_id,
                mcast.cast_name,
                movies.score
             FROM
                movie_cast mcast
             JOIN
                movies movies
             ON
                mcast.movie_id = movies.id
            WHERE
                movies.score >= 25
        ),
        cast_movie_count_ge_3 AS (
            SELECT
                cast_id,
                cast_name,
                COUNT(*) AS movie_count,
                AVG(score) AS average_score
            FROM
                movie_scores_ge_25
            GROUP BY
                cast_id, cast_name
            HAVING
                COUNT(*) >= 3
        ),
        top_ten_high_scoring_actors AS (
            SELECT
                cast_id,
                cast_name,
                average_score
            FROM
                cast_movie_count_ge_3
            ORDER BY
                average_score DESC,
                cast_name ASC
            LIMIT 10
        )
        SELECT 
            cast_id,
            cast_name,
            ROUND(average_score, 2) AS average_score
        FROM 
            top_ten_high_scoring_actors;        
        """
        ######################################################################
        cursor = connection.execute(part_6_sql)
        result = cursor.fetchall()

        formatted_result = [
            (cast_id, cast_name, f"{float(average_score):.2f}")
            for cast_id, cast_name, average_score in result
        ]
        return formatted_result

    # Part 7 Creating Views [6 points]
    def part_7(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_7_sql = """
        CREATE VIEW good_collaboration AS
        WITH 
        pair_of_actors AS (
            SELECT
                CASE
                    WHEN c1.cast_id < c2.cast_id THEN c1.cast_id
                    ELSE c2.cast_id
                END AS cast_member_id1,
                CASE
                    WHEN c1.cast_id < c2.cast_id THEN c2.cast_id
                    ELSE c1.cast_id
                END AS cast_member_id2,
                c1.movie_id
            FROM
                movie_cast c1
            JOIN
                movie_cast c2
                ON c1.movie_id = c2.movie_id
            WHERE
                c1.cast_id < c2.cast_id
        ),
        actor_movie_stats AS (
            SELECT
                pair_of_actors.cast_member_id1,
                pair_of_actors.cast_member_id2,
                COUNT(DISTINCT pair_of_actors.movie_id) AS movie_count,
                AVG(m.score) AS average_movie_score
            FROM
                pair_of_actors
            JOIN
                movies m
                ON pair_of_actors.movie_id = m.id
            GROUP BY
                pair_of_actors.cast_member_id1,
                pair_of_actors.cast_member_id2
        )
        SELECT
            cast_member_id1,
            cast_member_id2,
            movie_count,
            average_movie_score
        FROM
            actor_movie_stats
        WHERE
            movie_count >= 2
            AND average_movie_score >= 40;
        """
        ######################################################################
        return self.execute_query(connection, part_7_sql)

    def part_8(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_8_sql = """
        WITH collaboration_score AS (
            SELECT  
                    AVG(average_movie_score) AS collaboration_score,
                    cast_member_id1 AS cast_id
            FROM 
                    good_collaboration
            GROUP BY
                    cast_member_id1

            UNION ALL

            SELECT  
                    AVG(average_movie_score) AS collaboration_score,
                    cast_member_id2 AS cast_id
            FROM 
                    good_collaboration
            GROUP BY
                    cast_member_id2
        ),
        highest_average_scores AS (
            SELECT  
                    cast_id,
                    AVG(collaboration_score) AS collaboration_score
            FROM 
                    collaboration_score
            GROUP BY
                    cast_id
        )
        SELECT
                ascore.cast_id,
                castbio.cast_name,
                printf('%.2f', ascore.collaboration_score) AS collaboration_score
        FROM 
                highest_average_scores ascore
        JOIN
                cast_bio castbio
                ON
                ascore.cast_id = castbio.cast_id
        ORDER BY
                ascore.collaboration_score DESC,
                castbio.cast_name ASC
        LIMIT 5;

        """
        ######################################################################
        cursor = connection.execute(part_8_sql)
        return cursor.fetchall()

    # Part 9 FTS [4 points]
    def part_9_a(self, connection, path):
        try:
            part_9_a_sql = """
                CREATE VIRTUAL TABLE IF NOT EXISTS movie_overview USING fts4(
                  id INTEGER,
                  overview TEXT
                )
            """
            connection.execute(part_9_a_sql)

            with open(path, "r") as csv_file:
                cursor = connection.cursor()
                cursor.executemany(
                    "INSERT INTO movie_overview (id, overview) VALUES (?, ?);",
                    csv.reader(csv_file),
                )
                connection.commit()

            sql = "SELECT COUNT(id) FROM movie_overview;"
            result = connection.execute(sql)
            return result.fetchone()[0]

        except Exception as e:
            print(f"Error in part_9_a: {e}")
            return 0

    def part_9_b(self, connection):
        try:
            ############### EDIT SQL STATEMENT ###################################
            part_9_b_sql = """
                SELECT COUNT(*)
                FROM movie_overview
                WHERE overview MATCH 'fight'
            """

            result = connection.execute(part_9_b_sql)
            return result.fetchone()[0]
        ######################################################################
        except Exception as e:
            print(f"Error in part_9_b: {e}")
            return 0

    def part_9_c(self, connection):
        try:
            ############### EDIT SQL STATEMENT ###################################
            space_query = """
                    SELECT id, overview
                    FROM movie_overview
                    WHERE overview MATCH 'space';
            """
            space_rows = connection.execute(space_query).fetchall()
            print(f"Rows containing 'space': {len(space_rows)}")

            program_query = """
                    SELECT id, overview
                    FROM movie_overview
                    WHERE overview MATCH 'program';
            """
            program_rows = connection.execute(program_query).fetchall()
            print(f"Rows containing 'program': {len(program_rows)}")

            part_9_c_sql = """
                    SELECT COUNT(*)
                    FROM movie_overview
                    WHERE overview MATCH 'space NEAR/5 program';
            """

            result = connection.execute(part_9_c_sql)
            return result.fetchone()[0]
        ######################################################################
        except Exception as e:
            print(f"Error in part_9_c: {e}")
            return 0


if __name__ == "__main__":

    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print("\033[32m" + "Q2 Output: " + "\033[m")
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except Exception as e:
        print("Error in Table Drops")
        print(e)

    try:
        print("\033[32m" + "part 1.a.i: " + "\033[m" + str(db.part_1_a_i(conn)))
        print("\033[32m" + "part 1.a.ii: " + "\033[m" + str(db.part_1_a_ii(conn)))
    except Exception as e:
        print("Error in Part 1.a")
        print(e)

    try:
        print(
            "\033[32m"
            + "Row count for Movies Table: "
            + "\033[m"
            + str(db.part_1_b_movies(conn, "data/movies.csv"))
        )
        print(
            "\033[32m"
            + "Row count for Movie Cast Table: "
            + "\033[m"
            + str(db.part_1_b_movie_cast(conn, "data/movie_cast.csv"))
        )
    except Exception as e:
        print("Error in part 1.b")
        print(e)

    try:
        print(
            "\033[32m"
            + "Row count for Cast Bio Table: "
            + "\033[m"
            + str(db.part_1_c(conn))
        )
    except Exception as e:
        print("Error in part 1.c")
        print(e)

    try:
        print("\033[32m" + "part 2.a: " + "\033[m" + db.part_2_a(conn))
        print("\033[32m" + "part 2.b: " + "\033[m" + db.part_2_b(conn))
        print("\033[32m" + "part 2.c: " + "\033[m" + db.part_2_c(conn))
    except Exception as e:
        print("Error in part 2")
        print(e)

    try:
        print("\033[32m" + "part 3: " + "\033[m" + str(db.part_3(conn)))
    except Exception as e:
        print("Error in part 3")
        print(e)

    try:
        print("\033[32m" + "part 4: " + "\033[m")
        for line in db.part_4(conn):
            print(line[0], line[1])
    except Exception as e:
        print("Error in part 4")
        print(e)

    try:
        print("\033[32m" + "part 5: " + "\033[m")
        for line in db.part_5(conn):
            print(line[0], line[1], line[2])
    except Exception as e:
        print("Error in part 5")
        print(e)

    try:
        print("\033[32m" + "part 6: " + "\033[m")
        for line in db.part_6(conn):
            print(line[0], line[1], line[2])
    except Exception as e:
        print("Error in part 6")
        print(e)

    try:
        print("\033[32m" + "part 7: " + "\033[m" + str(db.part_7(conn)))
        print(
            "\033[32mRow count for good_collaboration view:\033[m",
            conn.execute("select count(*) from good_collaboration").fetchall()[0][0],
        )
        print("\033[32m" + "part 8: " + "\033[m")
        for line in db.part_8(conn):
            print(line[0], line[1], line[2])
    except Exception as e:
        print("Error in part 7 and/or 8")
        print(e)

    try:
        print(
            "\033[32m"
            + "part 9.a: "
            + "\033[m"
            + str(db.part_9_a(conn, "data/movie_overview.csv"))
        )
        print("\033[32m" + "Count 9.b: " + "\033[m" + str(db.part_9_b(conn)))
        print("\033[32m" + "Count 9.c: " + "\033[m" + str(db.part_9_c(conn)))
    except Exception as e:
        print("Error in part 9")
        print(e)

    conn.close()
    #################################################################################
    #################################################################################
