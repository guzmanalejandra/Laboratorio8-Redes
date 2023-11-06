from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Función para convertir imagen a bytes y reshape
def image_to_bytes(img_path):
    img = Image.open(img_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    img_array = np.array(img)
    reshaped_img_array = img_array.reshape((405, 480, 4))
    return reshaped_img_array.tobytes()

# Función para cifrar los bytes de la imagen
def encrypt_image_bytes(image_bytes, mode=AES.MODE_CBC):
    key = get_random_bytes(16)
    iv = get_random_bytes(16) if mode == AES.MODE_CBC else None
    cipher = AES.new(key, mode, iv) if iv else AES.new(key, mode)
    padded_img_bytes = pad(image_bytes, AES.block_size)
    encrypted_img_bytes = cipher.encrypt(padded_img_bytes)
    return encrypted_img_bytes, key, iv

# Función para convertir bytes cifrados a imagen
def bytes_to_image(encrypted_bytes, original_shape, mode='RGBA'):
    image_byte_size = original_shape[0] * original_shape[1] * original_shape[2]
    image_bytes = encrypted_bytes[:image_byte_size]
    image_array = np.frombuffer(image_bytes, dtype=np.uint8).reshape(original_shape)
    return Image.fromarray(image_array, mode)

# Convertir imagen a bytes
img_path = 'tux.bmp'  # Reemplazar con tu ruta de imagen
img_bytes = image_to_bytes(img_path)
original_shape = (405, 480, 4)

# Cifrar la imagen en modo CBC
encrypted_img_bytes_cbc, key_cbc, iv_cbc = encrypt_image_bytes(img_bytes, mode=AES.MODE_CBC)

# Cifrar la imagen en modo ECB
encrypted_img_bytes_ecb, key_ecb, _ = encrypt_image_bytes(img_bytes, mode=AES.MODE_ECB)

# Convertir bytes cifrados a imagen en modo CBC
encrypted_img_cbc = bytes_to_image(encrypted_img_bytes_cbc, original_shape)

# Convertir bytes cifrados a imagen en modo ECB
encrypted_img_ecb = bytes_to_image(encrypted_img_bytes_ecb, original_shape)

# Guardar las imágenes cifradas
encrypted_img_cbc.save('cbcimage.png')  # Reemplazar con tu ruta de guardado
encrypted_img_ecb.save('ecbimage.png')  # Reemplazar con tu ruta de guardado

# Visualizar las imágenes
plt.figure(figsize=(15, 5))

# Imagen original
plt.subplot(1, 3, 1)
plt.imshow(Image.open(img_path))
plt.title('Original Image')
plt.axis('off')

# Imagen cifrada en modo CBC
plt.subplot(1, 3, 2)
plt.imshow(encrypted_img_cbc)
plt.title('Encrypted Image (CBC Mode)')
plt.axis('off')

# Imagen cifrada en modo ECB
plt.subplot(1, 3, 3)
plt.imshow(encrypted_img_ecb)
plt.title('Encrypted Image (ECB Mode)')
plt.axis('off')

plt.show()
