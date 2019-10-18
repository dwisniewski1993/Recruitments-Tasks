import os

from flask import Flask, render_template, jsonify, abort, make_response, request

from Models.Image import Images, Image

app = Flask(__name__)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES = Images(main_dir=APP_DIR)
METHODS = ['GET', 'POST', 'PUT', 'DELETE']


@app.route('/')
def handle_request():
    return render_template("index.html")


@app.route('/api/images', methods=METHODS)
def get_images():
    if request.method == 'GET':
        return jsonify({'images': IMAGES.get_images_list()})
    else:
        return jsonify({'images': 'Only GET method is supported here...'})


@app.route('/api/images/<int:image_id>', methods=METHODS)
def get_image(image_id: int):
    if request.method == 'GET':
        image = [image for image in IMAGES.get_images_list() if image['id'] == image_id]
        if len(image) == 0:
            abort(404)
        return jsonify({'image': image[0]})

    elif request.method == 'DELETE':
        image = [image for image in IMAGES.get_images_list() if image['id'] == image_id]

        if len(image) == 0:
            abort(404)

        if os.path.exists(image[0]['path']):
            os.remove(image[0]['path'])
            msg = 'Image deleted successfully'
        else:
            msg = 'Image with this id do not exist'

        return jsonify({'image': msg})

    else:
        return jsonify({'image': 'Only GET and DELETE methods are supported here...'})


@app.route('/api/upload', methods=METHODS)
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        name = file.filename

        IMAGES.increase_id()
        image_index = IMAGES.cur_id
        filename = f"{image_index}_{name}"
        path = os.path.join(IMAGES.working_directory, filename)
        img = Image(index=image_index, file_name=filename, path=path)
        IMAGES.add_image(image=img)
        file.save(path)

        return jsonify({'upload': 'Upload successful'})

    elif request.method == 'PUT':
        return jsonify({'upload': 'PUT method is not supported'})

    elif request.method == 'GET':
        return jsonify({'upload': 'Uploading images to server'})

    elif request.method == 'DELETE':
        return jsonify({'upload': 'DELETE method is not supported'})

    else:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
