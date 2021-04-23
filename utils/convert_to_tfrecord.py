import tensorflow as tf
import numpy as np
import csv

def _bytes_feature(value):
  """Returns a bytes_list from a string / byte."""
  if isinstance(value, type(tf.constant(0))):
    value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
  """Returns a float_list from a float / double."""
  return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def _int64_feature(value):
  """Returns an int64_list from a bool / enum / int / uint."""
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

"""
structure reference from IMDB

features {
  feature {
    key: "label"
    value {
      int64_list {
        value: 0
      }
    }
  }
  feature {
    key: "text"
    value {
      bytes_list {
        value: "This was an absolutely terrible movie. Don\'t be lured in by Christopher Walken or Michael Ironside. Both are great actors, but this must simply be their worst role in history. Even their great acting could not redeem this movie\'s ridiculous storyline. This movie is an early nineties US propaganda piece. The most pathetic scenes were those when the Columbian rebels were making their cases for revolutions. Maria Conchita Alonso appeared phony, and her pseudo-love affair with Walken was nothing but a pathetic emotional plug in a movie that was devoid of any real meaning. I am disappointed that there are movies like this, ruining actor\'s like Christopher Walken\'s good name. I could barely sit through it."
      }
    }
  }
}

"""

def serialize_example(label, text):
  """
  Creates a tf.train.Example message ready to be written to a file.
  """
  # Create a dictionary mapping the feature name to the tf.train.Example-compatible
  # data type.
  feature = {
      'label': _int64_feature(label),
      'text': _bytes_feature(text)
  }

  # Create a Features message using tf.train.Example.

  example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
  return example_proto.SerializeToString()

def convert_csv_tfrecord(csv_path, tfrecord_path):
   with open(csv_path, newline='') as csvfile:
      csv_reader = csv.reader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE, escapechar='\\')

      with tf.io.TFRecordWriter(tfrecord_path) as writer:
         for row in csv_reader:
            text = row[1][1:]
            text = text[:-1]
            text = str.encode(text)
            label = int(row[0])
            example = serialize_example(label, text)
            writer.write(example)

# TEST
serialized_example = serialize_example(0, b"hello world")
example_proto = tf.train.Example.FromString(serialized_example)
print(example_proto)

print(convert_csv_tfrecord('./twitter.csv', './twitter.tfrecord'))
