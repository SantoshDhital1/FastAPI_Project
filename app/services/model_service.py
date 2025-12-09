import joblib
import pandas as pd
from app.core.config import settings
from app.cache.redis_cache import set_cached_prediction, get_cached_prediction

try:
    model = joblib.load(settings.MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model from {settings.MODEL_PATH}: {str(e)}") from e

def predict_car_price(data: dict):
    cache_key = " ".join([str(val) for val in data.values()])
    cached = get_cached_prediction(cache_key)
    if cached is not None:
        return cached
    
    try:
        input_data = pd.DataFrame([data])
        prediction = model.predict(input_data)[0]
        set_cached_prediction(cache_key, prediction)
        return prediction
    except AttributeError as e:
        if '_name_to_fitted_passthrough' in str(e):
            raise RuntimeError(
                "Model compatibility error: The model was trained with an older version of scikit-learn. "
                "Please retrain the model using the current scikit-learn version (1.3.2). "
                "Run: python training/train_model.py"
            ) from e
        raise
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}") from e