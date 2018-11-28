curl -w "\n" \                                          
-H "Accept: application/json" \
-F "deployment-name=create_event" \
-F "enable-duplicate-filtering=true" \
-F "deploy-changed-only=true" \
-F "create_event.bpmn=@create_event.bpmn" \
-F "tenant-id=create_event_1" http://localhost:8080/engine-rest/deployment/create \
&& \
curl -w "\n" \
-H "Accept: application/json" \
-F "deployment-name=book_event" \
-F "enable-duplicate-filtering=true" \
-F "deploy-changed-only=true" \
-F "cancel_order.bpmn=@book_event.bpmn" \
-F "tenant-id=book_event_1" http://localhost:8080/engine-rest/deployment/create \
&& \
curl -w "\n" \
-H "Accept: application/json" \
-F "deployment-name=book_event" \
-F "enable-duplicate-filtering=true" \
-F "deploy-changed-only=true" \
-F "cancel_order.bpmn=@book_event.bpmn" \
-F "tenant-id=book_event_1" http://localhost:8080/engine-rest/deployment/create
