def send_notification(event, registration_ids):
	registration_ids = [id.encode('utf-8') for id in registration_ids]
	data = {}
	import json
	# data['message'] = 'test notif'
	data['type'] = 'normal'
	data['message_type'] = 'The event '+event.name+'\'s schedule has changed to '+event.date_time.strftime('%d/%m/%Y at %H:%M') +' at '+event.venue
	fields = {'data':data, 'registration_ids' :registration_ids}
	headers = {'Authorization': 'key=AIzaSyDjYk4nCrXn6Nb2VL2EZgGbebT7NdLJ5s8','Content-Type': 'application/json' }
	print fields
	url = 'https://android.googleapis.com/gcm/send'
	import requests
	r = requests.post(url, data = json.dumps(fields), headers = headers)
	print r.content
	print r.status_code


def send_notification_custom(event, registration_ids, message):
	registration_ids = [id.encode('utf-8') for id in registration_ids]
	data = {}
	import json
	data['message'] = message
	data['msg_type'] = 'normal'
	# data['message'] = 'The event '+event.name+'\'s schedule has changed to '+event.date_time.strftime('%d/%m/%Y at %H:%M') +' at '+event.venue
	fields = {'data':data, 'registration_ids' :registration_ids}
	headers = {'Authorization': 'key=AIzaSyDjYk4nCrXn6Nb2VL2EZgGbebT7NdLJ5s8','Content-Type': 'application/json' }
	print fields
	url = 'https://android.googleapis.com/gcm/send'
	import requests
	r = requests.post(url, data = json.dumps(fields), headers = headers)
	print r.content
	print r.status_code


def send_event(event, image_url, registration_ids):
	'''
	Using this function as a means to update events in the app's local db by sending event details using android gcm
	'''
	registration_ids = [id.encode('utf-8') for id in registration_ids]
	data = {}
	import json
	data['msg_type'] = 'event'
	data['message'] = "A new event - "+ event.name +" has been added! Check it out on Event Hub"
	data['id'] = event.id
	data['type1'] = event.type
	data['subtype'] = event.subtype
	data['name'] = event.name
	# data['content'] = event.content
	data['description'] = event.content.description
	data['cname1'] = event.contact_name_1
	data['cname2'] = event.contact_name_2
	data['cno1'] = event.contact_number_1
	data['cno2'] = event.contact_number_2
	data['club'] = event.club.name
	data['image'] = image_url
	data['date_time'] = str(event.date_time)
	data['venue']=event.venue
	data['going'] = 0

	for key in data.keys():
		if type(data[key]) == unicode:
			data[key] = data[key].encode('utf-8')

	fields = {'data':data, 'registration_ids' :registration_ids}
	headers = {'Authorization': 'key=AIzaSyDjYk4nCrXn6Nb2VL2EZgGbebT7NdLJ5s8','Content-Type': 'application/json' }
	print fields
	url = 'https://android.googleapis.com/gcm/send'
	import requests
	r = requests.post(url, data = json.dumps(fields), headers = headers)
	print r.content
	print r.status_code

if __name__ == "__main__":
	# ids = ["APA91bGCS2kkPIHgjqmBhI5YW3TZaVJCGi3fxdlKcE4oA6USULcreEcdJIbRSsFGpqL8joRqa2Vzia5rEJUjJqwF69Xb5vp1W-HQNoLcSxh0d-z0NNRvgaQtGLxwHCmY9ldx5qrAJpo5EeoZ1zrypObXUza28MywLw"]
	# ids = ["APA91bGP44rcqurTWUcK5vpbBoTUgrpPFVdQKE4g4klzT73dEDYI28bKaa08aejfHP1UspuSVtlR4ADPY5ewBVNpE5VqqrN6UACiwuUB5KIrXGwZs1JJ1icpN6BaqkY8oN1fC6iEdakk"] #saiteja
	ids = ["APA91bEpuPhRN-y4Duj8zR1cqoxFMREwvu_cR9-luC9EEI7yfuUWwpWPUws8sTWtZENHnARpbv0PjeGXoORkSXxL3WYvuj7O_Lh6CPuy0XO7N2Oj7MWAagqNvGBxKg2ofZvDX9kodlNrDr7tRt9XEDBTXb6kgyTrnw"] #vivek
	event = {}
	event["name"] = "Test event"
	event["date_time"] = "tomorrow"


	data = {}
	import json
	data['message'] = "Test message"
	# data['message'] = 'The event '+event.name+'\'s schedule has changed to '+event.date_time.strftime('%d/%m/%Y at %H:%M') +' at '+event.venue
	fields = {'data':data, 'registration_ids' :ids}
	headers = {'Authorization': 'key=AIzaSyDjYk4nCrXn6Nb2VL2EZgGbebT7NdLJ5s8','Content-Type': 'application/json' }
	print fields
	url = 'https://android.googleapis.com/gcm/send'
	import requests
	r = requests.post(url, data = json.dumps(fields), headers = headers, verify = False)
	print r.content
	print r.status_code