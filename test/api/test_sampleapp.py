import json
import logging
import os
import sys

from mongoengine.errors import NotUniqueError

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")
import base

from sampleapp import app
from sampleapp.models import Item

log = logging.getLogger(__name__)


class TestSampleAppAPI(base.SampleAppTestCase):
    def setUp(self):
        super(TestSampleAppAPI, self).setUp()

    def tearDown(self):
        super(TestSampleAppAPI, self).tearDown()

    def test_get_all_items(self):
        resp = self.app.get('/items/')
        items = json.loads(resp.data)
        self.assertEquals(len(items), 0)

        name1 = "test1 name"
        description1 = "test1 description"
        price1 = 1.00

        name2 = "test2 name"
        description2 = "test2 description"
        price2 = 2.00

        item1 = Item(name=name1, description=description1, price=price1)
        item2 = Item(name=name2, description=description2, price=price2)
        item1.save(force_insert=True)
        item2.save(force_inster=True)

        resp = self.app.get('/items/')
        self.assertEquals(resp.status_code, 200)
        items = json.loads(resp.data)
        self.assertEquals(len(items), 2)

        for item in items:
            self.assertIn(item["name"], [item1.name, item2.name])
            self.assertIn(item["description"], [item1.description, item2.description])

    def test_create(self):
        name = "test"
        description = "description"
        price = 1.00

        data = {"name":name, "description":description, "price":price}
        json_data = json.dumps(data)

        resp = self.app.post('/items/', data=json_data, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        item = json.loads(resp.data)
        self.assertEquals(item["name"], name)
        self.assertEquals(item["description"], description)
        self.assertEquals(item["price"], price)

    def test_create_already_exists(self):
        name = "test"
        description = "description"
        price = 1.00
        item1 = Item(name=name, description=description, price=price)
        item1.save(force_insert=True)

        data = {"name":name, "description":description, "price":price}
        json_data = json.dumps(data)

        resp = self.app.post('/items/', data=json_data, content_type='application/json')
        self.assertEquals(resp.status_code, 409)

    def test_read(self):
        name = "test"
        description = "description"
        price = 1.00

        item = Item(name=name, description=description, price=price)
        item.save(force_insert=True)

        resp = self.app.get("/items/%s/" % (name))
        self.assertEquals(resp.status_code, 200)
        items = json.loads(resp.data)
        self.assertEquals(len(items), 1)
        self.assertEquals(items[0]["name"], name)
        self.assertEquals(items[0]["description"], description)
        self.assertEquals(items[0]["price"], price)

    def test_update(self):
        name = "test"
        description = "description"
        price = 1.00

        item = Item(name=name, description=description, price=price)
        item.save(force_insert=True)

        updated_description = "new description"
        updated_price = 99.99
        data = {"name":name, "description":updated_description, "price":updated_price}
        json_data = json.dumps(data)

        resp = self.app.put("/items/%s/" % (name), data=json_data, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        items = json.loads(resp.data)
        self.assertEquals(len(items), 1)
        self.assertEquals(items[0]["name"], name)
        self.assertEquals(items[0]["description"], updated_description)
        self.assertEquals(items[0]["price"], updated_price)

        resp = self.app.get("/items/%s/" % (name))
        self.assertEquals(resp.status_code, 200)
        items = json.loads(resp.data)
        self.assertEquals(len(items), 1)
        self.assertEquals(items[0]["name"], name)
        self.assertEquals(items[0]["description"], updated_description)
        self.assertEquals(items[0]["price"], updated_price)

    def test_delete(self):
        name = "test"
        description = "description"
        price = 1.00

        item = Item(name=name, description=description, price=price)
        item.save(force_insert=True)

        resp = self.app.delete("/items/%s/" % (name))
        self.assertEquals(resp.status_code, 200)

        resp = self.app.get("/items/%s/" % (name))
        self.assertEquals(resp.status_code, 404)
