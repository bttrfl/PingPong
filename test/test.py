#!/usr/bin/env python3
from unittest import TestCase
import requests as r
import unittest


class TestApp(TestCase):
    user = 'random_test_final'
    password = 'random'
    host = '0.0.0.0'
    port = ':80'

    
    def test_fake_login(self):
        resp = r.post('http://' + self.host + self.port + "/user/login", data={
            "user": self.user,
            "pwd": self.password
            }, verify=True)
        self.assertEqual(resp.status_code, 401)


    def test_invalid_login(self):
        resp = r.post('http://' + self.host + self.port + "/user/login", data={
            "user": self.user,
            }, verify=True)
        self.assertEqual(resp.status_code, 400)

   
    def test_double_signUp(self):
        resp = r.post('http://' + self.host + self.port + "/user/signup", data={
            "user": self.user + "_success",
            "pwd": self.password
            }, verify=True)
        self.assertEqual(resp.status_code, 200)
        
        resp = r.post('http://' + self.host + self.port + "/user/signup", data={
            "user": self.user + "_success",
            "pwd": self.password 
            }, verify=True)
        self.assertEqual(resp.status_code, 401)

    
    def test_double_login(self):
        resp = r.post('http://' + self.host + self.port + "/user/signup", data={
            "user": self.user + "_success_1",
            "pwd": self.password
            }, verify=True)
        self.assertEqual(resp.status_code, 200)
        
        session = r.session()
        resp = session.post('http://' + self.host + self.port + "/user/login", data={
            "user": self.user + "_success_1",
            "pwd": self.password
            }, verify=True)
        self.assertEqual(resp.status_code, 200)

        resp = session.post('http://' + self.host + self.port + "/user/login", data={
            "user": self.user + "_success_1",
            "pwd": self.password
            }, verify=True)
        self.assertEqual(resp.status_code, 401)



    def test_fake_logout(self):
        resp = r.get('http://' + self.host + self.port + "/user/logout", data={
            "user": self.user + "_fail_",
            "pwd": self.password
            }, verify=True)
        self.assertEqual(resp.status_code, 400)

if __name__ ==  '__main__':
    unittest.main()
