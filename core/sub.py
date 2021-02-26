import sys
from google.cloud import pubsub_v1

class WorkflowStateMachine:

  state = "Completed"
  terminate_command = False

  def is_terminate_command(self):
      return self.terminate_command

  def terminate(self):
      self.terminate_command = True


############################################################################################################
# Note, while processing the messages/events in a topic, here we can loop until all messages are processed
# still one message at a time ie Strictly Sequentially or we can process just one message per each invokation
# of this function
############################################################################################################
def process_topic(subscriber, subscription_path, workflow_state_machine):

    # this is synchrnous pull pubsub client - its use is part of the solution for Strictly Sequential Event Processing
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
        #retry=retry.Retry(deadline=300),
    )

    if len(response.received_messages) != 0:

        received_message = response.received_messages[0]
        print(received_message)
        print(f"Received: {received_message.message.data}.")
        ack_ids = [received_message.ack_id]

        if received_message.message.attributes:
                print("Attributes:")
                for key in received_message.message.attributes:
                    value = received_message.message.attributes.get(key)
                    print(f"{key}: {value}")


        #ToDO: Perform business processing for the messages in the current topic and then update / process the Workflow State MAchine based on the received events/messages


        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": ack_ids}
        )

        print(
            f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
        )

    # ToDO: perform final operation on the State Machine before return

    return workflow_state_machine


def sdl_event_generator(workflow_state_machine):
    return 0


project_id = "studied-client-297916"

upstream_subscription_id = "upstream-central-orchestrator"
sdl_subscription_id = "sdl-central-orchestrator"
sfl_subscription_id = "sfl-central-orchestrator"
command_subscription_id = "command-channel-central-orchestrator"

upstream_subscriber = pubsub_v1.SubscriberClient()
sdl_subscriber = pubsub_v1.SubscriberClient()
sfl_subscriber = pubsub_v1.SubscriberClient()
command_subscriber = pubsub_v1.SubscriberClient()

upstream_subscription_path = upstream_subscriber.subscription_path(project_id, upstream_subscription_id)
sdl_subscription_path = sdl_subscriber.subscription_path(project_id, sdl_subscription_id)
sfl_subscription_path = sfl_subscriber.subscription_path(project_id, sfl_subscription_id)
command_subscription_path = command_subscriber.subscription_path(project_id, command_subscription_id)

# Enforces strictly sequential message processing (in combination with the used synchronous pull pubsub client type)
NUM_MESSAGES = 1

workflow_state_machine = WorkflowStateMachine()


##############################################################################################
# This is the main processing loop. It cycles through each topic, processes the messages/events and
# updates the Workflow State Machine. It exits if it receives a command from the command topic
##############################################################################################
while True:

    # Business Logic for Upstream EoD Events

    print("#########################################################################################################")

    workflow_state_machine = process_topic(upstream_subscriber, upstream_subscription_path, workflow_state_machine)




