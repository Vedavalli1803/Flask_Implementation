class a():
    def xoxo(self,name):
        import pandas as pd
        import seaborn as sns
        import matplotlib.pyplot as plt
        from sklearn.cluster import KMeans
        from sklearn import neighbors
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import MinMaxScaler
        import warnings
        warnings.filterwarnings("ignore")

        data = pd.read_csv("/Users/veda/Downloads/books.csv",error_bad_lines = False)

        data.head()

        data.isnull().sum()

        data.describe()

        top_ten = data[data['ratings_count'] > 1000000]
        data_1 = top_ten.sort_values(by='average_rating', ascending=False).head(10)

        most_books = data.groupby('authors')['title'].count().reset_index().sort_values('title', ascending=False).head(10).set_index('authors')
        #ax = sns.barplot(most_books['title'], most_books.index)
        #totals = []
        #for i in ax.patches:
        #    totals.append(i.get_width())
        #total = sum(totals)
        #for i in ax.patches:
        #    ax.text(i.get_width()+.2, i.get_y()+.2,str(round(i.get_width())), fontsize=15,color='black')

        most_rated = data.sort_values('ratings_count', ascending = False).head(10).set_index('title')
        #ax = sns.barplot(most_rated['ratings_count'], most_rated.index, palette = 'inferno')
        #totals = []
        #for i in ax.patches:
        #    totals.append(i.get_width())
        #total = sum(totals)
        #for i in ax.patches:
        #    ax.text(i.get_width()+.2, i.get_y()+.2,str(round(i.get_width())), fontsize=15,color='black')

        data.average_rating = data.average_rating.astype(float)
        #fig, ax = plt.subplots(figsize=[15,10])

        #ax = sns.relplot(data=data, x="average_rating", y="ratings_count", color = 'red', sizes=(100, 200), height=7, marker='o')

        #ax = sns.relplot(x="average_rating", y="  num_pages", data = data, color = 'red',sizes=(100, 200), height=7, marker='o')

        data_2 = data.copy()

        data_2.loc[ (data_2['average_rating'] >= 0) & (data_2['average_rating'] <= 1), 'rating_between'] = "between 0 and 1"
        data_2.loc[ (data_2['average_rating'] > 1) & (data_2['average_rating'] <= 2), 'rating_between'] = "between 1 and 2"
        data_2.loc[ (data_2['average_rating'] > 2) & (data_2['average_rating'] <= 3), 'rating_between'] = "between 2 and 3"
        data_2.loc[ (data_2['average_rating'] > 3) & (data_2['average_rating'] <= 4), 'rating_between'] = "between 3 and 4"
        data_2.loc[ (data_2['average_rating'] > 4) & (data_2['average_rating'] <= 5), 'rating_between'] = "between 4 and 5"

        rating_data = pd.get_dummies(data_2['rating_between'])
        language_data = pd.get_dummies(data_2['language_code'])

        features = pd.concat([rating_data, 
                            language_data, 
                            data_2['average_rating'], 
                            data_2['ratings_count']], axis=1)

        from sklearn.preprocessing import MinMaxScaler
        min_max_scaler = MinMaxScaler()
        features = min_max_scaler.fit_transform(features)

        model = neighbors.NearestNeighbors(n_neighbors=6, algorithm='ball_tree')
        model.fit(features)
        dist, idlist = model.kneighbors(features)

        book_list_name = []
        book_id = data_2[data_2['title'] == name].index
        book_id = book_id[0]
        for newid in idlist[book_id]:
            book_list_name.append(data_2.loc[newid].title)
        print(book_list_name)
        return book_list_name
    



