from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from flask_table import Table, Col

# Membangun tabel Flask untuk tampilan hasil rekomendasi
class Results(Table):
    id = Col('Id', show=False)
    title = Col('Daftar Rekomendasi')

app = Flask(__name__)

# Halaman Selamat Datang
@app.route("/")
def welcome():
    return render_template('index.html')

# Halaman Penilaian
@app.route("/nilai", methods=["GET", "POST"])
def nilai():
    if request.method == "POST":
        return render_template('rekomendasi.html')
    return render_template('halaman_nilai.html')

# Halaman Hasil Rekomendasi
@app.route("/rekomendasi", methods=["GET", "POST"])
def rekomendasi():
    if request.method == 'POST':
        # Membaca dataset asli
        movies = pd.read_csv('movies.csv')

        # Memisahkan genre untuk setiap film
        movies = pd.concat([movies, movies.genres.str.get_dummies(sep='|')], axis=1)

        # Menghapus variabel untuk mendapatkan matriks dummy 1-0 film dan genre mereka
        categories = movies.drop(['title', 'genres', 'IMAX', 'movieId'], axis=1)

        # Menginisialisasi daftar preferensi pengguna yang akan berisi peringkat pengguna
        preferences = []

        # Membaca nilai peringkat yang diberikan oleh pengguna di tampilan
        Action = request.form.get('Action')
        Adventure = request.form.get('Adventure')
        Children = request.form.get('Children')
        Animation = request.form.get('Animation')
        Documentary = request.form.get('Documentary')
        Comedy = request.form.get('Comedy')
        Crime = request.form.get('Crime')
        Drama = request.form.get('Drama')
        Fantasy = request.form.get('Fantasy')
        FilmNoir = request.form.get('FilmNoir')
        Horror = request.form.get('Horror')
        Mystery = request.form.get('Mystery')
        SciFi = request.form.get('SciFi')
        Romance = request.form.get('Romance')
        War = request.form.get('War')
        Western = request.form.get('Western')
        Thriller = request.form.get('Thriller')
        Musical = request.form.get('Musical')

        # Memasukkan setiap peringkat ke dalam posisi tertentu berdasarkan matriks film-genre
        preferences.insert(0, int(Action))
        preferences.insert(1, int(Adventure))
        preferences.insert(2, int(Children))
        preferences.insert(3, int(Animation))
        preferences.insert(4, int(Documentary))
        preferences.insert(5, int(Comedy))
        preferences.insert(6, int(Crime))
        preferences.insert(7, int(Drama))
        preferences.insert(8, int(Fantasy))
        preferences.insert(9, int(FilmNoir))
        preferences.insert(10, int(Horror))
        preferences.insert(11, int(Mystery))
        preferences.insert(12, int(SciFi))
        preferences.insert(13, int(Romance))
        preferences.insert(14, int(War))
        preferences.insert(15, int(Western))
        preferences.insert(16, int(Thriller))
        preferences.insert(17, int(Musical))

        # Fungsi ini akan mendapatkan skor setiap film berdasarkan peringkat pengguna melalui dot product
        def get_score(a, b):
            return np.dot(a, b)
        
        # Menghasilkan rekomendasi berdasarkan film dengan skor tertinggi
        def rekomendasis(X, n_rekomendasis):
            movies['score'] = get_score(categories, preferences)
            return movies.sort_values(by=['score'], ascending=False)['title'][:n_rekomendasis]
        
        # Mencetak rekomendasi teratas-20
        output = rekomendasis(preferences, 20)
        table = Results(output)
        table.border = True
        return render_template('rekomendasi.html', table=table)

if __name__ == '__main__':
    app.run(debug=True)