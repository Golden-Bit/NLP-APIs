from fastapi import FastAPI
from chains.experiments.script_1 import router as script1_router
from chains.experiments.script_2 import router as script2_router
from chains.experiments.script_3 import router as script3_router

app = FastAPI()

app.include_router(script1_router, prefix="/script1", tags=["script1"])
app.include_router(script2_router, prefix="/script2", tags=["script2"])
app.include_router(script3_router, prefix="/script3", tags=["script3"])

# To run the application
# Save the above code in a file named main.py and run the following command in your terminal:
# uvicorn main:app --reload


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8110)

