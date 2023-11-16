import pickle

import requests
import logging
import aiohttp
from typing import Dict, Any, Optional
from .common_logging import Logging
from os import environ

_logger = Logging(filename='flask.server', exec_name=__name__).get_logger()

ODOO_SERVER_DOMAIN = environ.get('ODOO_SERVER_DOMAIN')
ODOO_WORK_DB = environ.get('ODOO_WORK_DB')


class OdooAPI:
    ODOO_SERVER_DOMAIN = environ.get('ODOO_SERVER_DOMAIN')

    @staticmethod
    async def make_request(url: str, method: str, data: Optional[Dict[str, Any]] = None, **kwargs):
        try:
            async with aiohttp.ClientSession() as session:
                if method == 'GET':
                    async with session.get(url=url, **kwargs) as response:
                        return await response.json()
                else:
                    async with session.post(url=url, data=data, **kwargs) as response:
                        return await response.json()
        except Exception as e:
            _logger.exception(e)

    @staticmethod
    def check_response(response):
        if response:
            if response.get('status') and response.get('status') == 200:
                return response.get('data')
            return response.get('result')
        return None


class ServiceAPI:

    @staticmethod
    async def register_service(uid: int, service_id: int, image_face_bytes: (bytes, bytearray),
                               image_license_plate_bytes: (bytes, bytearray)):
        try:
            url = '{}/odoo-api/spp/service/register?uid={}&service_id={}'.format(
                ODOO_SERVER_DOMAIN, uid, service_id
            )
            bufferer_image = pickle.dumps(dict(image_face_bytes=image_face_bytes,
                                               image_license_plate_bytes=image_license_plate_bytes))
            _logger.info(f'[ServiceAPI]: {url}')
            response = await OdooAPI.make_request(url=url, method='POST', data=bufferer_image,
                                                  headers={'Content-type': 'application/octet-stream'})
            _logger.info(f'[ServiceAPI]: {response}')
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)


class IndexAPI:

    @staticmethod
    async def info() -> Optional[Dict[str, Dict[str, Any]]]:
        try:
            url = f'{ODOO_SERVER_DOMAIN}/odoo-api/spp/index/info'
            _logger.info(f'[IndexAPI]: {url}')
            response = await OdooAPI.make_request(url=url, method='GET')
            _logger.info(f'[IndexAPI]: {response}')
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)


class UserAPI:

    @staticmethod
    async def sign_in(email: str, password: str):
        try:
            url = f'{ODOO_SERVER_DOMAIN}/web/session/authenticate'
            data = dict(params=dict(db=ODOO_WORK_DB, login=email, password=password))
            _logger.info(f'[UserAPI]: {url}: {data}')
            response = await OdooAPI.make_request(url=url, method='GET', json=data)
            _logger.info(f'[UserAPI]: {response}')
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)

    @staticmethod
    async def sign_out():
        try:
            url = f'{ODOO_SERVER_DOMAIN}/odoo-api/spp/user/sign_out'
            _logger.info(f'[UserAPI]: {url}')
            response = await OdooAPI.make_request(url=url, method='POST')
            _logger.info(f'[UserAPI]: {response}')
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)

    @staticmethod
    async def sign_up(login: str, password: str, fullname: str):
        try:
            url = f'{ODOO_SERVER_DOMAIN}/odoo-api/spp/user/sign_up'
            data = dict(login=login, password=password, name=fullname)
            _logger.info(f'[UserAPI]: {url}: {data}')
            response = await OdooAPI.make_request(url=url, method='POST', json=data)
            _logger.info(f'[UserAPI]: {response}')
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)

    @staticmethod
    async def profile(uid):
        try:
            url = f'{ODOO_SERVER_DOMAIN}/odoo-api/spp/user/profile?uid={uid}'
            _logger.info(f'[UserAPI]: {url}')
            response = await OdooAPI.make_request(url=url, method='POST')
            _logger.info(f'[UserAPI]: {response}')
            return OdooAPI.check_response(response)
        except Exception as e:
            _logger.exception(e)


class Address:

    @staticmethod
    def get_provinces():
        try:
            response = requests.get(url=f'{ODOO_SERVER_DOMAIN}/odoo-api/spp/get-provinces')
            data = response.json().get('data')
            return data
        except Exception as e:
            _logger.exception(e)