"""command scheduler tests"""

from random import random
from sner.server.command.scheduler import scheduler_command
from sner.server.extensions import db
from sner.server.model.scheduler import Queue

from tests.server import persist_and_detach
from tests.server.model.scheduler import create_test_queue, create_test_target, fixture_test_queue, fixture_test_task # pylint: disable=unused-import


def test_queue_list_command(runner, fixture_test_queue): # pylint: disable=redefined-outer-name
	"""queue list command test"""

	test_queue = fixture_test_queue
	test_queue.name += ' command list '+str(random())
	persist_and_detach(test_queue)


	result = runner.invoke(scheduler_command, ['queue_list'])
	assert result.exit_code == 0
	assert test_queue.name in result.output


def test_queue_add_command(runner, fixture_test_task): # pylint: disable=redefined-outer-name
	"""queue add command test"""

	test_queue = create_test_queue(fixture_test_task)
	test_queue.name += ' command add '+str(random())


	result = runner.invoke(scheduler_command, ['queue_add', str(test_queue.task.id), '--name', test_queue.name])
	assert result.exit_code == 0

	queue = Queue.query.filter(Queue.name == test_queue.name).one_or_none()
	assert queue
	assert queue.name == test_queue.name


	db.session.delete(queue)
	db.session.commit()


def test_queue_enqueue_command(runner, fixture_test_queue): # pylint: disable=redefined-outer-name
	"""queue enqueue route test"""

	test_queue = fixture_test_queue
	test_queue.name += ' enqueue '+str(random())
	persist_and_detach(test_queue)
	test_target = create_test_target(test_queue)


	result = runner.invoke(scheduler_command, ['queue_enqueue', str(test_queue.id), test_target.target])
	assert result.exit_code == 0

	queue = Queue.query.filter(Queue.id == test_queue.id).one_or_none()
	assert queue.targets[0].target == test_target.target


	db.session.delete(queue.targets[0])
	db.session.commit()


def test_queue_flush_command(runner, fixture_test_queue): # pylint: disable=redefined-outer-name
	"""queue flush route test"""

	test_queue = fixture_test_queue
	test_queue.name += ' flush '+str(random())
	persist_and_detach(test_queue)
	test_target = create_test_target(test_queue)
	persist_and_detach(test_target)


	result = runner.invoke(scheduler_command, ['queue_flush', str(test_queue.id)])
	assert result.exit_code == 0


	queue = Queue.query.filter(Queue.id == test_queue.id).one_or_none()
	assert not queue.targets


def test_queue_delete_command(runner, fixture_test_task): # pylint: disable=redefined-outer-name
	"""queue delete command test"""

	test_queue = create_test_queue(fixture_test_task)
	test_queue.name = test_queue.name+' delete command '+str(random())
	persist_and_detach(test_queue)


	result = runner.invoke(scheduler_command, ['queue_delete', str(test_queue.id)])
	assert result.exit_code == 0

	queue = Queue.query.filter(Queue.id == test_queue.id).one_or_none()
	assert not queue


def test_enumips(runner):
	"""basic enumerator test"""

	result = runner.invoke(scheduler_command, ['enumips', '127.0.0.128/30'])
	assert result.exit_code == 0
	assert '127.0.0.129' in result.output
	assert '127.0.0.130' in result.output