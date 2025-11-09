from pymongo import MongoClient
import certifi


def loud_data_mg(data):
    if not data:
        raise ValueError("No data to insert into MongoDB")

    username = "kfir571"
    password = "KfirDana"
    uri = "mongodb+srv://kfir571:" + password + "@cluster2.lqabsiv.mongodb.net/?appName=Cluster2"
    client = MongoClient(uri, tlsCAFile=certifi.where())

 
    try:
        database = client.get_database("sample_mflix")
        movies = database.get_collection("movies")

        # Query for a movie that has the title 'Back to the Future'
        # query = { "title": "Back to the Future kkkkkkkkkkk" }
        movie = movies.insert_many(data)

        print(movie)

        client.close()

    except openai.OpenAIError as e:
        log.error("OpenAI error", exc_info=True)
        raise Exception("Unable to find the document due to the following error: ") from e

    finally:
        client.close()
