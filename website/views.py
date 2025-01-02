from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, logout_user, current_user
from .models import Flashcard
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    if query:
        flashcards = Flashcard.query.filter(
            Flashcard.question.ilike(f"%{query}%") |
            Flashcard.answer.ilike(f"%{query}%") |
            Flashcard.category.ilike(f"%{query}%")
        ).paginate(page=page, per_page=per_page)
    else:
        flashcards = Flashcard.query.paginate(page=page, per_page=per_page)
    result_count = flashcards.total
    total_pages = flashcards.pages
    return render_template("home.html", user=current_user, flashcards=flashcards, query=query, result_count=result_count, total_pages=total_pages, page=page, per_page=per_page)

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