from google.cloud import pubsub_v1

# TODO(developer)
project_id = "studied-client-297916"

upstream_topic_id = "argo"

upstream_publisher = pubsub_v1.PublisherClient()
upstream_topic_path = upstream_publisher.topic_path(project_id, upstream_topic_id)

for n in range(1, 4):
    data = """{"event_name":"ledger_refresh_completion","source":"workflow_1","is_cascade":true,"reporting_date":"2021-3-3"}"""
    #     Data must be a bytestring
    data = data.encode("utf-8")
    # Add two attributes, origin and username, to the message
    future = upstream_publisher.publish(
         upstream_topic_path, data, origin="workflow-orchestrator", event_name="ledger_refresh_completion", event_seq_number = str(n)
    )
    print(future.result())

print(f"Published internal CC messages with custom attributes to {upstream_topic_path}.")

################################################################################################



