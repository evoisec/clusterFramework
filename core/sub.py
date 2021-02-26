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
# still one message at a time ie Strictly Sequentially or we can process just one message per each invocation
# of this function
# The current implementation processes strictly one event message per invocation
############################################################################################################
def process_topic(subscriber, subscription_path, workflow_state_machine):

    # this is synchrnous pull pubsub client - its use is part of the solution for Strictly Sequential Event Processing
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
        #retry=retry.Retry(deadline=300),
    )

    if len(response.received_messages) != 0:

        # ToDO: On first connection to the topic, Ignore and ACK all Event Messages with timestamp older than the
        # the system time when the connection to the topic was establsihed

        ############################################################################
        # Go to the end of the topic and start consuming messages from there. Execute only once, On first connection to the topic,
        # Ignore and ACK all Event Messages with timestamp older than the the system time when the new/first connection to
        # the topic was establsihed
        ############################################################################

        print("Just launched for the first time, positioning at the end of the message topic/queue, thus skpipping all old message in the topic/queue")


        received_message = response.received_messages[0]
        print(received_message)
        print(f"Received: {received_message.message.data}.")
        ack_ids = [received_message.ack_id]

        if received_message.message.attributes:
                print("Attributes:")
                for key in received_message.message.attributes:
                    value = received_message.message.attributes.get(key)
                    print(f"{key}: {value}")


        #ToDO: Dedup the Event Message

        ############################################################################
        # Dedup the Event Message against CO Audit Log, here also skip any further processing - if dedup conditions encountered
        ############################################################################

        print("Deduping the Event Message against the CO Audit Log")

        #ToDO: Persist the Event Message to the CO Audit Log

        ############################################################################
        # Persist the Event Message in CO Audit Log conditional on only if it doesnt already exist there
        # When done here, it prevents Race Conditions between CO and the CC Workflows when updating the CO Audit Log
        # This step corresponds to Workflow State = Event Message Received by CO and Stored in CO Audit Log
        ############################################################################

        print("Persisting the Event Message to the CO Audit Log")

        ############################################################################
        # Acknowledge the Event Message to GCP PUBSUB
        ############################################################################

        # check whether ACK can still be done and of not, then consume the message again and ACK it

        request = {"subscription": subscription_path, "ack_ids": ack_ids}
        subscriber.acknowledge(request)
        print( f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}." )

        #ToDO: Perform business processing for the messages in the current topic and then update / process the Workflow State MAchine based on the received events/messages


        ############################################################################
        # Map Event Message to CC Argo Workflow Name
        ############################################################################

        print("Mapping Event Message to CC Argo Workflow Name")

        ############################################################################
        # Trigger CC Argo Workflow
        ############################################################################
        print("Triggering CC Argo Workflow")

        ############################################################################
        # Keep checking the CO Audit Log whether the CC Workflow had started - loop for a configurable interval
        ############################################################################
        print("Checking whether the CC Argo Workflow has started")


    # ToDO: perform final operation on the State Machine before return

    return workflow_state_machine


project_id = "studied-client-297916"
cc_topic_subscription_id = "upstream-central-orchestrator"

cc_topic_subscriber = pubsub_v1.SubscriberClient()
cc_topic_subscription_path = cc_topic_subscriber.subscription_path(project_id, cc_topic_subscription_id)

# Enforces strictly sequential message processing (in combination with the used synchronous pull pubsub client type)
NUM_MESSAGES = 1

workflow_state_machine = WorkflowStateMachine()


##############################################################################################
# This is the main Central Orchestrator (CO) processing loop. It cycles through each topic (currently only one), processes the messages/events and
# updates the CO Audit Log and Workflow State Machine. It exits if it receives a command from the command topic
##############################################################################################
while True:

    print("################### Start of New Event Message Processing Cycle #########################################################")

    workflow_state_machine = process_topic(cc_topic_subscriber, cc_topic_subscription_path, workflow_state_machine)




