from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, Formation, TrainingWish, CompletedTraining
from app import db
from geopy.geocoders import Nominatim

bp = Blueprint('member', __name__)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.firstname = request.form.get('firstname')
        current_user.lastname = request.form.get('lastname')
        current_user.phone = request.form.get('phone')
        current_user.organization = request.form.get('organization')
        current_user.training_preference = request.form.get('training_preference')
        current_user.schedule_preference = request.form.get('schedule_preference')
        
        # Géocodage de l'adresse
        address = request.form.get('address')
        if address:
            geolocator = Nominatim(user_agent="formation_assmat")
            try:
                location = geolocator.geocode(address)
                if location:
                    current_user.latitude = location.latitude
                    current_user.longitude = location.longitude
            except:
                flash('Impossible de géocoder l\'adresse')
        
        db.session.commit()
        flash('Profil mis à jour avec succès')
        return redirect(url_for('member.profile'))
    
    return render_template('member/profile.html')

@bp.route('/training-wishes')
@login_required
def training_wishes():
    wishes = TrainingWish.query.filter_by(user_id=current_user.id).all()
    available_formations = Formation.query.all()
    return render_template('member/training_wishes.html', 
                         wishes=wishes, 
                         available_formations=available_formations)

@bp.route('/add-training-wish/<int:formation_id>')
@login_required
def add_training_wish(formation_id):
    if not TrainingWish.query.filter_by(
        user_id=current_user.id, 
        formation_id=formation_id
    ).first():
        wish = TrainingWish(user_id=current_user.id, formation_id=formation_id)
        db.session.add(wish)
        db.session.commit()
        flash('Formation ajoutée à vos souhaits')
    return redirect(url_for('member.training_wishes'))

@bp.route('/completed-trainings')
@login_required
def completed_trainings():
    completed = CompletedTraining.query.filter_by(user_id=current_user.id).all()
    return render_template('member/completed_trainings.html', completed=completed)
