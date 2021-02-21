from google.cloud import pubsub_v1

# TODO(developer)
project_id = "studied-client-297916"

upstream_topic_id = "argo"
sfl_topic_id = "sfl-hub"

upstream_publisher = pubsub_v1.PublisherClient()
upstream_topic_path = upstream_publisher.topic_path(project_id, upstream_topic_id)

for n in range(1, 5):
    data = "Upstream Msg number {}".format(n)
    # Data must be a bytestring
    data = data.encode("utf-8")
    # Add two attributes, origin and username, to the message
    future = upstream_publisher.publish(
        upstream_topic_path, data, origin="workflow-orchestrator", event_name="UPSTREAM_WORKFLOW_COMPLETION"
    )
    print(future.result())

print(f"Published Upstream messages with custom attributes to {upstream_topic_path}.")

################################################################################################

sfl_publisher = pubsub_v1.PublisherClient()
sfl_topic_path = sfl_publisher.topic_path(project_id, sfl_topic_id)

for n in range(1, 5):
    data = "SFL Msg number {}".format(n)
    # Data must be a bytestring
    data = data.encode("utf-8")
    # Add two attributes, origin and username, to the message
    future = sfl_publisher.publish(
        sfl_topic_path, data, origin="workflow-orchestrator", event_name="SFL_WORKFLOW_COMPLETION"
    )
    print(future.result())

print(f"Published SFL messages with custom attributes to {sfl_topic_path}.")