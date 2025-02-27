
# Traffic Management System  

Welcome to the Traffic Management System repository! This project aims to develop an integrated approach for urban traffic management and real-time transit information dissemination using IoT technology. Our goal is to enhance traffic efficiency, reduce congestion, and provide commuters with real-time information for a smoother travel experience.  

## Project Overview  

The primary objectives of this project include:  

- IoT Sensor Deployment: Implementing sensors to monitor traffic flow, environmental conditions, and public transit status.  
- Real-Time Data Processing: Analyzing collected data to optimize traffic signals and manage incidents promptly.  
- User Engagement: Providing commuters with up-to-date transit information through digital displays and mobile applications.  

## Features  

- Traffic Flow Monitoring: Real-time analysis of vehicle speed, count, and direction.  
- Environmental Monitoring: Tracking air quality, weather conditions, and noise levels.  
- Public Transit Updates: Live updates on bus and train schedules, delays, and arrivals.  
- Incident Management: Immediate detection and reporting of traffic incidents to relevant authorities.  

## Tech Stack  

- Programming Languages: Python 3.8, HTML5, CSS3  
- Frameworks: Flask 1.1.2  
- Database: SQLite 3  
- Deployment: Heroku  

## Getting Started  

Follow these steps to set up the project locally:  

1. Clone the repository:  
   ```  
   git clone https://github.com/ashenbandara02/trafficmanagementsystem.git  
   cd trafficmanagementsystem  
   ```  

2. Set up a virtual environment:  
   ```  
   python3 -m venv venv  
   source venv/bin/activate  (On Windows, use `venv\Scripts\activate`)  
   ```  

3. Install dependencies:  
   ```  
   pip install -r requirements.txt  
   ```  

4. Run the application:  
   ```  
   python app.py  
   ```  
   The application should now be running on http://127.0.0.1:5000/  

## Project Structure  

trafficmanagementsystem/  
├── static/  
│   ├── css/  
│   └── js/  
├── templates/  
│   ├── index.html  
│   └── dashboard.html  
├── app.py  
├── requirements.txt  
└── README.md  

- `static/`: Contains static files like CSS and JavaScript.  
- `templates/`: HTML templates for the web pages.  
- `app.py`: Main application script.  
- `requirements.txt`: List of Python dependencies.  

## Contributing  

We welcome contributions to enhance the project! To contribute:  

1. Fork the repository.  
2. Create a new branch: `git checkout -b feature/your-feature-name`.  
3. Commit your changes: `git commit -m 'Add some feature'`.  
4. Push to the branch: `git push origin feature/your-feature-name`.  
5. Open a pull request.  

Please ensure your code adheres to our coding standards and includes relevant tests.  

## License  

This project is licensed under the MIT License. See the LICENSE file for more details.  

## Contact  

For questions or support, please contact me at bandaraashen02@gmail.com.  
