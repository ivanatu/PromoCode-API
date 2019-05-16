from flask_testing import TestCase
from .. import models
from .. import promoapp
from ..models import db
import json
from datetime import datetime
import unittest

class BaseTests(TestCase):
    """Tests for the Promo codes API endpoints """

    test_code = "OorOFL"
    test_event = "bukoto"
    test_expiry_date = datetime(2019, 5, 15, 10, 10, 10)
    test_status = "active"
    test_price = "1200"
    test_radius = "100"

    def create_app(self):
        return promoapp

    def create_promo_code(self):
        """This is a test to use during the running of tests"""
        promo_code = models.Promo_code(code=self.test_code,
                           event=self.test_event,
                           expiry_date=self.test_expiry_date,
                           price=self.test_price,
                           radius=self.test_radius,
                           status=self.test_status)
        db.session.add(promo_code)
        db.session.commit()

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_promo_code(self):
        """
        This tests whether a promo code has been created successfully
        """
        self.create_promo_code()
        with self.client:
            response = self.client.post('/generate_code',
                                        content_type='application/json',
                                        data=json.dumps(dict(code="OorOFL",
                                                             event="bukoto",
                                                             expiry_date="2019-05-15 13:40:22.53219",
                                                             status="active",
                                                             price="1200",
                                                             radius="100")))
            reply = json.loads(response.data.decode())
            self.assertTrue(reply['code'],
                            msg="id key fail")
            # self.assertEqual(reply['code'], "OorOFL",
            #                  msg="promo_code key fail")
            self.assertEqual(reply['status'], "pass",
                             msg="status key fail")
            self.assertEqual(reply['message'], "promo code generated successfully",
                             msg="message key fail")

    def test_view_all_promo_codes(self):
        """
        This is to test whether we are able view all promo codes.
        """
        self.create_promo_code()
        with self.client:
            response = self.client.get('/all_promo_codes',
                                       content_type='application/json')

            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "pass",
                             msg="status key fail")
            self.assertEqual(reply['message'], "promo codes found",
                             msg="message key fail")

    def test_view_active_promo_codes(self):
        """
        This is to test whether we are able view all active promo codes.
        """
        self.create_promo_code()
        with self.client:
            response = self.client.get('/active_promo_codes',
                                       content_type='application/json')

            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "pass",
                             msg="status key fail")
            self.assertEqual(reply['message'], "active promo codes found",
                             msg="message key fail")



    def test_view_non_existing_promo_codes(self):
        """
        This tests that we cannot see promo_codes that
        have not been created yet.
        """
        with self.client:
            response = self.client.get('/all_promo_codes',
                                       content_type='application/json')
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['count'], "0", msg="count key fail")
            self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertEqual(reply['message'], "no promo codes found",
                             msg="message key fail")

    def test_view_non_existing_active_promo_codes(self):
        """
        This tests that we cannot see non existing active promo_codes .
        """
        with self.client:
            response = self.client.get('/active_promo_codes',
                                       content_type='application/json')
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['count'], "0", msg="count key fail")
            self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertEqual(reply['message'], "no active promo codes found",
                             msg="message key fail")

    def test_deactivate_an_existing_promo_code(self):
        """
        Test whether we can deactivate an existing active promo code.
        """
        self.create_promo_code()
        with self.client:
            response = self.client.put('/promo_code/1',
                                       content_type='application/json',
                                       data=json.dumps(dict(status="deactivated")))
            reply = json.loads(response.data.decode())

            self.assertTrue(reply['status'], msg="status key fail")
            self.assertEqual(reply['status'], "pass", msg="status key fail")
            self.assertEqual(reply['message'], "promo_code deactivated",
                             msg="message key fail")

    def test_deactivate_a_non_existing_promo_code(self):
        """
         Test the promo code to be deactivated doesnot exist.
        """
        with self.client:
            response = self.client.put('/promo_code/1',
                                       content_type='application/json',
                                       data=json.dumps(dict(status="deactivated")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="status key fail")
            self.assertEqual(reply['message'], "code doesnot exist",
                             msg="message key fail")

    def test_deactivate_an_already_deactivated_code(self):
        """
         Test the promo code to be deactivated doesnot exist.
        """
        # self.create_promo_code()
        promo_code = models.Promo_code(code=self.test_code,
                                       event=self.test_event,
                                       expiry_date=self.test_expiry_date,
                                       price=self.test_price,
                                       radius=self.test_radius,
                                       status="deactivated")
        db.session.add(promo_code)
        db.session.commit()
        with self.client:
            response = self.client.put('/promo_code/1',
                                       content_type='application/json',
                                       data=json.dumps(dict(status="deactivated")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['status'], "fail", msg="status key fail")

