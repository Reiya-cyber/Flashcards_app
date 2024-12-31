from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, logout_user, current_user
from .models import Flashcard
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    flashcards = Flashcard.query.all()
    return render_template("home.html", user=current_user, flashcards=flashcards)

@views.route('/add', methods=['GET', 'POST'])
def add_flashcard():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        category = request.form.get('category')

        if not question or not answer:
            flash('Question and Answer fields cannot be empty.', category='error')
            return redirect(url_for('views.add_flashcard'))
        
        new_card = Flashcard(question=question, answer=answer, category=category, owner_id=current_user.id)
        db.session.add(new_card)
        db.session.commit()
        flash('Flashcard added succeddfully!')
        return redirect(url_for('views.home'))
    return render_template("flashcard.html", user=current_user)

@views.route('/delete/<int:id>')
def delete_flashcard(id):
    card = Flashcard.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    flash('Flashcard deleted successfully!', category='success')
    return redirect(url_for('views.home'))