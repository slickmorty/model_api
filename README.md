## For algotrading with metatrader 5

- Every 5 minuts
  - Get the data
  - Check if the data is new
  - If data is new
    - Get the data + some number before it
      - Clean
      - Add indicators
      - Preprocess
      - Add the last row to all the data csv
    - Feed data to the model
    - Get the Prediction
    - if the prediction is True, Do it in mt5

each of these should have loggings

