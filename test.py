# Define the logic to update 'tableCombined' based on 'tableIOS' and 'tableAndroid'
def update_combined_table():
    # Drop existing 'tableCombined' if it exists
    cursor.execute("DROP TABLE IF EXISTS tableCombined")

    # Create 'tableCombined'
    cursor.execute(
        """
        CREATE TABLE tableCombined (
            Date TEXT,
            'App Name' TEXT,
            'Avg App Rating' REAL,
            'Total Reviews' INTEGER,
            'iOS App Rating' REAL,
            'iOS Total Reviews' INTEGER,
            'Android App Rating' REAL,
            'Android Total Reviews' INTEGER
        )
    """
    )

    # Merge data from 'tableIOS' and 'tableAndroid' and insert into 'tableCombined'
    cursor.execute(
        """
        INSERT INTO tableCombined (
            'Date',
            'App Name',
            'Avg App Rating',
            'Total Reviews',
            'iOS App Rating',
            'iOS Total Reviews',
            'Android App Rating',
            'Android Total Reviews'
        )
        SELECT
            t1.'Date',
            t2.'App Name',
            ROUND((t1.'iOS App Rating' + t2.'Android App Rating') / 2,2) AS 'Avg App Rating',
            t1.'iOS Total Reviews' + t2.'Android Total Reviews' AS 'Total Reviews',
            ROUND(t1.'iOS App Rating', 2) AS 'iOS App Rating',
            t1.'iOS Total Reviews',
            ROUND(t2.'Android App Rating', 2) AS 'Android App Rating',
            t2.'Android Total Reviews'
        FROM
            tableIOS AS t1
        INNER JOIN
            tableAndroid AS t2
        ON
            t1.Mapping = t2.Mapping AND t1.Date = t2.Date
    """
    )

    # Commit the changes to the database
    conn.commit()


# Call the update_combined_table() function to update 'tableCombined'
update_combined_table()

# Close the database connection
conn.close()
