# Interview Prep

## Overview

**Interview Prep** is a web application designed to help users prepare for interviews by generating customized interview questions based on their resume. The app also provides feedback on their responses to help them improve.

## Features

- **Resume Upload:** Users can upload their resumes in PDF format.
- **Interview Question Generation:** Based on the content of the resume, the app generates personalized interview questions.
- **Response Feedback:** After the user responds to the questions, the app provides detailed feedback to help them refine their answers.
- **User-Friendly Interface:** A simple and intuitive interface for a seamless user experience.

## How It Works

1. **Upload Resume:** The user uploads their resume.
2. **Question Generation:** The app analyzes the resume and generates a set of interview questions tailored to the user's experience and skills.
3. **Answer Submission:** The user answers the questions.
4. **Receive Feedback:** The app reviews the responses and provides constructive feedback.

## Installation

1. Clone the Repo
2. pip install -r requirements.txt
3. Create a file '.env' and fill in the huggingface api key. Refer '.env.example'
4. run using 'fastapi dev main.py'
