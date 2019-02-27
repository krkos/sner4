"""sqlalchemy models"""
# pylint: disable=too-few-public-methods,abstract-method

from datetime import datetime
from sqlalchemy.orm import relationship
from sner.server.extensions import db


class Task(db.Model):
	"""holds settings/arguments for type of scan/scanner. eg. host discovery, fast portmap, version scan, ..."""

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(1000))
	module = db.Column(db.String(100), nullable=False)
	params = db.Column(db.Text())

	queues = relationship('Queue', back_populates='task')

	def __str__(self):
		return '<Task: %s>' % self.name


class Queue(db.Model):
	"""task assignment for specific targets"""

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(1000))
	task_id = db.Column(db.Integer(), db.ForeignKey('task.id'), nullable=False)
	group_size = db.Column(db.Integer(), nullable=False)
	priority = db.Column(db.Integer(), nullable=False)
	active = db.Column(db.Boolean())

	task = relationship('Task', back_populates='queues')
	targets = relationship('Target', back_populates='queue', cascade='delete,delete-orphan')
	jobs = relationship('Job', back_populates='queue', cascade='delete,delete-orphan')

	def __repr__(self):
		return '<Queue: %s>' % self.name
	def __str__(self):
		return '<Queue: %s>' % self.name


class Target(db.Model):
	"""single target of the task"""

	id = db.Column(db.Integer, primary_key=True)
	target = db.Column(db.Text())
	queue_id = db.Column(db.Integer(), db.ForeignKey('queue.id'), nullable=False)

	queue = relationship('Queue', back_populates='targets')


class Job(db.Model):
	"""assigned job"""

	id = db.Column(db.String(100), primary_key=True)
	assignment = db.Column(db.Text())
	result = db.Column(db.LargeBinary)
	queue_id = db.Column(db.Integer(), db.ForeignKey('queue.id'), nullable=False)
	time_start = db.Column(db.DateTime(), default=datetime.utcnow)
	time_end = db.Column(db.DateTime())

	queue = relationship('Queue', back_populates='jobs')