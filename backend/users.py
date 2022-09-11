from flask import Blueprint, flash, render_template, url_for, redirect, jsonify, request
from backend.auth import login_required
from backend.db import db, get_all_collection
from werkzeug.security import generate_password_hash

usersapp = Blueprint('usersapp', __name__)

# Read All
@usersapp.route('/users')
@login_required
def users():
    users = get_all_collection('users')
    return render_template('users/users.html', users=users)

# create
@usersapp.route('/users/tambah', methods=['POST', 'GET'])
@login_required
def create_users():
    if request.method == 'POST':
        # Cek kesamaan password
        if request.form['password'] != request.form['password_1']:
            flash('Password Tidak sama', 'danger')
            return redirect(url_for('.create_users'))
        
        #Memanggil database
        cek_username = db.collection('users').where('username', '==', request.form['username']).stream()
        username = {}
        
        #Perulangan database
        for p in cek_username:
            user = p.to_dict()
            username = user

        #Pengecekan username
        if username:
            flash('Username Sudah Ada', 'danger')
            return redirect(url_for('.create_users'))
        else:
            data = {
                'nama_lengkap' : request.form['nama_lengkap'],
                'username' : request.form['username'],
                'email' : request.form['email'],
            }

            data['password'] = generate_password_hash(request.form['password'], 'sha256')
            db.collection('users').document().set(data)
            flash('Berhasil Menambahkan User', 'success')
            return redirect(url_for('.users'))
    return render_template('users/create_users.html')

# Update
@usersapp.route('/users/edit/<uid>', methods=['POST', 'GET'])
@login_required
def update_users(uid):
    if request.method == 'POST':
        form = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'email' : request.form['email'],
        }
        db.collection('users').document(uid).update(form)
        flash('Berhasil Mengubah Data', 'success')
        return redirect(url_for('.users'))
    data = db.collection('users').document(uid).get().to_dict()
    return render_template('users/edit_users.html', data=data)

# Delete
@usersapp.route('/users/hapus/<uid>')
@login_required
def delete_users(uid):
    db.collection('users').document(uid).delete()
    flash('Berhasil Menghapus Data', 'success')
    return redirect(url_for('.users'))

# Read
@usersapp.route('/users/lihat/<uid>')
@login_required
def view_users(uid):
    data = db.collection('users').document(uid).get().to_dict()
    return render_template('users/view_users.html', data=data)