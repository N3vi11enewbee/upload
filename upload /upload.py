from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import pandas as pd
from io import StringIO
import os


# Initialize FastAPI application
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

@app.post("/process")
async def process_data_and_question(
    file: UploadFile = File(...),
    question: str = Form(...)
):
    try:
        # Read the uploaded file
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        data = df.to_string(index=False)
        
        # Query OpenAI with the data and question
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"The following data is provided: {data}. {question}"}
            ],
            max_tokens=150
        )
        
        return {"data": data, "response": response['choices'][0]['message']['content']}
    
    except Exception as e:
        print("Error processing request:", e)
        raise HTTPException(status_code=500, detail="Error processing request")

def read_root():
    return {"Hello": "World"}

# Function to start the FastAPI server
def start_fastapi():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    import threading
    import time

    # Start the FastAPI server in a separate thread
    fastapi_thread = threading.Thread(target=start_fastapi)
    fastapi_thread.start()

    # Wait a moment to ensure the server is up
    time.sleep(2)