import os 
import sys
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from uvicorn import run as app_run
from fastapi.responses import Response, JSONResponse, FileResponse
from starlette.responses import RedirectResponse
import pandas as pd

from etl_project.utils.main_utils.utils import load_object
from etl_project.utils.ml_utils.model.estimator import ETLModel
from etl_project.pipeline.training_pipeline import TrainingPipeline
from etl_project.exception.exception import ETLPipelineException
from etl_project.logging.logger import logging
from etl_project.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME
from dotenv import load_dotenv
import certifi
import pymongo

ca = certifi.where()
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

client = pymongo.MongoClient(MONGO_DB_URI, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="templates"), name="static")

@app.get("/", tags=["authentication"])
async def index():
    return FileResponse("templates/index.html")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise ETLPipelineException(e,sys)
    
@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        logging.info(f"Received file: {file.filename}")
        
        # Check if file is CSV
        if not file.filename.endswith('.csv'):
            return JSONResponse({
                "status": "error",
                "message": "Please upload a CSV file"
            }, status_code=400)
        
        # Check if model files exist
        if not os.path.exists("final_model/preprocessor.pkl"):
            return JSONResponse({
                "status": "error",
                "message": "Preprocessor model not found. Please train the model first."
            }, status_code=404)
            
        if not os.path.exists("final_model/model.pkl"):
            return JSONResponse({
                "status": "error",
                "message": "Trained model not found. Please train the model first."
            }, status_code=404)
        
        # Read and validate CSV file
        try:
            df = pd.read_csv(file.file)
            logging.info(f"CSV loaded successfully. Shape: {df.shape}")
            logging.info(f"Columns: {list(df.columns)}")
        except Exception as csv_error:
            logging.error(f"Error reading CSV: {str(csv_error)}")
            return JSONResponse({
                "status": "error",
                "message": f"Error reading CSV file: {str(csv_error)}"
            }, status_code=400)
        
        # Check if dataframe is empty
        if df.empty:
            return JSONResponse({
                "status": "error",
                "message": "The uploaded CSV file is empty"
            }, status_code=400)
        
        # Load models
        try:
            preprocessor = load_object("final_model/preprocessor.pkl")
            final_model = load_object("final_model/model.pkl")
            logging.info("Models loaded successfully")
        except Exception as model_error:
            logging.error(f"Error loading models: {str(model_error)}")
            return JSONResponse({
                "status": "error",
                "message": f"Error loading models: {str(model_error)}"
            }, status_code=500)
        
        # Create ETL model and make predictions
        try:
            network_model = ETLModel(preprocessor=preprocessor, model=final_model)
            y_pred = network_model.predict(df)
            logging.info(f"Predictions made successfully. Predictions shape: {len(y_pred)}")
        except Exception as pred_error:
            logging.error(f"Error making predictions: {str(pred_error)}")
            return JSONResponse({
                "status": "error",
                "message": f"Error making predictions: {str(pred_error)}"
            }, status_code=500)
        
        # Add predictions to dataframe
        df['predicted_column'] = y_pred
        
        # Create prediction_output directory if it doesn't exist
        os.makedirs('prediction_output', exist_ok=True)
        df.to_csv('prediction_output/output.csv', index=False)
        
        # Convert to records for JSON response
        try:
            predictions_records = df.to_dict('records')
            logging.info("Data converted to JSON format successfully")
        except Exception as json_error:
            logging.error(f"Error converting to JSON: {str(json_error)}")
            return JSONResponse({
                "status": "error",
                "message": f"Error converting results to JSON: {str(json_error)}"
            }, status_code=500)
        
        # Return JSON response with prediction results
        return JSONResponse({
            "status": "success",
            "message": "Prediction completed successfully",
            "predictions": predictions_records,
            "total_records": len(df)
        })
        
    except Exception as e:
        logging.error(f"Unexpected error in predict_route: {str(e)}", exc_info=True)
        return JSONResponse({
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }, status_code=500)



if __name__=="__main__":
    app_run(app, host="0.0.0.0", port=8000)
