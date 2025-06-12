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
                'description': 'Large project with chat section, live section, post section, reaction sections, profile sections, connections section, and donate section. Works with authorize.net payment and WebRTC/Kurento for live streaming with custom video/voice players. Includes foreground and background notifications on Android and iOS. Non-profit project helping Afghan people help each other.',
                'image_url': '',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'mobile',
                'technologies': 'Flutter, Kotlin, Swift, WebRTC, Video',
                'status': 'Under Working',
                'year': '2022',
                'featured': True
            },
            {
                'title': 'Restaurant Applications (Dulces Antojitos Food Delivery)',
                'description': 'Three applications for online food delivery: customer app, admin panel for managing customers/orders/foods/feedback/income, and driver app for order pickup and delivery. Includes customer management, order management, content management, report management, and foods management.',
                'image_url': '',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'mobile',
                'technologies': 'RESTful APIs, Android, Flutter, WebRTC, Kotlin',
                'status': 'Deployed',
                'year': '2021',
                'featured': True
            },
            {
                'title': 'ShiftNext',
                'description': 'Large project with Angular features, signin/signup with AWS Cognito, three view types (Timeline, Grid, Staff). Uses Socket.io for real-time data and RESTful APIs. Implements SSO login/signup, backend with Node.js/Express, file upload to S3, and Google Maps for location picking.',
                'image_url': '',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'web',
                'technologies': 'AngularJS, Express.js, Socket.io, Node.js, AWS, Angular, REST APIs, JavaScript, Angular 2+',
                'status': 'Delivered',
                'year': '2022',
                'featured': True
            },
            {
                'title': 'Herat Exchanger',
                'description': 'Real-time currency exchange rates for Herat Money Changers Union. Features momentary and daily rate changes, blog, info sections, and rate changer tools. Includes website with union news and WordPress API with custom field plugin. Published on Play Store and App Store.',
                'image_url': '',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'mobile',
                'technologies': 'WordPress, Flutter, PHP',
                'status': 'Published',
                'year': '2020',
                'featured': False
            },
            {
                'title': 'Badam Real Estate',
                'description': 'First product for own company allowing users to buy, sell, and rent properties in Afghanistan. Features verified listings in Kabul, Herat, Mazar, and other major cities. Search by location, property type, area, and price range. Includes website and REST API development. Published on Google Play Store.',
                'image_url': '',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'mobile',
                'technologies': 'Flutter, Android, Kotlin, Socket.io',
                'status': 'Delivered',
                'year': '2019',
                'featured': False
            },
            {
                'title': 'Next Level Skin',
                'description': 'Shopify WooCommerce project with custom theme and Storefront API for mobile application. Features product lists, product reviews, branding and advertising, with daily skin care changes.',
                'image_url': '',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'web',
                'technologies': 'Shopify, Frontend Store API, Flutter',
                'status': 'Under Working',
                'year': '2022',
                'featured': False
            },
            {
                'title': 'Driver App and Passenger App',
                'description': 'Applications focused on customizing FCM and setting up Google Maps with custom markers, circles, and live tracking functionality.',
                'image_url': '',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'mobile',
                'technologies': 'Android, Kotlin',
                'status': 'Incomplete',
                'year': '2020',
                'featured': False
            },
            {
                'title': 'AutoComplete Library',
                'description': 'Open source project helping developers implement async autocomplete with scrolling, listing, and data fetching in Flutter applications across all device types.',
                'image_url': '',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'opensource',
                'technologies': 'Flutter, Dart',
                'status': 'Published',
                'year': '2022',
                'featured': False
            },
            {
                'title': 'Dictionary For Desktop Library',
                'description': 'Open source desktop application for Windows users in the Afghanistan community. Supports 3 languages (Dari, Pashto, English), favorites, theme changes, and search history logging.',
                'image_url': '',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'opensource',
                'technologies': 'Flutter, Dart',
                'status': 'Published',
                'year': '2022',
                'featured': False
            },
            {
                'title': 'Clean Architecture for Android with Jetpack Compose',
                'description': 'Open source project for new developers to quickly set up their environment and understand MVVM pattern setup with Jetpack Compose.',
                'image_url': '',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'opensource',
                'technologies': 'Android, Kotlin, Jetpack Compose',
                'status': 'Uploaded',
                'year': '2021',
                'featured': False
            },
            {
                'title': 'Kurento One to Many Call Example for Node.js',
                'description': 'Open source project for new developers to quickly set up their environment and understand how Kurento one-to-many works and how to save live streams in WebRTC media server.',
                'image_url': '',
                'project_url': '#',
                'github_url': 'https://github.com/rahmanrezaee',
                'category': 'opensource',
                'technologies': 'Node.js',
                'status': 'Uploaded',
                'year': '2021',
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
