"""controller notes tests"""

from http import HTTPStatus
from random import random

from flask import url_for

from sner.server import db
from sner.server.model.storage import Note
from tests.server import persist_and_detach
from tests.server.model.storage import create_test_note


def test_note_list_route(client):
	"""note list route test"""

	response = client.get(url_for('storage.note_list_route'))
	assert response.status_code == HTTPStatus.OK
	assert b'<h1>Notes list' in response


def test_note_add_route(client, test_host):
	"""note add route test"""

	test_note = create_test_note(test_host)
	test_note.data = 'test note add %d' % random()


	form = client.get(url_for('storage.note_add_route', host_id=test_note.host.id)).form
	form['ntype'] = test_note.ntype
	form['data'] = test_note.data
	response = form.submit()
	assert response.status_code == HTTPStatus.FOUND

	note = Note.query.filter(Note.data == test_note.data).one_or_none()
	assert note
	assert note.ntype == test_note.ntype
	assert note.data == test_note.data


	db.session.delete(note)
	db.session.commit()


def test_note_edit_route(client, test_note):
	"""note edit route test"""

	test_note.data = 'test note edit %d' % random()
	persist_and_detach(test_note)


	form = client.get(url_for('storage.note_edit_route', note_id=test_note.id)).form
	form['data'] = 'edited '+form['data'].value
	response = form.submit()
	assert response.status_code == HTTPStatus.FOUND

	note = Note.query.filter(Note.id == test_note.id).one_or_none()
	assert note
	assert note.data == form['data'].value


def test_note_delete_route(client, test_host):
	"""note delete route test"""

	test_note = create_test_note(test_host)
	test_note.data = 'test note delete %d' % random()
	persist_and_detach(test_note)


	form = client.get(url_for('storage.note_delete_route', note_id=test_note.id)).form
	response = form.submit()
	assert response.status_code == HTTPStatus.FOUND

	note = Note.query.filter(Note.id == test_note.id).one_or_none()
	assert not note