import os
import random

import flask
from flask import Flask, render_template, flash, redirect, session, url_for

from names import get_famous_names
from image_search import search_images

app = Flask(__name__)
app.secret_key = os.urandom(64)


def num_names_for_level(level):
    return {'easy': 10, 'normal': 50, 'hard': -1}[level]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/play/<level>')
def play(level):
    if level not in ('easy', 'normal', 'hard'):
        flash("Invalid game level!")
        return redirect(url_for('index'))

    all_names = get_famous_names()[:num_names_for_level(level)]
    random.shuffle(all_names)

    all_answers = all_names[0:4]
    person_name = all_answers[0]
    session['person_name'] = person_name
    session['level'] = level

    offered_answers = list(all_answers)
    random.shuffle(offered_answers)

    images = search_images(person_name)
    image = random.choice(images)

    random.shuffle(images)

    return render_template('play.html',
                           level=level,
                           name=person_name,
                           image_url=image.url,
                           answers=offered_answers)


@app.route('/check/<given_answer>')
def check(given_answer):
    if 'person_name' in session:
        correct_answer = session['person_name'].strip()
        level = session['level']
        is_correct = (given_answer.strip() == correct_answer.strip())

        return render_template('check.html',
                               level=level,
                               correct_answer=session['person_name'],
                               given_answer=given_answer,
                               is_correct=is_correct)
    else:
        flask.flash("No game was started.")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
