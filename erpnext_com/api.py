from __future__ import unicode_literals
import requests, json
import frappe
from frappe import _
from central.signup import signup as _signup

@frappe.whitelist(allow_guest=True)
def signup(full_name, email, subdomain, plan="Free-Solo", distribution="erpnext"):
	status = _signup(full_name, email, subdomain, distribution, plan)

	context = {
		'pathname': 'schools/signup' if distribution=='schools' else 'signup'
	}

	if status == 'success':
		location = frappe.redirect_to_message(_('Thank you for signing up'),
			"""<div><p>You will receive an email at <strong>{}</strong>,
			asking you to verify this account request.<br>
			If you are unable to find the email in your inbox, please check your SPAM folder.
			It may take a few minutes before you receive this email.</p>
			<p>Once you click on the verification link, your account will be ready in a few minutes.</p>
			</div>""".format(email), context=context)
	# TODO Need to decide whether this part of code is necessary or not
	# elif r.status_code in (417, 409):
	# 	# ValidationError, NameError
	# 	# show the message that we got from server
	# 	frappe.throw(json.loads(r.json()['_server_messages'])[0])

	else:
		# something went wrong
		location = frappe.redirect_to_message(_('Something went wrong'),
			'Please try again or drop an email to support@erpnext.com',
			context=context)

	return {
		'location': location
	}