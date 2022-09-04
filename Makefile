integration_test:
	sh Test/integration_test/run.sh



build: integration_test
	docker-compose -f web_service_monitoring/docker-compose.yml up -d

train:
	sh Tracking_Orchestration/track.sh

stop:
	docker-compose -f web_service_monitoring/docker-compose.yml down
