import asyncio
from typing import Final
from flask import Blueprint, request, redirect, flash, session, render_template
from ..common.odoo_api import ServiceAPI
from ..common.messages import Categories, ServicePackMessage
from .users_bp import login_required

MAXIMUM_IMAGE_FACE: Final[int] = 4

services = Blueprint('services', __name__, url_prefix='/services')


# def encoding_face(face_image: List[bytes]):
#     encode_list = []
#     for image in face_image:
#         num_array = np.frombuffer(image, np.uint8)
#         img_list = cv2.imdecode(num_array, cv2.IMREAD_COLOR)
#         img_list_rgb = cv2.cvtColor(img_list, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img_list_rgb)[0]
#         encode_list.append(encode)
#     return encode_list
#
#
# def validate_license_plate(result: List[str]) -> bool:
#     if not result or len(result) != 2:
#         flash(LicensePlateMessage.RecognizeFailed.value, Categories.Error.value)
#         return False
#     elif not result[0][:2].isnumeric():
#         flash(LicensePlateMessage.LocalCodeInvalid.value, Categories.Error.value)
#         return False
#     elif not result[0][-1].isalpha():
#         flash(LicensePlateMessage.CharacterSeriesInvalid.value, Categories.Error.value)
#         return False
#     elif len(result[1]) not in [4, 5]:
#         flash(LicensePlateMessage.LengthRegistrationInvalid.value, Categories.Error.value)
#         return False
#     elif not result[1].isnumeric():
#         return False
#     return True
#
#
# def clean_character(text):
#     character_cleaned = re.sub(r'[^\w\s]', '', text)
#     character_cleaned = re.sub(r'\s', '', character_cleaned)
#     return character_cleaned
#
#
# def license_plate_ocr(license_plate_bytes: List[bytes]):
#     reader = easyocr.Reader(['en'])
#     license_plate_list = []
#     for license_plate_byte in license_plate_bytes:
#         result = [clean_character(r) for r in reader.readtext(image=license_plate_byte, detail=0)]
#         if not validate_license_plate(result):
#             return False
#         license_plate_list.append(''.join(result))
#     return license_plate_list


@services.route('/register', methods=['POST'])
@login_required
def register_service():

    service_id = int(request.form.get('service_id'))
    if not service_id:
        flash(ServicePackMessage.ServiceIdRequired.value, Categories.Error.value)
        return redirect('/')
    elif 'face_image[]' not in request.files:
        flash(ServicePackMessage.FileImageFacesRequired.value, Categories.Error.value)
        return redirect('/')
    elif len(request.files.getlist('face_image[]')) > MAXIMUM_IMAGE_FACE:
        flash(ServicePackMessage.Maximum3ImagesFace.value, Categories.Error.value)
        return redirect('/')
    elif 'license_plate_image[]' not in request.files:
        flash(ServicePackMessage.FileImageLicensePlateRequired.value, Categories.Error.value)
        return redirect('/')
    face_data = [{
        'face_binary': file.read(),
        'face_name': file.filename.split('.')[0].capitalize()
    } for file in request.files.getlist('face_image[]')]
    image_license_plate_bytes = [file.read() for file in request.files.getlist('license_plate_image[]')]
    asyncio.run(ServiceAPI.register_service(uid=session['user']['__uid'],
                                            service_id=service_id,
                                            image_face_bytes=face_data,
                                            image_license_plate_bytes=image_license_plate_bytes))
    return redirect('/users/profile')
