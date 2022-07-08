#!/usr/bin/env python3

# A *very* quick-and-dirty API test, everything hardcoded.

import json
import requests

base_url = 'https://reqres.in'

# create these variables for the comparison
user_info_list = {}
user_info_single = {}

# and a result list
results = []

# hardcode a couple of things we check for
user_id = '11'
unsuccessful_email = 'failure@unsuccessful'

# get the oracles, which contain the expected results
with open('oracles/oracle.json', 'r') as oracle_file:
	oracle = json.loads(oracle_file.read())

# we prepare to write our results
with open('results.js', 'w') as result_file:

	# some recurring validations for unexpected http statuses
	def request_validation(response, case, status):
		if response.status_code != status:
			results.append({case: 'error ' + str(response.status_code)})

	# first we test the user list endpoint
	def get_user_list():
		# get the "page"
		user_data = requests.get(base_url + '/api/users?page=2')

		# do the validation whether we get an error
		request_validation(user_data, 'list', 200)

		# we check if we got an error back from the validation
		if (len(results) == 0):

			# get the actual list out of the request object
			user_data = user_data.json()
			user_list = user_data['data']

			# parse the list and dump the specified entry
			for i in range(0, len(user_list)):
				if (str(user_list[i]['id']) == user_id):
					user_info_list = user_list[i]
					if (user_info_list != oracle):
						results.append({'list': 'failure'})
					else:
						results.append({'list': 'success'})

			# return the user object
			return(user_info_list)

	# then we test the single user endpoint
	def get_single_user(single_user_id):
		# get the user with the specific user ID
		user_data = requests.get(base_url + '/api/users/' + single_user_id)

		# validate
		request_validation(user_data, 'single', 200)

		# we check if we got an error back from the validation
		if ('single' not in results[-1]):

			# get the actual user data
			user_data = user_data.json()
			user_info_single = user_data['data']
			if (user_info_single != oracle):
				results.append({'single': 'failure'})
			else:
				results.append({'single': 'success'})
			# return the user object
			return(user_info_single)


	# let's compare them too
	def compare_list_and_single_user(list_user, single_user):
		# check that we don't have any errors...
		if ('error' not in results[-2]['list']) and ('error' not in results[-1]['single']):
			# ...and compare user list vs single user
			if (list_user != single_user):
				results.append({'compare': 'failure'})
			else:
				results.append({'compare': 'success'})

		# if we do have errors, return that comparison failed
		# even if both have errors, because that's a failure.
		else:
			results.append({'compare': 'failure'})

	# then we test successful user creation
	def create_successful(name, job):
		# make a dict of the name and job
		request_payload = {}
		request_payload['name'] = name
		request_payload['job'] = job

		# poke the endpoint with a POST
		r = requests.post(base_url + '/api/users', json=request_payload)

		# validate if we get an error back
		request_validation(r, 'createUser', 201)

		if ('createIser' not in results[-1]):
			response = r.json()
			if (response['name'] != name) or (response['job'] != job):
				results.append({'createUser': 'failure'})
			else:
				results.append({'createUser': 'success'})

	# lastly we test unsuccessful registration
	def register_unsuccessful(email):
		# make a dict of the name and job
		request_payload = {}
		request_payload['email'] = email

		# poke the endpoint with a POST
		r = requests.post(base_url + '/api/register', json=request_payload)

		# validate that we do get an error back
		request_validation(r, 'failedRegistration', 400)

		if ('failedRegistration' not in results[-1]):
			response = r.json()
			if (response['error'] != 'Missing password' or 'error' not in response):
				results.append({'failedRegistration': 'failure'})
			else:
				results.append({'failedRegistration': 'success'})

	# run the functions
	user_info_list = get_user_list()
	user_info_single = get_single_user(user_id)
	compare_list_and_single_user(user_info_list, user_info_single)
	create_successful('Peter', 'Sales')
	register_unsuccessful(unsuccessful_email)

	# write the results to the file
	result_data = 'var DATA = ' + str(results)
	result_file.write(result_data)
