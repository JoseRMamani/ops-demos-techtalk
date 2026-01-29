from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app import db
from app.models import Event, Attendance

main = Blueprint('main', __name__)

@main.route('/')
def index():
    events = Event.query.order_by(Event.name).all()
    return render_template('index.html', events=events)

@main.route('/register', methods=['POST'])
def register():
    event_id = request.form.get('event_id')
    participant_name = request.form.get('participant_name', '').strip()
    
    if not event_id or not participant_name:
        flash('Por favor complete todos los campos', 'error')
        return redirect(url_for('main.index'))
    
    attendance = Attendance(event_id=event_id, participant_name=participant_name)
    db.session.add(attendance)
    db.session.commit()
    
    flash(f'¡{participant_name} registrado exitosamente!', 'success')
    return redirect(url_for('main.index'))

@main.route('/admin')
def admin():
    events = Event.query.order_by(Event.name).all()
    attendances = Attendance.query.order_by(Attendance.registered_at.desc()).all()
    return render_template('admin.html', events=events, attendances=attendances)

@main.route('/registros')
def registros():
    event_id = request.args.get('event_id', type=int)
    events = Event.query.order_by(Event.name).all()
    
    query = Attendance.query
    if event_id:
        query = query.filter_by(event_id=event_id)
    attendances = query.order_by(Attendance.registered_at.desc()).all()
    
    return render_template('registros.html', events=events, attendances=attendances, selected_event=event_id)

@main.route('/admin/event', methods=['POST'])
def add_event():
    name = request.form.get('name', '').strip()
    if name:
        event = Event(name=name)
        db.session.add(event)
        db.session.commit()
        flash(f'Evento "{name}" creado', 'success')
    return redirect(url_for('main.admin'))

@main.route('/admin/event/<int:id>/delete', methods=['POST'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Evento eliminado', 'success')
    return redirect(url_for('main.admin'))

@main.route('/api/attendances/<int:event_id>')
def get_attendances(event_id):
    attendances = Attendance.query.filter_by(event_id=event_id).all()
    return jsonify([{
        'id': a.id,
        'participant_name': a.participant_name,
        'registered_at': a.registered_at.strftime('%Y-%m-%d %H:%M')
    } for a in attendances])
