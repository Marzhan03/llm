import psycopg2 
 
connection = psycopg2.connect( 
    database="llm_news_db", 
    user="postgres", 
    password="admin", 
    host="localhost", 
)
 
cursor = connection.cursor() 
cursor.execute(""" 
    CREATE TABLE location ( 
               id SERIAL PRIMARY KEY,  
               name VARCHAR(255) NOT NULL 
    ); 
 
    CREATE TABLE category ( 
               id SERIAL PRIMARY KEY,  
               name VARCHAR(255) NOT NULL 
    ); 
 
    CREATE TABLE site ( 
               id SERIAL PRIMARY KEY,  
               name VARCHAR(255) NOT NULL 
    ); 
                
    CREATE TABLE news ( 
               id SERIAL PRIMARY KEY,  
               title VARCHAR(255) NOT NULL, 
               content TEXT NOT NULL, 
               summarized_content TEXT NOT NULL,
               old_id INT NOT NULL, 
               date DATE NOT NULL, 
               category_id INT NOT NULL, 
               location_id INT NOT NULL, 
               is_read BOOLEAN NOT NULL DEFAULT false,
               site_id INT NOT NULL, 
               FOREIGN KEY (category_id) 
               REFERENCES category (id) 
               ON UPDATE CASCADE ON DELETE CASCADE, 
               FOREIGN KEY (location_id) 
               REFERENCES location (id) 
               ON UPDATE CASCADE ON DELETE CASCADE, 
               FOREIGN KEY (site_id) 
               REFERENCES site (id) 
               ON UPDATE CASCADE ON DELETE CASCADE 
    )""" 
)              
 
connection.commit() 
connection.close()
