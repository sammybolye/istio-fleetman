import tensorflow as tf
import sys
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def confirm_gpu_usage():
    """
    Checks for available GPUs using TensorFlow, logs the findings,
    and exits with a status code indicating success or failure.
    """
    logging.info("Starting GPU check...")
    try:
        # Get the list of physical devices recognized by TensorFlow
        gpus = tf.config.list_physical_devices('GPU')
        
        if gpus:
            logging.info(f"SUCCESS: Found {len(gpus)} GPU(s).")
            # Log details for each GPU found
            for i, gpu in enumerate(gpus):
                logging.info(f"  GPU [{i}]: Name={gpu.name}, Type={gpu.device_type}")
            
            # Perform a simple operation on the GPU to be certain
            logging.info("Performing a simple tensor operation on the GPU...")
            with tf.device(gpus[0].name):
                a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
                b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
                c = tf.matmul(a, b)
            logging.info(f"TensorFlow matrix multiplication result:\n{c.numpy()}")
            logging.info("GPU is confirmed to be working.")
            
            # Exit with a success code
            sys.exit(0)
        else:
            logging.error("FAILURE: No GPU devices were found by TensorFlow.")
            # Exit with an error code
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        # Exit with an error code
        sys.exit(1)

if __name__ == "__main__":
    confirm_gpu_usage()
