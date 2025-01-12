# VERSO: Poetry & Artwork AI Generation System
 King AbdulAziz Universality - Graduation Project

## Overview
VERSO is an innovative web-based platform that combines Artificial Intelligence with the rich tradition of Arabic poetry. Designed to both preserve and redefine the experience of Arabic literature, VERSO generates poetry that adheres to the traditional Arabic metrics (Al-Arood and Al-Bihar) and transforms these poetic compositions into bespoke visual art. The project was developed as the Graduation Project at King Abdulaziz University.

---

## Features
- **AI-Powered Arabic Poetry Generation**: Generate poetry based on user prompts with strict adherence to Arabic poetic metrics.
- **Prosody Analysis**: Analyze poems to ensure they follow traditional poetic structures.
- **Visual Representations**: Create unique artistic representations of poems through text-to-image AI.

---

## Platform Demonstration
A video showcasing the platform's functionality and features is available. Watch the video here:
[VERSO Platform Demonstration](https://drive.google.com/drive/folders/1inscodaQr3BnO2pMziO6ZPm79E7PBIMS?usp=sharing)

---

## Dataset
The project utilizes a custom Arabic poetry dataset for training and analysis. The dataset was compiled from a variety of sources and is carefully annotated for poetic structure and meter. You can find the dataset and related files here:
[VERSO Dataset and Resources](https://drive.google.com/drive/folders/1inscodaQr3BnO2pMziO6ZPm79E7PBIMS?usp=sharing)

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
```

---

## Install Dependencies

### Python Backend
```bash
pip install -r requirements.txt
```

### Vue.js Frontend
```bash
npm install
```

---

## Setup Environment
Create a .env file in both the backend and frontend directories.
Add the following environment variables
```bash
DJANGO_SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

---

## Usage

### Start the Backend
```bash
python manage.py runserver
```

### Start the Frontend
```bash
npm run serve
```

### Access the Application
Visit the following URL in your browser:
```bash
[python manage.py runserver
](http://localhost:8080)
```

---

## Testing

### Backend Testing
Run unit tests for the backend:
```bash
python manage.py test
```

### Frontend Testing
Run unit tests for the frontend:
```bash
npm run test
```

---

## Challenges and Solutions

### Challenges
1. Quantization Impact on Model Quality:
 - Loss of precision with 4-bit quantization for SILMA-9B.
 - Limited computational resources for training.


2. Dataset Challenges:
 - Inconsistent data from sources like Diwan.net.
 - Limited availability of high-quality, labeled datasets.

   
3. Integration Issues:
 - Compatibility issues between tools like Hugging Face, QLoRA, and Django.

### Solutions
- Used 8-bit quantization as an alternative for better precision.
- Developed preprocessing scripts for cleaning and aligning poetry data.
- Leveraged modular architecture for smooth integration between components.

---

## Contributors
- Mahmued A. Alardawi
- Thamer S. Almalki
- Rawad Algamidi
  
Supervised by **Dr. Mohammed Dahab**
Linguistic and prosody consultant: **Dr. Rania Alardawe**

---

## License
This project is licensed under the MIT License. See the LICENSE file for more information.


Thank you for exploring VERSO!

### Additions:
1. **Platform Demonstration** [VERSO Platform Demonstration](https://drive.google.com/drive/folders/1inscodaQr3BnO2pMziO6ZPm79E7PBIMS?usp=sharing)
2. **Dataset** [VERSO Dataset and Resources](https://drive.google.com/drive/folders/1inscodaQr3BnO2pMziO6ZPm79E7PBIMS?usp=sharing)












