# -*- coding: utf-8 -*-
# Copyright (c) 2013, 2014 Corvusoft

from lettuce import step, world
import base64
from helpers import *

@step(u'I have configured a service with a default resource$')
def i_have_configured_a_service_with_a_default_resource(step):
	if not hasattr(world, 'service') or world.service == None:
		world.service = Service(world.port)

	world.service.publish_default_resource()


@step(u'I have configured a service with a custom resource and response header "([^"]*)" and a value of "([^"]*)"$')
def i_have_configured_a_service_with_a_custom_resource_and_response_header_name_and_a_value_of_value(step, name, value):
	if not hasattr(world, 'service') or world.service == None:
		world.service = Service(world.port)

	world.service.publish_resource_with_response_header(name, value)


@step(u'I have configured a service and a resource with a custom "([^"]*)" handler$')
def i_have_configured_a_service_with_a_custom_method_handler(step, method):
	if not hasattr(world, 'service') or world.service == None:
		world.service = Service(world.port)

	world.service.publish_resource("/", method)

@step(u'I have configured a service and published a resource at "([^"]*)" with a "([^"]*)" header filter of "([^"]*)"$')
def i_have_published_a_resource_at_path_with_a_header_filter_of_value(step, path, header, value): #header and value aint used mofo
	if not hasattr(world, 'service') or world.service == None:
		world.service = Service(world.port)

	if value == "application/json":
		world.service.publish_json_resource(path)
	elif value == "application/xml":
		world.service.publish_xml_resource(path)
	elif value == "1.0":
		world.service.publish_api_1_0_resource(path)
	elif value == "1.1":
		world.service.publish_api_1_1_resource(path)
	else:
		assert False, "Unknown resource requested"

@step(u'I have published a resource at "([^"]*)" with a "([^"]*)" header filter of "([^"]*)"$')
def i_have_published_a_resource_at_path_with_a_header_filter_of_value(step, path, header, value):
	if value == "application/json":
		world.service.publish_json_resource(path)
	elif value == "application/xml":
		world.service.publish_xml_resource(path)
	elif value == "1.0":
		world.service.publish_api_1_0_resource(path)
	elif value == "1.1":
		world.service.publish_api_1_1_resource(path)
	else:
		assert False, "Unknown resource requested"



# @step(u'I have published a resource at "([^"]*)" with a custom "([^"]*)" handler')
# def i_have_published_a_resource_with_a_custom_method_handler(step, path, method):
# 	world.service.publish_resource(path, method)


@step(u'I perform a HTTP "([^"]*)" request to "([^"]*)" with header "([^"]*)" set to "([^"]*)"$')
def i_perform_a_http_method_request_to_path_with_header_set_to_value(step, method, path, header, value):
	http_method = method.upper()

	url = world.url + path

	headers = {'User-Agent':'acceptance tests', 'accept-encoding': 'gzip, deflate', header:value}

	world.service.response, world.service.response.body = world.http.request(url, http_method, headers=headers)


@step(u'I perform a HTTP "([^"]*)" request$')
def i_perform_a_http_method_request(step, method):
	http_method = method.upper()

	headers = {'User-Agent':'acceptance tests', 'accept-encoding': 'gzip, deflate'}

	world.service.response, world.service.response.body = world.http.request(world.url, http_method, headers=headers)


@step(u'I should see a response body of "([^"]*)"$')
def i_should_see_a_response_body_of_data(step, data):
	assert world.service.response.body == data, "Expected response: " + data + " Received response: " + world.service.response.body


@step(u'I should see a "([^"]*)" response header with a value of "([^"]*)"$')
def i_should_see_a_header_value_of(step, name, value):
	header_name  = name if name in world.service.response else name.lower()
	assert header_name in world.service.response, "No '%s' header found!" % name

	header_value = world.service.response[header_name]
	assert header_value == value, "Expected %s=%s, Actual %s=%s" % (name, value, header_name, header_value)

@step(u'I should see a body of:$')
def and_i_should_see_a_body_of(step):
	expected = step.multiline;
	expected = unicode.replace(expected, '\n', '\r\n')
	expected += '\r\n'

	assert expected == world.service.response.body


@step(u'I have configured a service with a custom authentication handler$')
def i_have_configured_a_service_with_a_custom_authentication_handler(step):
	if not hasattr(world, 'service') or world.service == None:
		world.service = BasicAuthService(world.port)

	world.service.publish_resource_with_response_header("dummy", "header")

#add username + password to cuke
@step(u'I perform a basic-auth HTTP "([^"]*)" request$')
def i_perform_an_basic_auth_http_method_request(step, method):
	auth = base64.encodestring( 'Aladdin' + ':' + 'open sesame' )
	http_method = method.upper()
	headers = {'User-Agent':'acceptance tests', 'accept-encoding': 'gzip, deflate', 'Authorization' : 'Basic ' + auth }
	world.service.response, world.service.response.body = world.http.request(world.url, http_method, headers=headers)

@step(u'I should see a status code of "([^"]*)"$')
def then_i_should_see_a_status_code_of_status(step, status_code):
	assert world.service.response.status == int(status_code), "Status code expectation of %s does not match %s" %(status_code, world.service.response.status)

@step(u'I perform an unauthorised basic-auth HTTP "([^"]*)" request$')
def i_perform_an_unauthorised_basic_auth_http_method_request(step, method):
	auth = base64.encodestring( 'Glasgow' + ':' + 'Edinburgh' )
	http_method = method.upper()
	headers = {'User-Agent':'acceptance tests', 'accept-encoding': 'gzip, deflate', 'Authorization' : 'Basic ' + auth }
	world.service.response, world.service.response.body = world.http.request(world.url, http_method, headers=headers)