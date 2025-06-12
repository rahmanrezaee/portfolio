from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Message
from app import app, db, mail
from models import Contact, Project
import logging

@app.route('/')
def index():
    """Single page application with all sections"""
    featured_projects = Project.query.filter_by(featured=True).limit(3).all()
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    
    # Get unique categories for filter buttons
    categories = db.session.query(Project.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('single_page.html', 
                         featured_projects=featured_projects,
                         all_projects=all_projects, 
                         categories=categories)

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()
    
    # Validation
    if not all([name, email, subject, message]):
        flash('All fields are required.', 'danger')
        return redirect('/#contact')
    
    if '@' not in email or '.' not in email:
        flash('Please enter a valid email address.', 'danger')
        return redirect('/#contact')
    
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
        return redirect('/#contact')
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Database error in contact form: {str(e)}")
        flash('There was an error sending your message. Please try again.', 'danger')
        return redirect('/#contact')

@app.route('/resume')
def resume():
    """Redirect to resume download"""
    return redirect('/static/resume/sample_resume.pdf')

# Initialize some sample projects if none exist
def create_sample_projects():
    """Create sample projects if database is empty"""
    if Project.query.count() == 0:
        sample_projects = [
            {
                'title': 'Dist ba Dist',
                'description': 'Large social platform with chat section, live streaming, post section, reactions, profiles, connections, and donations. Built with WebRTC and Kurento for live streaming, custom video/voice players, and real-time notifications.',
                'image_url': 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=600&fit=crop',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'mobile',
                'technologies': 'Flutter, Kotlin, Swift, WebRTC, Video',
                'featured': True
            },
            {
                'title': 'Restaurant Food Delivery App',
                'description': 'Complete food delivery system with three applications: customer app, restaurant management, and driver delivery app. Includes order management, GPS tracking, and payment integration.',
                'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=600&fit=crop',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'mobile',
                'technologies': 'Flutter, Android, Kotlin, RESTful APIs, WebRTC',
                'featured': True
            },
            {
                'title': 'ShiftNext',
                'description': 'Large project with Angular features, AWS Cognito authentication, timeline/grid/staff views, Socket.io for real-time data, and RESTful APIs. Includes SSO login, file upload to S3, and Google Maps integration.',
                'image_url': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'web',
                'technologies': 'Angular, Node.js, Express.js, Socket.io, AWS, REST APIs',
                'featured': True
            },
            {
                'title': 'Herat Exchanger',
                'description': 'Real-time currency exchange rate application for Herat Money Changers Union. Features momentary and daily rate changes, blog section, info pages, and rate changer tools. Published on both Play Store and App Store.',
                'image_url': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=600&fit=crop',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'mobile',
                'technologies': 'Flutter, WordPress, PHP, Custom API',
                'featured': False
            },
            {
                'title': 'Badam Real Estate',
                'description': 'Real estate application for buying, selling, and renting properties in Afghanistan. Features verified listings in Kabul, Herat, Mazar with search by location, property type, area, and price range.',
                'image_url': 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&h=600&fit=crop',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'mobile',
                'technologies': 'Flutter, Android, Kotlin, Socket.io, REST API',
                'featured': False
            },
            {
                'title': 'Next Level Skin',
                'description': 'Shopify WooCommerce project with custom theme and Storefront API for mobile application. Features product listings, reviews, branding and advertising, with daily skin care changes.',
                'image_url': 'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=800&h=600&fit=crop',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'web',
                'technologies': 'Shopify, Frontend Store API, Flutter',
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
