
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template
import pandas as pd
import numpy as np

#Load csv
genres_df=pd.read_csv('/home/lin2yu/data/selectedmoviesgenres.csv', encoding='latin-1')
selected_movies=pd.read_csv('/home/lin2yu/data/selectedmovies_infor.csv')
raw_movies_data = pd.read_csv('/home/lin2yu/data/CleanedMovies.csv', encoding='latin-1')

#Load pkl
Rating_df = pd.read_pickle('Part_of_Rating.pkl')
movies_data = raw_movies_data.loc[raw_movies_data['movieId'].isin(Rating_df.columns.values)]

#Build Dictionary
movie_dict = dict(zip(movies_data.title, movies_data.movieId))
selected_id = np.array(selected_movies.id, dtype=pd.Series)
lower_case_movie_dict = {k.lower(): v for k, v in movie_dict.items()}

#Load Previously Trained Low_Dim_Rating matrix
vt = np.load("/home/lin2yu/data/Low_dim_data.npy")

#Define Relative Functions
def get_url_name(genres_df, movie_df, args='Comdedy', top_k=10, condition='rtAudienceScore'):
    get_id = genres_df[genres_df.genres.apply(lambda x: args in x.split('|'))].movieId
    get_content = movie_df[movie_df.id.apply(lambda x: x in list(get_id))].sort_values(condition, ascending=False).iloc[:top_k]
    return get_content[['title','rtAllCriticsScore', 'rtAudienceScore', 'rtPictureURL']]



def top_cosine_similarity(low_dim_data, movie_name, top_n):
    movie_name = movie_name.replace('+', ' ')
    low_case_movie_name = movie_name.lower()
    if low_case_movie_name in lower_case_movie_dict:
        index = Rating_df.columns.get_loc(lower_case_movie_dict[low_case_movie_name])
        movie_row = low_dim_data[:, index]
        magnitude = np.sqrt(np.einsum('ij, ij -> i', low_dim_data.T, low_dim_data.T))
        similarity = np.dot(movie_row, low_dim_data) / (magnitude[index] * magnitude)
        pre_sort_indexes = np.argsort(-similarity)
        sort_indexes = np.delete(pre_sort_indexes, 0)
        top_movie_id = Rating_df.columns[sort_indexes]
        frozen_selected_id = frozenset(selected_id)
        selected_top_movie_id = [x for x in top_movie_id if x in frozen_selected_id][:top_n]
        return selected_top_movie_id
    else:
        return("Sorry, no matching found in the dataset")



def get_movie_infor(movie_df, movie_id):
    indexes = []
    for id in movie_id:
        index = movie_df[movie_df['id']==id].index.astype(int)[0]
        indexes.append(index)
    get_content = movie_df.iloc[indexes]
    return get_content[['title','rtAllCriticsScore', 'rtAudienceScore', 'rtPictureURL']]


def recom_based_on_movie(low_dim_data, input_movie_name, top_n, movie_df):
    recom_ids = top_cosine_similarity(low_dim_data, input_movie_name, top_n)
    return get_movie_infor(movie_df, recom_ids)



def recom_based_on_genre(genres_df, movie_df, args='Comdedy', top_k=10, condition='rtAudienceScore'):
    get_id = genres_df[genres_df.genres.apply(lambda x: args in x.split('|'))].movieId
    get_content = movie_df[movie_df.id.apply(lambda x: x in list(get_id))].sort_values(condition, ascending=False).iloc[:top_k]
    return get_content[['title','rtAllCriticsScore', 'rtAudienceScore', 'rtPictureURL']]



app = Flask(__name__)

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/recomdationonmovies/')
def reconmovies():
    return render_template('reconmovies.html')

