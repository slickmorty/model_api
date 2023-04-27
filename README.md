## Trade helper data server

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
    - Send the prediction to a remote database
each of these should have loggings

# The predictions will be shown in the users device