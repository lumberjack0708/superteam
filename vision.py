from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os
def vision():
    # Get path to images folder
    dirname = os.path.dirname(__file__)
    images_folder = os.path.join(dirname, 'image/Test')
    # Create variables for your project
    publish_iteration_name = "Iteration3"
    project_id = "37b0d5fe-396f-4443-a10a-b619ef49152a"
    # Create variables for your prediction resource
    prediction_key = "GBdJ5akyp6d6yBZzG6KDgVet3xVIvUArBdVn1bh2Z3X4rBiAqLqBJQQJ99AKACi0881XJ3w3AAAIACOGWM0B"
    endpoint = "https://weather33655-prediction.cognitiveservices.azure.com/"
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)
    # Open an image and make a prediction
    with open(os.path.join(images_folder, "test.jpg"), "rb") as image_contents:
        results = predictor.classify_image(project_id, publish_iteration_name, image_contents.read())
    # Display the results
    for prediction in results.predictions:
        print(f"{prediction.tag_name}: {prediction.probability * 100 :.2f}%")
    pred = max(results.predictions, key=lambda x: x.probability)
    return f"最有可能的天氣為: {pred.tag_name}: {pred.probability * 100 :.2f}%"

classify = vision()
print(classify)