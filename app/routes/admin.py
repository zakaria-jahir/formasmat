from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Formation, User, TrainingAction, TrainingWish
from app import db
from werkzeug.utils import secure_filename
import os
from math import radians, sin, cos, sqrt, atan2

bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès non autorisé')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return wrapper

@bp.route('/admin/formations', endpoint='admin_formations')
@login_required
@admin_required
def formations():
    formations = Formation.query.all()
    return render_template('admin/formations.html', formations=formations)

@bp.route('/admin/formation/<int:id>', methods=['GET', 'POST'], endpoint='admin_edit_formation')
@login_required
@admin_required
def edit_formation(id):
    formation = Formation.query.get_or_404(id)
    if request.method == 'POST':
        formation.iperia_code = request.form.get('iperia_code')
        formation.name = request.form.get('name')
        formation.duration = request.form.get('duration')
        formation.trainers = request.form.get('trainers')
        formation.program_link = request.form.get('program_link')
        formation.description = request.form.get('description')
        
        if 'image' in request.files:
            file = request.files['image']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join('app/static/uploads', filename))
                formation.image_path = filename
        
        db.session.commit()
        flash('Formation mise à jour')
        return redirect(url_for('admin.formations'))
    
    return render_template('admin/edit_formation.html', formation=formation)

@bp.route('/admin/formation/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_formation():
    if request.method == 'POST':
        formation = Formation(
            iperia_code=request.form.get('iperia_code'),
            name=request.form.get('name'),
            duration=request.form.get('duration'),
            trainers=request.form.get('trainers'),
            program_link=request.form.get('program_link'),
            description=request.form.get('description')
        )
        
        if 'image' in request.files:
            file = request.files['image']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join('app/static/uploads', filename))
                formation.image_path = filename
        
        db.session.add(formation)
        db.session.commit()
        flash('Nouvelle formation créée')
        return redirect(url_for('admin.formations'))
    
    return render_template('admin/new_formation.html')

@bp.route('/admin/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/admin/user/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.firstname = request.form.get('firstname')
        user.lastname = request.form.get('lastname')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.organization = request.form.get('organization')
        user.is_admin = 'is_admin' in request.form
        db.session.commit()
        flash('Utilisateur mis à jour')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', user=user)

@bp.route('/admin/training-actions')
@login_required
@admin_required
def training_actions():
    actions = TrainingAction.query.all()
    return render_template('admin/training_actions.html', actions=actions)

@bp.route('/admin/training-action/<int:id>/find-participants')
@login_required
@admin_required
def find_participants(id):
    action = TrainingAction.query.get_or_404(id)
    radius = float(request.args.get('radius', 50))  # rayon en km
    
    # Récupérer tous les souhaits pour cette formation
    wishes = TrainingWish.query.filter_by(formation_id=action.formation_id).all()
    
    # Calculer la distance pour chaque utilisateur
    potential_participants = []
    for wish in wishes:
        if wish.user.latitude and wish.user.longitude:
            # Formule de Haversine pour calculer la distance
            R = 6371  # Rayon de la Terre en km
            lat1, lon1 = radians(action.latitude), radians(action.longitude)
            lat2, lon2 = radians(wish.user.latitude), radians(wish.user.longitude)
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c
            
            if distance <= radius:
                potential_participants.append({
                    'user': wish.user,
                    'distance': round(distance, 2)
                })
    
    return render_template('admin/potential_participants.html', 
                         action=action, 
                         participants=potential_participants)
