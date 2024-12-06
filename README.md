# VERSO: Poetry & Artwork AI Generation System
 King AbdulAziz Universality - Graduation Project

## Overview
VERSO is an innovative web-based platform that combines Artificial Intelligence with the rich tradition of Arabic poetry. Designed to both preserve and redefine the experience of Arabic literature, VERSO generates poetry that adheres to the traditional Arabic metrics (Al-Arood and Al-Bihar) and transforms these poetic compositions into bespoke visual art. The project was developed as part of the CPCS-498 course at King Abdulaziz University.

---

## Features
- **AI-Powered Arabic Poetry Generation**: Generate poetry based on user prompts with strict adherence to Arabic poetic metrics.
- **Prosody Analysis**: Analyze poems to ensure they follow traditional poetic structures.
- **Visual Representations**: Create unique artistic representations of poems through text-to-image AI.
- **Optional Audiovisual Recitations**: Leverage deepfake technology to provide personalized recitations of generated poems.

---

## Tech Stack
- **Frontend**: Vue.js
- **Backend**: Django
- **AI Models**: Hugging Face (Transformer-based models)
- **Data Collection**: Selenium, Pandas
- **Visualization**: Generative Adversarial Networks (GANs)
- **Hosting**: ngrok (for testing)

---

## Installation

### Clone the Repository
```bash
git clone https://github.com/your-repo/verso.git
cd verso
Install Dependencies
Python Backend
bash
Copy code
pip install -r requirements.txt
Vue.js Frontend
bash
Copy code
npm install
Setup Environment
Create a .env file in both the backend and frontend directories.
Add the following environment variables:
bash
Copy code
DJANGO_SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
Usage
Start the Backend
bash
Copy code
python manage.py runserver
Start the Frontend
bash
Copy code
npm run serve
Access the Application
Visit the following URL in your browser:

text
Copy code
http://localhost:8080
Testing
Backend Testing
Run unit tests for the backend:

bash
Copy code
python manage.py test
Frontend Testing
Run unit tests for the frontend:

bash
Copy code
npm run test
Architecture
Backend Server: Handles poetry generation, prosody analysis, and data processing.
Frontend Interface: Provides an intuitive user interface for seamless interaction.
Database: Stores poetry data, user-generated content, and visual artworks.
Design
Functional Requirements
Generate Arabic poetry based on user input.
Analyze poetry for adherence to traditional poetic structures.
Transform poetry into artistic visuals.
Provide optional audiovisual recitations.
Non-Functional Requirements
Performance: Support up to 1000 concurrent users with a response time of less than 3 seconds.
Security: Implement secure user authentication and data encryption.
Usability: Provide an intuitive interface with English and Arabic language support.
Reliability: Achieve 99.5% uptime, excluding scheduled maintenance.
Challenges and Solutions
Challenges
Quantization Impact on Model Quality:

Loss of precision with 4-bit quantization for SILMA-9B.
Limited computational resources for training.
Dataset Challenges:

Inconsistent data from sources like Diwan.net.
Limited availability of high-quality, labeled datasets.
Integration Issues:

Compatibility issues between tools like Hugging Face, QLoRA, and Django.
Solutions
Used 8-bit quantization as an alternative for better precision.
Developed preprocessing scripts for cleaning and aligning poetry data.
Leveraged modular architecture for smooth integration between components.
Future Enhancements
Expand support for other languages and poetic forms.
Add collaborative poetry creation features.
Integrate 3D holographic representations for immersive experiences.
Contributors
Thamer S. Almalki
Mahmoud Alardawi
Rawad Algamidi
Supervised by Dr. Mohammed Dahab

License
This project is licensed under the MIT License. See the LICENSE file for more information.

References
DeepLearning.AI - Natural Language Processing
GitHub - How AI Code Generation Works
GeeksforGeeks - LSTM-Based Poetry Generation
OpenAI - Text Generation
Deepfake Web Guide
TechTarget - Deepfake Overview
