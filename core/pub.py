from google.cloud import pubsub_v1

# TODO(developer)
project_id = "studied-client-297916"
topic_id = "argo"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

for n in range(1, 2):
    data = "Msg number {}".format(n)
    # Data must be a bytestring
    data = data.encode("utf-8")
    # Add two attributes, origin and username, to the message
    future = publisher.publish(
        topic_path, data, origin="workflow-orchestrator", event_name="WORKFLOW_COMPLETION"
    )
    print(future.result())

print(f"Published messages with custom attributes to {topic_path}.")