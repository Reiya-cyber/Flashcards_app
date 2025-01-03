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
    sort_by = request.args.get('sort_by', 'date_created')
    sort_order = request.args.get('sort_order', 'asc')

    if query:
        flashcards = Flashcard.query.filter(
            Flashcard.question.ilike(f"%{query}%") |
            Flashcard.answer.ilike(f"%{query}%") |
            Flashcard.category.ilike(f"%{query}%")
        )
    else:
        flashcards = Flashcard.query
    
    # Apply sorting
    if sort_by == 'category':
        sort_column = Flashcard.category
    elif sort_by == 'date_created':
        sort_column = Flashcard.date_created
    elif sort_by == 'question':
        sort_column = Flashcard.question

    if sort_order == 'desc':
        sort_column = sort_column.desc()
    
    flashcards = flashcards.order_by(sort_column).paginate(page=page, per_page=per_page)
    result_count = flashcards.total
    total_pages = flashcards.pages
    return render_template("home.html", user=current_user, flashcards=flashcards, query=query, result_count=result_count, total_pages=total_pages, page=page, per_page=per_page, sort_by=sort_by, sort_order=sort_order)


@views.route('/add', methods=['GET', 'POST'])
@login_required
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
@login_required
def delete_flashcard(id):
    card = Flashcard.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    flash('Flashcard deleted successfully!', category='success')
    return redirect(url_for('views.home'))


@views.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_flashcard(id):
    card = Flashcard.query.get_or_404(id)

    if card.owner_id == current_user.id:
        
        if request.method == 'POST':
            card.question = request.form.get('question')
            card.answer = request.form.get('answer')
            card.category = request.form.get('category')

            if not card.question or not card.answer:
                flash("Question and Answer fields cannot be empty", category='error')
                return redirect(url_for('views.edit_flashcard', id=id))
            
            db.session.commit()
            flash("Flashcard updated successfully!", category='success')
            return redirect(url_for('views.home'))

    return render_template('edit_flashcard.html', user=current_user, card=card)
