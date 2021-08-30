# import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import matplotlib.pyplot as plt

img_name = [r"C:\Users\ryan.jhang\Documents\ryan\note\opencv\rgb_groups_by_kmeans\k-mean-example.jpg"]
filename_queue = tf.train.string_input_producer(img_name)
img_reader = tf.WholeFileReader()
_,image_jpg = img_reader.read(filename_queue)

image_decode_jpeg = tf.image.decode_jpeg(image_jpg)
image_decode_jpeg = tf.image.convert_image_dtype(image_decode_jpeg, dtype=tf.float32)

sess = tf.Session()
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

image_rgb_to_grayscale = tf.image.rgb_to_grayscale(image_decode_jpeg)
image_grayscale_to_rgb = tf.image.grayscale_to_rgb(image_rgb_to_grayscale)
image_rgb_to_hsv = tf.image.rgb_to_hsv(image_decode_jpeg)
image_hsv_to_rgb = tf.image.hsv_to_rgb(image_rgb_to_hsv)

print(image_rgb_to_grayscale.shape)
print(image_rgb_to_grayscale.dtype)

plt.figure()
plt.subplot(221)
#plt.imshow(sess.run(image_rgb_to_grayscale))
plt.title("image_rgb_to_grayscale")
plt.subplot(222)
plt.imshow(sess.run(image_grayscale_to_rgb))
plt.title("image_grayscale_to_rgb")
plt.subplot(223)
plt.imshow(sess.run(image_rgb_to_hsv))
plt.title("image_rgb_to_hsv")
plt.subplot(224)
plt.imshow(sess.run(image_hsv_to_rgb))
plt.title("image_hsv_to_rgb")
plt.show()