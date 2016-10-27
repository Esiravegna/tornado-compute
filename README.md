# Summary
Sample application for building a tornado-powered webservice that runs blocking calls sequentially on a second thread. Handlers of the webservice remain asynchronous, therefore many requests can be accepted in parallel.

# Scenario
+ you want to accepts many requests in parallel
+ computation is slow (fine for the client, but unacceptable for the server)
+ computation is blocking
+ all computations must happend on the same thread/process
+ the computation thread/process must be pre-initialized only once (common for deep learning frameworks)

# Solution
Before the service is started, a ComputationBroker is created. It will import Processing.py on a new thread and creates one instance of the Processor. It uses a pipe to wait for incoming requests.
Each computation/request is indentified by a unique key. When a request comes in, this key is passed through the pipe to the computation process. The computation loop at the other end of the pipe sequentially does the (blocking) calls, while the main thread asynchronously waits for the finished computation key to be returned through the pipe.

# ToDo
+ implement handling of really long-running jobs (where the client must ask for the result) like described here: http://farazdagi.com/blog/2014/rest-long-running-jobs/