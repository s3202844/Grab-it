### not work
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path='./model.tflite')

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

print(height, width)


