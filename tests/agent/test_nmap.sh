#!/bin/sh

. tests/agent/lib.sh
TESTID="agent_test_nmap_$(date +%s)"
testserver_create


bin/server scheduler task_add nmap --name ${TESTID} --params '-sL'
bin/server scheduler queue_add ${TESTID} --name ${TESTID}
bin/server scheduler queue_enqueue ${TESTID} "127.0.0.1"


bin/agent --server 'http://localhost:19000' --debug --queue ${TESTID} --oneshot
if [ $? -ne 0 ]; then
	testserver_cleanup
	rreturn 1 'agent failed'
fi

OUTPUT_FILENAME=$(bin/server scheduler job_list | grep ${TESTID} | awk '{print $6}')
unzip -p ${OUTPUT_FILENAME} output.gnmap | grep -q 'Host: 127.0.0.1 (localhost)'
if [ $? -ne 0 ]; then
	testserver_cleanup
	rreturn 1 'agent output failed'
fi


testserver_cleanup
rreturn 0 $0