@app.route('/recomdationonmovies/<input_movie>')
def reconmoviesinput(input_movie):
    input_movie_title = input_movie[7:]
    search_input = input_movie_title.upper()
    low_case_input_movie = input_movie_title.lower()

    if low_case_input_movie in lower_case_movie_dict:

        movie_result = recom_based_on_movie(vt, low_case_input_movie, 10, selected_movies)
        movie1 = movie_result.iloc[0].title
        movie2 = movie_result.iloc[1].title
        movie3 = movie_result.iloc[2].title
        movie4 = movie_result.iloc[3].title
        movie5 = movie_result.iloc[4].title
        movie6 = movie_result.iloc[5].title
        movie7 = movie_result.iloc[6].title
        movie8 = movie_result.iloc[7].title
        movie9 = movie_result.iloc[8].title
        movie10 = movie_result.iloc[9].title
        user_score1 = int(round(movie_result.iloc[0].rtAudienceScore))
        user_score2 = int(round(movie_result.iloc[1].rtAudienceScore))
        user_score3 = int(round(movie_result.iloc[2].rtAudienceScore))
        user_score4 = int(round(movie_result.iloc[3].rtAudienceScore))
        user_score5 = int(round(movie_result.iloc[4].rtAudienceScore))
        user_score6 = int(round(movie_result.iloc[5].rtAudienceScore))
        user_score7 = int(round(movie_result.iloc[6].rtAudienceScore))
        user_score8 = int(round(movie_result.iloc[7].rtAudienceScore))
        user_score9 = int(round(movie_result.iloc[8].rtAudienceScore))
        user_score10 = int(round(movie_result.iloc[9].rtAudienceScore))
        url1 = movie_result.iloc[0].rtPictureURL
        url2 = movie_result.iloc[1].rtPictureURL
        url3 = movie_result.iloc[2].rtPictureURL
        url4 = movie_result.iloc[3].rtPictureURL
        url5 = movie_result.iloc[4].rtPictureURL
        url6 = movie_result.iloc[5].rtPictureURL
        url7 = movie_result.iloc[6].rtPictureURL
        url8 = movie_result.iloc[7].rtPictureURL
        url9 = movie_result.iloc[8].rtPictureURL
        url10 = movie_result.iloc[9].rtPictureURL

        return render_template('reconmovies_output.html', search_input=search_input,
        movie1=movie1, movie2=movie2, movie3=movie3, movie4=movie4, movie5=movie5,
        movie6=movie6, movie7=movie7, movie8=movie8, movie9=movie9, movie10=movie10,
        user_score1=user_score1, user_score2=user_score2, user_score3=user_score3,
        user_score4=user_score4, user_score5=user_score5, user_score6=user_score6,
        user_score7=user_score7, user_score8=user_score8, user_score9=user_score9,
        user_score10=user_score10, url1=url1, url2=url2, url3=url3, url4=url4,
        url5=url5, url6=url6, url7=url7, url8=url8, url9=url9, url10=url10)

    else:
        return render_template('nomatch.html', search_input=search_input)



@app.route('/recom_on_genres/<genre>')
def genrerecom(genre):
    arg = str(genre)
    genre_result = get_url_name(genres_df, selected_movies, args=arg, top_k=10, condition='rtAudienceScore')

    movie1 = genre_result.iloc[0].title
    movie2 = genre_result.iloc[1].title
    movie3 = genre_result.iloc[2].title
    movie4 = genre_result.iloc[3].title
    movie5 = genre_result.iloc[4].title
    movie6 = genre_result.iloc[5].title
    movie7 = genre_result.iloc[6].title
    movie8 = genre_result.iloc[7].title
    movie9 = genre_result.iloc[8].title
    movie10 = genre_result.iloc[9].title
    user_score1 = int(round(genre_result.iloc[0].rtAudienceScore))
    user_score2 = int(round(genre_result.iloc[1].rtAudienceScore))
    user_score3 = int(round(genre_result.iloc[2].rtAudienceScore))
    user_score4 = int(round(genre_result.iloc[3].rtAudienceScore))
    user_score5 = int(round(genre_result.iloc[4].rtAudienceScore))
    user_score6 = int(round(genre_result.iloc[5].rtAudienceScore))
    user_score7 = int(round(genre_result.iloc[6].rtAudienceScore))
    user_score8 = int(round(genre_result.iloc[7].rtAudienceScore))
    user_score9 = int(round(genre_result.iloc[8].rtAudienceScore))
    user_score10 = int(round(genre_result.iloc[9].rtAudienceScore))
    url1 = genre_result.iloc[0].rtPictureURL
    url2 = genre_result.iloc[1].rtPictureURL
    url3 = genre_result.iloc[2].rtPictureURL
    url4 = genre_result.iloc[3].rtPictureURL
    url5 = genre_result.iloc[4].rtPictureURL
    url6 = genre_result.iloc[5].rtPictureURL
    url7 = genre_result.iloc[6].rtPictureURL
    url8 = genre_result.iloc[7].rtPictureURL
    url9 = genre_result.iloc[8].rtPictureURL
    url10 = genre_result.iloc[9].rtPictureURL

    return render_template('genres_output.html', genre=genre,
    movie1=movie1, movie2=movie2, movie3=movie3, movie4=movie4, movie5=movie5,
    movie6=movie6, movie7=movie7, movie8=movie8, movie9=movie9, movie10=movie10,
    user_score1=user_score1, user_score2=user_score2, user_score3=user_score3,
    user_score4=user_score4, user_score5=user_score5, user_score6=user_score6,
    user_score7=user_score7, user_score8=user_score8, user_score9=user_score9,
    user_score10=user_score10, url1=url1, url2=url2, url3=url3, url4=url4,
    url5=url5, url6=url6, url7=url7, url8=url8, url9=url9, url10=url10)
