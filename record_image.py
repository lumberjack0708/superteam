def record_image():
    with open("image/user_input.jpg", "rb") as f:
            image_data = f.read()
            with open("image/Test/test.jpg", "wb") as image:
                image.write(image_data)