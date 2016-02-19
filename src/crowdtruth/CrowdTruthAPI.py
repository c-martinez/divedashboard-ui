import httplib2
import simplejson

class CrowdTruthAPI():

	def __init__(self, config):
		self.config = config

	def getJobsOfCollection(self, collection, page):
		collection = 'temp'
		return self.fetchJobsFromCT(collection, page)


	def fetchJobsFromCT(self, collection, page=0, limit=10):
		jobs = []
		http = httplib2.Http()
		url = '%s/search?noCache&&collection=%s&match[documentType]=job' % (self.config['CROWDTRUTH_API'], collection)
		url += '&orderBy[created_at]=desc&limit=%s&page=%s&authkey=%s' % (
			limit, page, self.config['CROWDTRUTH_API_KEY']
		)
		print url
		resp, content = http.request(url, 'GET')
		print resp
		data = None
		if resp and resp['status'] == '200':
			try:
				data = simplejson.loads(content)
			except simplejson.JSONDecodeError, e:
				print e
		if data and type(data) == dict and data.has_key('documents'):
			for d in data['documents']:
				jobs.append(self.toClientObject(d))
		return jobs

	def fetchAllJobsFromCT(self, collection, jobs, page=0, limit=10):
		http = httplib2.Http()
		url = '%s/search?noCache&&collection=%s&match[documentType]=job' % (self.config['CROWDTRUTH_API'], collection)
		url += '&orderBy[created_at]=desc&limit=%s&page=%s&authkey=%s' % (
			limit, page, self.config['CROWDTRUTH_API_KEY']
		)
		resp, content = http.request(url, 'GET')
		print resp
		data = None
		if resp and resp['status'] == '200':
			try:
				data = simplejson.loads(content)
			except simplejson.JSONDecodeError, e:
				print e
		if data and type(data) == dict and data.has_key('documents'):
			if len(data['documents']) == 0:
				return jobs
			else:
				for d in data['documents']:
					jobs.append(self.toClientObject(d))
				return self.fetchJobsFromCT(collection, jobs, page + 1)
		print 'exiting...'
		return jobs

	def toClientObject(self, job):
		data = {
			'id' : job['_id'], #"entity/text/news/job/48",
			'activity_id' : job['activity_id'], #"activity/jobcreator/348",
			'batch_id' : job['batch_id'], #"entity/text/news/batch/9",
			'completion' : job['completion'], #0,
			'created_at' : job['created_at'], #"2015-02-11 15:40:05",
			'domain' : job['domain'], # "news",
			'jobConf_id' : job['jobConf_id'], #"entity/text/news/jobconf/47",
			'platformJobId' : job['platformJobId'], #"689110",
			'project' : job['project'], #"CrowdWatson",
			'status' : job['status'], #"running",
			'type' : job['type'], #"EventTypeIdentificationTweet_T1",
			'unitsCount' : job['unitsCount'], #30,
			'updated_at' : job['updated_at'], #"2015-02-13 16:27:36",
			'user_id' : job['user_id'] #"oana"
		}
		if job.has_key('latestMetrics'):
			data['latestMetrics'] = job['latestMetrics']
		if job.has_key('projectedCost'):
			data['projectedCost'] = job['projectedCost']
		if job.has_key('realCost'):
			data['realCost'] = job['realCost']
		if job.has_key('results'):
			data['results'] = job['results']
		if job.has_key('startedAt'):
			data['startedAt'] = job['startedAt']
		if job.has_key('url'):
			data['url'] = job['url']

		#add the config
		conf = {'title' : 'Unknown'}
		if job.has_key('hasConfiguration') and job['hasConfiguration'].has_key('content'):
			for k, v in job['hasConfiguration']['content'].iteritems():
				conf[k] = v
		data['config'] = conf
		return data


if __name__ == '__main__':
	print 'Try out the CrowdTruth API:'
	api = CrowdTruthAPI()
	api.getJobs('temp')#collection name=temp
