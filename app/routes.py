import os
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
import pandas as pd
from app.analysis import perform_basic_analysis, get_ai_insights
from app.models import User, db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # The dashboard is now simple, no user plan data is needed.
    return render_template('dashboard.html')

@main_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    # No more access checks needed! Every logged-in user can upload.
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return jsonify({'error': 'Unsupported file type. Please use CSV or Excel.'}), 400

        chart_data = perform_basic_analysis(df)
        if "error" in chart_data:
             return jsonify(chart_data), 400

        ai_insights = get_ai_insights(df.head().to_string())
        
        return jsonify({
            'chart_data': chart_data,
            'ai_insights': ai_insights
        })
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@main_bp.route('/admin')
@login_required
def admin():
    # Admin check remains the same
    if current_user.email != os.environ.get('ADMIN_EMAIL'):
        flash('You are not authorized to view this page.')
        return redirect(url_for('main.dashboard'))
    
    total_users = User.query.count()
    users = User.query.order_by(User.created_at.desc()).all()
    
    # We no longer need to count premium users
    return render_template('admin.html', total_users=total_users, users=users)