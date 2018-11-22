curl -w "\n" \
-H "Accept: application/json" \
-F "deployment-name=cancel_order" \
-F "enable-duplicate-filtering=true" \
-F "deploy-changed-only=true" \
-F "cancel_order.bpmn=@cancel_order.bpmn" \
-F "tenant-id=cancel_order_1" http://localhost:8080/engine-rest/deployment/create
