from tensorflow import keras
from tensorflow import metrics
from data import DataProcessing


def compile_and_fit(model, input_window, output_window):

    MAX_EPOCHS = 3

    # model.compile(loss='binary_crossentropy',
    #                 optimizer='adam',
    #                 metrics=[metrics.BinaryAccuracy()])

    history = model.fit(
        x=input_window,
        y=output_window,
        batch_size=24,
        shuffle=True,
        epochs=MAX_EPOCHS,
        verbose=2,
    )

    return history
