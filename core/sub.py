from google.cloud import pubsub_v1


class WorkflowStateMachine:

  state = "Completed"
  terminate_command = False

  def is_terminate_command(self):
      return self.terminate_command

  def terminate(self):
      self.terminate_command = True

def process_topic(subscriber, subscription_path, workflow_state_machine):

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
        #retry=retry.Retry(deadline=300),
    )

    ack_ids = []
    for received_message in response.received_messages:
        print(received_message)
        print(f"Received: {received_message.message.data}.")
        ack_ids.append(received_message.ack_id)
        if received_message.message.attributes:
            print("Attributes:")
            for key in received_message.message.attributes:
                value = received_message.message.attributes.get(key)
                print(f"{key}: {value}")

    if len(ack_ids) != 0:
        # Acknowledges the received messages so they will not be sent again.
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": ack_ids}
        )

    print(
        f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
    )

    #ToDO: update / process the Workflow State MAchine based on the received events/messages

    return workflow_state_machine



project_id = "studied-client-297916"

upstream_subscription_id = "upstream-central-orchestrator"
sdl_subscription_id = "sdl-central-orchestrator"
sfl_subscription_id = "sfl-central-orchestrator"

upstream_subscriber = pubsub_v1.SubscriberClient()
sfl_subscriber = pubsub_v1.SubscriberClient()

upstream_subscription_path = upstream_subscriber.subscription_path(project_id, upstream_subscription_id)
sfl_subscription_path = sfl_subscriber.subscription_path(project_id, sfl_subscription_id)

NUM_MESSAGES = 1

workflow_state_machine = WorkflowStateMachine()

while True:

    workflow_state_machine = process_topic(upstream_subscriber, upstream_subscription_path, workflow_state_machine)

    workflow_state_machine = process_topic(sfl_subscriber, sfl_subscription_path, workflow_state_machine)
