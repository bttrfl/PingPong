#!/usr/bin/env python3
from unittest import TestCase
import requests as r
import unittest


class TestApp(TestCase):
    user = 'test'
    password = 'test'
    host = '0.0.0.0'
    port = ':80'

    
    def test_fake_login(self):
        resp = r.post('http://' + self.host + self.port + "/user/login", json={
            "user": self.user,
            "pwd": self.password
            }, verify=True)
        self.assertEqual(resp.status_code, 401)


    def test_invalid_login(self):
        resp = r.post('http://' + self.host + self.port + "/user/login", json={
            "user": self.user,
            }, verify=True)
        self.assertEqual(resp.status_code, 400)

   
    def test_double_signUp(self):
        resp = r.post('http://' + self.host + self.port + "/user/signup", json={
            "user": self.user,
            "pwd": self.password
            }, verify=True)
        self.assertEqual(resp.status_code, 200)
        
        resp = r.post('http://' + self.host + self.port + "/user/signup", json={
            "user": self.user,
            "pwd": self.password
            }, verify=True)
        self.assertEqual(resp.status_code, 401)

    
    def test_double_login(self):
        resp = r.post('http://' + self.host + self.port + "/user/login", json={
            "user": self.user,
            "pwd": self.password
            }, verify=True)
        self.assertEqual(resp.status_code, 200)

        resp = r.post('http://' + self.host + self.port + "/user/login", json={
            "user": self.user,
            "pwd": self.password
            }, verify=True)
        self.assertEqual(resp.status_code, 401)



    def test_fake_logout(self):
        resp = r.post('http://' + self.host + self.port + "/user/logout", json={
            "user": self.user + "1",
            "pwd": self.password + "1"
            }, verify=True)
        self.assertEqual(resp.status_code, 400)

if __name__ ==  '__main__':
    unittest.main()
