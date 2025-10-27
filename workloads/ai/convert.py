import joblib
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

model = joblib.load("sound_classifier.pkl")
initial_type = [('float_input', FloatTensorType([None, 1024]))]  # adjust feature length
onnx_model = convert_sklearn(model, initial_types=initial_type)
with open("sound_classifier.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())