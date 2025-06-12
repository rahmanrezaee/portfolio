from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Message
from app import app, db, mail
from models import Contact, Project
import logging

@app.route('/')
def index():
    """Homepage with hero section and featured projects"""
    featured_projects = Project.query.filter_by(featured=True).limit(3).all()
    return render_template('index.html', featured_projects=featured_projects)

@app.route('/about')
def about():
    """About page with skills and experience"""
    return render_template('about.html')

@app.route('/portfolio')
def portfolio():
    """Portfolio page with all projects"""
    category = request.args.get('category', 'all')
    
    if category == 'all':
        projects = Project.query.order_by(Project.created_at.desc()).all()
    else:
        projects = Project.query.filter_by(category=category).order_by(Project.created_at.desc()).all()
    
    # Get unique categories for filter buttons
    categories = db.session.query(Project.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('portfolio.html', projects=projects, categories=categories, current_category=category)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validation
        if not all([name, email, subject, message]):
            flash('All fields are required.', 'danger')
            return render_template('contact.html')
        
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address.', 'danger')
            return render_template('contact.html')
        
        try:
            # Save to database
            contact_entry = Contact(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            db.session.add(contact_entry)
            db.session.commit()
            
            # Send email notification
            try:
                msg = Message(
                    subject=f'Portfolio Contact: {subject}',
                    recipients=[app.config['MAIL_DEFAULT_SENDER']],
                    reply_to=email
                )
                msg.body = f"""
New contact form submission:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
                """
                mail.send(msg)
                logging.info(f"Contact email sent successfully for {name}")
            except Exception as e:
                logging.error(f"Failed to send contact email: {str(e)}")
                # Don't fail the form submission if email fails
            
            flash('Thank you for your message! I\'ll get back to you soon.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Database error in contact form: {str(e)}")
            flash('There was an error sending your message. Please try again.', 'danger')
    
    return render_template('contact.html')

@app.route('/resume')
def resume():
    """Redirect to resume download"""
    return redirect('/static/resume/sample_resume.pdf')

# Initialize some sample projects if none exist
@app.before_first_request
def create_sample_projects():
    """Create sample projects if database is empty"""
    if Project.query.count() == 0:
        sample_projects = [
            {
                'title': 'E-Commerce Platform',
                'description': 'A full-stack e-commerce platform built with modern web technologies. Features include user authentication, payment processing, inventory management, and responsive design.',
                'image_url': 'https://pixabay.com/get/ga8dd8a5dcee01018cd4fee205b933378da208ea49ac049159404e17fc133701989cd98f18c09bedf1caa4357d7cb3daa4869a97ac3a608038cf448766c082e69_1280.jpg',
                'project_url': '#',
                'github_url': '#',
                'category': 'web',
                'technologies': 'Flask, Python, JavaScript, Bootstrap, SQLAlchemy',
                'featured': True
            },
            {
                'title': 'Mobile Task Manager',
                'description': 'A cross-platform mobile application for task management with real-time synchronization, offline support, and intuitive user interface.',
                'image_url': 'https://pixabay.com/get/gf14971deb5f58d4e28cbdedf8577f44059feb9fff243ad84f8089bfcf32d7d592d6a75d8fbd917a240f183367406e19634e92c32a5eae04adce7a842c0409fa5_1280.jpg',
                'project_url': '#',
                'github_url': '#',
                'category': 'mobile',
                'technologies': 'React Native, Node.js, MongoDB, Firebase',
                'featured': True
            },
            {
                'title': 'Data Analytics Dashboard',
                'description': 'An interactive dashboard for data visualization and analytics with real-time updates, custom charts, and export functionality.',
                'image_url': 'https://pixabay.com/get/g6cf4b2084dffdff1dc48e7e3a84116cbf75d015f8fc121c58150d1cbf1a4214c51d063e80712440fc1a8425ac20f7944070f60df62ca309e053f9ab98701e745_1280.jpg',
                'project_url': '#',
                'github_url': '#',
                'category': 'data',
                'technologies': 'Python, D3.js, Flask, PostgreSQL, Chart.js',
                'featured': True
            },
            {
                'title': 'API Gateway Service',
                'description': 'A microservices API gateway with authentication, rate limiting, load balancing, and comprehensive logging.',
                'image_url': 'https://pixabay.com/get/g073a1468392698f1a0880e18fb238a2eb4be917533a1b1ed25eae4fad968aefe7e9876a343119a833d4af304f3ea302cb19c8c409864f1ecb6099e513c727a8a_1280.jpg',
                'project_url': '#',
                'github_url': '#',
                'category': 'backend',
                'technologies': 'Node.js, Express, Redis, Docker, AWS',
                'featured': False
            }
        ]
        
        for project_data in sample_projects:
            project = Project(**project_data)
            db.session.add(project)
        
        try:
            db.session.commit()
            logging.info("Sample projects created successfully")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating sample projects: {str(e)}")
