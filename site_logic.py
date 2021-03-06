import datetime
from rfc3339 import rfc3339 as rfc
from model import User, Task, Collect, Kao
import timehelpers

def convert_datetime_to_dict(dt):
	dt_dict = {
		"year" : dt.year,
		"month": dt.month,
		"day" : dt.day,
		"hours" : dt.hour,
		"minutes" : dt.minute,
		"seconds" : dt.second,
		"milliseconds" : 0
	}
	print("hour:",dt.hour)
	return dt_dict


def convert_tasklist_to_list(tasklist):

	task_list = [
		{"task_id":task.task_id,
		"msg":task.msg, 
		"is_complete":task.is_complete,
		"due_date":convert_datetime_to_dict(task.due_date),
		"is_repeating":task.is_repeating,
		"user_id":task.user_id} for task in tasklist]

	return task_list
def convert_tasklist_to_dict(tasklist,tz_string):

	task_list = [
		{"task_id":task.task_id,
		"msg":task.msg, 
		"is_complete":task.is_complete,

		"due_date":convert_datetime_to_dict(timehelpers.convert_UTC_to_user_tz(task.due_date,tz_string)),
		
		"is_repeating":task.is_repeating,
		"user_id":task.user_id} for task in tasklist]
	task_dict = {}
	for task in task_list:
		task_dict[task['task_id']] = task

	return task_dict

def convert_user_to_dict(user):

	user_dict = {
		"user_id":user.user_id,
		"username":user.username,
		"email": user.email,
		"timezone": user.timezone
		}

	return user_dict

def convert_collects_to_dict(collects):

	collect_dict_list = [
		{"kao_id":collect.kao_id,
		'kao_str': Kao.query.get(collect.kao_id).kao,
		 'date':convert_datetime_to_dict(collect.collect_date)} for collect in collects]

	return collect_dict_list



