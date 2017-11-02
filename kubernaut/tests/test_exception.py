import unittest
from kubernaut.exception import *
from uuid import uuid4


# class TestKubernautServiceException(unittest.TestCase):
#
#     def test_constructs_correctly(self):
#         expected_error_id = str(uuid4())
#         expected_message = """
# An error has occurred!
#
# This is a test message
#
# Status: 404 - Kubernaut.TestCase
# ID:     {}""".format(expected_error_id).strip()
#
#         ex = KubernautServiceException(
#             http_status=404,
#             code="Kubernaut.TestCase",
#             message="This is a test message",
#             error_id=expected_error_id
#         )
#
#         self.assertEqual(ex.error_id, expected_error_id)
#         self.assertEqual(ex.http_status, 404)
#         self.assertEqual(ex.code, "Kubernaut.TestCase")
#         self.assertEqual(str(ex), expected_message)
#
#     def test_create_kubernaut_service_exception(self):
#         expected_error_id = str(uuid4())
#         error_response_payload = {
#             "error": {
#                 "id":  expected_error_id,
#                 "code": "Kubernaut.TestCase",
#                 "description": "This is a test message",
#             }
#         }
#
#         ex = create_kubernaut_service_exception(404, error_response_payload)
#
#         self.assertEqual(ex.error_id, expected_error_id)
#         self.assertEqual(ex.http_status, 404)
#         self.assertEqual(ex.code, "Kubernaut.TestCase")
#
#     def test_create_kubernaut_service_exception_without_error_id(self):
#         expected_error_id = str(uuid4())
#         error_response_payload = {
#             "error": {
#                 "code": "Kubernaut.TestCase",
#                 "description": "This is a test message",
#             }
#         }
#
#         ex = create_kubernaut_service_exception(404, error_response_payload)
#
#         self.assertIsNotNone(ex.error_id)  # should  check that this is a datetime but this is good enough for now
#         self.assertEqual(ex.http_status, 404)
#         self.assertEqual(ex.code, "Kubernaut.TestCase")
