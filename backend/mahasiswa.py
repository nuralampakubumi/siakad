from flask import Blueprint, redirect, render_template, url_for, jsonify, flash, request
from backend.auth import login_required
from backend.db import db, get_all_collection, storage

mahasiswa = Blueprint('mahasiswa', __name__)

@mahasiswa.route('/mahasiswa')
@login_required
def daftar_mahasiswa():
    daftar_mahasiswa = get_all_collection('mahasiswa')
    return render_template('mahasiswa.html', mahasiswa=daftar_mahasiswa)

@mahasiswa.route('/mahasiswa/tambah_mahasiswa', methods=['POST', 'GET'])
@login_required
def tambah_mahasiswa():
    if request.method == 'POST':
        data = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'jurusan' : request.form['jurusan'],
            'email' : request.form['email'],
            'umur' : request.form['umur'],
            'status' : request.form['status'],
        }

        if 'image' in request.files and request.files['image']:
            image = request.files['image']
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            filename = image.filename
            lokasi = f"mahasiswa/{filename}"
            ext = filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                storage.child(lokasi).put(image)
                data['photoURL'] = storage.child(lokasi).get_url(None)
            else:
                flash("Foto tidak diperbolehkan", "danger")
                return redirect(url_for('.tambah_mahasiswa'))

        db.collection('mahasiswa').document().set(data)
        flash("Berhasil Menambahkan Data", "success")
        return redirect(url_for('mahasiswa.daftar_mahasiswa'))
    return render_template('tambah_mahasiswa.html')

@mahasiswa.route('/mahasiswa/view/<uid>')
@login_required
def view_mhs(uid):
    data = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('view_mahasiswa.html', data = data)

@mahasiswa.route('/mahasiswa/edit/<uid>', methods=['POST', 'GET'])
@login_required
def edit_mhs(uid):
    if request.method == 'POST':
        form ={
            'nama_lengkap' : request.form['nama_lengkap'],
            'jurusan' : request.form['jurusan'],
            'email' : request.form['email'],
            'umur' : request.form['umur'],
            'status' : request.form['status'],
        }
        db.collection('mahasiswa').document(uid).update(form)
        flash('Data Berhasi Di Update', 'success')
        return redirect(url_for('mahasiswa.daftar_mahasiswa'))
    data = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('edit_mahasiswa.html', data=data)

@mahasiswa.route('/mahasiswa/delete/<uid>')
@login_required
def delete_mhs(uid):
    db.collection('mahasiswa').document(uid).delete()
    flash('Berhasil Menghapus Data', 'danger')
    return redirect(url_for('mahasiswa.daftar_mahasiswa'))
